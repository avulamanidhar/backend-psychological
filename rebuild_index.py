import os
import django
import sys
import numpy as np

# Automatically find and set up the Django project relative to the script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindguard_backend.settings')
django.setup()

from api.rag_utils import RAGManager

def main():
    print("🚀 Starting MindGuard AI Knowledge Base Rebuilder...")
    
    try:
        # Initialize the Manager (loads environment secrets automatically)
        rag_mgr = RAGManager()
        
        use_openai = os.getenv("USE_OPENAI", "True").lower() == "true"
        if not use_openai:
            print("🧱 MOCK MODE ACTIVE: Skipping OpenAI, generating random vectors for logic testing.")
        
        print("📁 Reading JSON knowledge base and database models...")
        # Step 1-6 are handled within refresh_knowledge_base():
        # - Reads JSON
        # - Combines keywords + content
        # - Generates OpenAI embeddings
        # - Stores embedding, original content, and metadata
        # - Saves in FAISS
        # - Safe overwrite/re-run logic
        rag_mgr.refresh_knowledge_base()
        
        # Verify success
        if os.path.exists(rag_mgr.index_path) and os.path.exists(rag_mgr.docs_path):
            doc_count = len(rag_mgr.doc_metadata)
            print(f"✅ Success! New index created with {doc_count} documents.")
            print(f"📍 Files saved: \n  - {os.path.basename(rag_mgr.index_path)}\n  - {os.path.basename(rag_mgr.docs_path)}")
        else:
            print("❌ Error: Files were not saved correctly.")
            
    except Exception as e:
        print(f"❌ REBUILD FAILED: {str(e)}")
        print("\nPossible fixes:")
        print("  - Check your OPENAI_API_KEY in the .env file")
        print("  - Ensure your MySQL database is reachable")
        print("  - Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
