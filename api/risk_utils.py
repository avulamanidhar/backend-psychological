import os
from openai import OpenAI

class RiskAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        
        # Immediate High-Risk Keywords
        self.high_risk_keywords = [
            "suicide", "kill myself", "end my life", "suicidal", "better off dead", 
            "chavali", "pichodu", "die", "harm myself", "hurt myself", "cut my wrist"
        ]
        
        # Medium-Risk Keywords
        self.medium_risk_keywords = [
            "hopeless", "worthless", "can't go on", "nothing matters", 
            "empty", "suffering", "giving up", "no point"
        ]

    def analyze(self, text):
        """Classifies the risk level of a message."""
        text_lower = text.lower()
        
        # 1. Rule-based Fast Check (HIGH)
        if any(kw in text_lower for kw in self.high_risk_keywords):
            return "HIGH"
            
        # 2. LLM-based Contextual Check
        if not self.client:
            # Fallback to medium check if no API key
            if any(kw in text_lower for kw in self.medium_risk_keywords):
                return "MEDIUM"
            return "LOW"
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a clinical risk assessment assistant. Classify the user's message into LOW, MEDIUM, or HIGH risk related to self-harm or suicide. Reply with ONLY the category name."},
                    {"role": "user", "content": text}
                ],
                max_tokens=5,
                temperature=0.0
            )
            risk = response.choices[0].message.content.strip().upper()
            if risk in ["LOW", "MEDIUM", "HIGH"]:
                return risk
            return "LOW"
        except Exception as e:
            print(f"Risk Analysis error: {e}")
            return "MEDIUM" if any(kw in text_lower for kw in self.medium_risk_keywords) else "LOW"

    def get_emergency_response(self, language="English"):
        """Returns a standardized safe response for high-risk situations."""
        if language == "Telugu":
            return "నీ ప్రాణం చాలా విలువైనది. దయచేసి నీకు దగ్గరగా ఉన్న వారితో లేదా ఈ క్రింది హెల్ప్‌లైన్స్‌తో మాట్లాడండి:\n\n📞 AASRA: 9820466726\n📞 Vandrevala Foundation: 18602662345\nమేము నీకు తోడుగా ఉంటాను, కానీ ప్రొఫెషనల్ హెల్ప్ తీసుకోవడం చాలా ముఖ్యం. 💙"
        
        return "I hear how much pain you're in, and I want you to know that you're not alone. Your life is valuable. Please reach out to a professional or a crisis hotline right now:\n\n📞 National Suicide Prevention Lifeline: 988\n📞 Crisis Text Line: Text HOME to 741741\n\nPlease contact a trusted friend, family member, or healthcare provider immediately. 💙"
