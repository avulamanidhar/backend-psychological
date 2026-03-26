import os
import faiss
import numpy as np
import json
from openai import OpenAI
import google.generativeai as genai
from django.conf import settings
from .models import FAQ, AITransparency, HowItWorksStep, PrivacyPolicy

class RAGManager:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("⚠️ OPENAI_API_KEY is not set or is using placeholder. Set it in .env to use OpenAI.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here":
            genai.configure(api_key=self.gemini_api_key)
        else:
            print("⚠️ GEMINI_API_KEY is not set or is using placeholder. Set it in .env to use Gemini.")

        self.kb_dir = os.path.join(settings.BASE_DIR, "knowledge_base")
        self.index_path = os.path.join(settings.BASE_DIR, "faiss_index.bin")
        self.docs_path = os.path.join(settings.BASE_DIR, "kb_metadata.npy") # Stores content + metadata
        self.index = None
        self.doc_metadata = [] 
        self.embedding_model = "text-embedding-3-small"

    def load_or_create_index(self):
        """Loads the FAISS index if it exists, otherwise creates one."""
        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            try:
                self.index = faiss.read_index(self.index_path)
                self.doc_metadata = np.load(self.docs_path, allow_pickle=True).tolist()
            except Exception as e:
                print(f"Error loading FAISS index: {e}. Refreshing...")
                self.refresh_knowledge_base()
        else:
            self.refresh_knowledge_base()

    def refresh_knowledge_base(self):
        """Fetches data, generates embeddings with combined keywords/content, and saves everything."""
        processed_docs = [] # List of { 'text_for_embedding': '...', 'content': '...', 'metadata': {...} }
        
        # 1. PROCESS JSON KNOWLEDGE BASE
        json_kb_path = os.path.join(self.kb_dir, "mental_health_topics.json")
        if os.path.exists(json_kb_path):
            with open(json_kb_path, 'r', encoding='utf-8') as f:
                static_data = json.load(f)
                for item in static_data:
                    topic = item.get('topic', 'General Mental Health')
                    content = item.get('content') or item.get('description', '')
                    keywords = item.get('keywords', [])
                    severity = item.get('severity', 'low')
                    
                    # Combine keywords + content for better embedding search
                    keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
                    text_for_embedding = f"Topic: {topic}. Keywords: {keywords_str}. Content: {content}"
                    
                    processed_docs.append({
                        "text_for_embedding": text_for_embedding,
                        "content": content,
                        "metadata": {"topic": topic, "severity": severity, "source": "json"}
                    })

        # 2. PROCESS DATABASE ENTRIES
        try:
            for faq in FAQ.objects.all():
                processed_docs.append({
                    "text_for_embedding": f"FAQ: {faq.question} Answer: {faq.answer}",
                    "content": faq.answer,
                    "metadata": {"topic": "FAQ", "question": faq.question, "source": "db"}
                })
            
            for info in AITransparency.objects.all():
                processed_docs.append({
                    "text_for_embedding": f"SystemInfo: {info.title} {info.content}",
                    "content": info.content,
                    "metadata": {"topic": info.title, "source": "db"}
                })
        except Exception as e:
            print(f"DB Fetch warning: {e}")

        if not processed_docs:
            processed_docs.append({
                "text_for_embedding": "MindGuard AI providing mental health support.",
                "content": "MindGuard AI is a mental health support application.",
                "metadata": {"topic": "Default", "source": "fallback"}
            })

        # 3. GENERATE EMBEDDINGS & BUILD INDEX
        texts_to_embed = [d['text_for_embedding'] for d in processed_docs]
        embeddings = self._get_embeddings(texts_to_embed)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        # 4. SAVE (Safe re-run ensured by overwriting the single source of truth files)
        self.doc_metadata = [{"content": d['content'], "metadata": d['metadata']} for d in processed_docs]
        faiss.write_index(self.index, self.index_path)
        np.save(self.docs_path, np.array(self.doc_metadata, dtype=object))

    def _get_embeddings(self, texts):
        """Batch generate embeddings from OpenAI (or fallback to random for testing)."""
        use_openai = os.getenv("USE_OPENAI", "False").lower() == "true"
        
        try:
            if not use_openai or not self.client: raise Exception("Mock mode: Skipping OpenAI")
            response = self.client.embeddings.create(input=texts, model=self.embedding_model)
            return np.array([data.embedding for data in response.data]).astype('float32')
        except Exception as e:
            print(f"⚠️ OpenAI Embeddings failed: {e}. Generating mock vectors for testing...")
            return np.random.rand(len(texts), 1536).astype('float32')

    def retrieve_context(self, query, k_initial=5, k_final=3):
        """Advanced 2-stage retrieval: FAISS initial search + Keyword/Topic Re-ranking."""
        if self.index is None: self.load_or_create_index()
            
        query_embedding = self._get_embeddings([query])
        distances, indices = self.index.search(query_embedding, k_initial)
        
        candidates = []
        query_lower = query.lower()
        
        for idx in indices[0]:
            if idx != -1 and idx < len(self.doc_metadata):
                item = self.doc_metadata[idx]
                content = item['content']
                metadata = item['metadata']
                topic = metadata.get('topic', '').lower()
                
                # RE-RANKING LOGIC
                score = 0
                # 1. Keyword match (bonus for query words appearing in content)
                query_words = set(query_lower.split())
                content_words = set(content.lower().split())
                overlap = len(query_words.intersection(content_words))
                score += overlap * 2 
                
                # 2. Topic Match (bonus if the topic name is in the query)
                if topic and topic in query_lower:
                    score += 10
                
                candidates.append({
                    "score": score,
                    "topic": topic.title(),
                    "content": content
                })
        
        # Sort candidates by re-ranking score (highest first)
        sorted_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
        
        # Select best 2-3
        final_results = sorted_candidates[:k_final]
        
        context_blocks = []
        for res in final_results:
            context_blocks.append(f"[{res['topic']}]: {res['content']}")
        
        return "\n\n".join(context_blocks)

    def generate_ai_response(self, user_query, mode="General", language="English", history=None):
        """Generates AI response using Gemini or OpenAI, with fallback to mock."""
        context = self.retrieve_context(user_query)
        
        # --- Config & Flags ---
        use_gemini = os.getenv("USE_GEMINI", "False").lower() == "true"
        use_openai = os.getenv("USE_OPENAI", "False").lower() == "true"
        
        # 1. SYSTEM PROMPT
        system_msg = "You are a supportive, empathetic mental health assistant. Use the provided knowledge context strictly and prioritize the user's emotional state. Do not generate unsupported medical advice."
        
        # 2. CONTEXT BLOCK
        prompt = f"""
        Knowledge Context Block:
        {context}
        
        User Message:
        {user_query}
        
        Important: Respond empathetically to the user in {language}. If you don't have relevant information, tell the user you're here to listen, but remain supportive.
        """

        # --- GEMINI INTEGRATION ---
        if use_gemini and self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here":
            try:
                # Setup conversation history for Gemini
                gemini_history = []
                if history:
                    for msg in reversed(history):
                        # Gemini roles are "user" and "model"
                        role = "user" if msg.is_user else "model"
                        gemini_history.append({"role": role, "parts": [msg.text]})
                
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_msg
                )
                
                chat_session = model.start_chat(history=gemini_history)
                response = chat_session.send_message(prompt)
                return response.text.strip()
                
            except Exception as e:
                print(f"Gemini Chat failed: {e}")
                if "429" in str(e) or "quota" in str(e).lower():
                    return "My Gemini API key has run out of credits or quota! Please check your Google AI Studio plan. 💳"
                # If Gemini fails, we will gracefully fall down to OpenAI/mock

        # --- OPENAI INTEGRATION ---
        if use_openai and self.client:
            try:
                messages = [{"role": "system", "content": system_msg}]
                if history:
                    for msg in reversed(history):
                        messages.append({"role": "user" if msg.is_user else "assistant", "content": msg.text})
                messages.append({"role": "user", "content": prompt})
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=600
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"OpenAI Chat failed: {e}")
                if "insufficient_quota" in str(e) or "429" in str(e):
                    return "My OpenAI API key has run out of credits (Quota Exceeded). Please update your API key in the backend `.env` file! 💳"
                # Fall down to mock

        # --- FALLBACK MOCK RESPONSE ---
        if language == "Telugu":
            return f"[MOCK AI] నేను నీకు తోడుగా ఉన్నాను. నువ్వు చెప్పిన అంశం - {user_query}. మా దగ్గర ఉన్న సమాచారం: {context[:100]}..."
        return f"[MOCK AI] I hear you. You're talking about {user_query}. Based on my most relevant data: \n\n{context[:100]}..."
