import os
import requests
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from groq import Groq

# 1. Load configuration and setup Groq Client
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# --- FREE CLOUD EMBEDDING ENGINE VIA HUGGING FACE SERVERLESS ---
class CloudEmbeddings:
    """Uses Hugging Face's free cloud API to turn text chunks into coordinates, 0% local GPU used."""
    def __init__(self):
        # Using a highly standard open-source embedding model hosted on free cloud infrastructure
        self.api_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        # No extra API keys needed for low-volume student testing!
        self.headers = {} 

    def _query_api(self, texts):
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": texts})
        if response.status_code != 200:
            raise Exception(f"Hugging Face Cloud Error: {response.text}")
        return response.json()

    def embed_documents(self, texts):
        # Send chunks to cloud for processing
        return self._query_api(texts)
        
    def embed_query(self, text):
        # Send single chat question to cloud
        return self._query_api([text])[0]

def process_pdf(pdf_path):
    print("\n[1/3] Reading PDF file...")
    reader = PdfReader(pdf_path)
    raw_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text + "\n"
            
    print("[2/3] Slicing text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(raw_text)
    print(f"-> Created {len(chunks)} text chunks.")
    
    print("[3/3] Generating Free Cloud Embeddings & Building Shelf (FAISS)...")
    embedding_engine = CloudEmbeddings()
    vector_db = FAISS.from_texts(chunks, embedding_engine)
    print("-> Vector Database successfully built via Cloud API!")
    return vector_db

def main():
    pdf_file = input("Enter the full path to your PDF file: ").strip('双"') 
    if not os.path.exists(pdf_file):
        print("Error: That PDF file path does not exist!")
        return
        
    db = process_pdf(pdf_file)
    
    print("\n=== AI Study Assistant (Hybrid Cloud Mode) Ready ===")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_question = input("Ask a question about the PDF: ")
        if user_question.lower() == "quit":
            break
        if not user_question.strip():
            continue
            
        # Search the database for the top 3 relevant chunks
        relevant_docs = db.similarity_search(user_question, k=3)
        context_text = "\n\n--- Chunk ---\n".join([doc.page_content for doc in relevant_docs])
        
        system_prompt = f"""You are an AI Study Assistant. 
Answer the user's question using ONLY the provided context extracted from their textbook/notes below.
If the answer cannot be found in the context, say 'I cannot find that in the provided document.'

Context:
{context_text}"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )
        print(f"\nAssistant: {response.choices[0].message.content}\n")

if __name__ == "__main__":
    main()