import os
import requests
import gradio as gr
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Global variable to hold our vector database once loaded
vector_db = None

class CloudEmbeddings:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        self.headers = {} 

    def _query_api(self, texts):
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": texts})
        if response.status_code != 200:
            raise Exception(f"Hugging Face Cloud Error: {response.text}")
        return response.json()

    def embed_documents(self, texts):
        return self._query_api(texts)
        
    def embed_query(self, text):
        return self._query_api([text])[0]

# --- UI Backend Functions ---
def load_and_build_db(pdf_path):
    global vector_db
    pdf_path = pdf_path.strip('双"') 
    
    if not os.path.exists(pdf_path):
        return "❌ Error: The file path you entered does not exist. Please check it!"
    
    try:
        reader = PdfReader(pdf_path)
        raw_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text + "\n"
                
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(raw_text)
        
        embedding_engine = CloudEmbeddings()
        vector_db = FAISS.from_texts(chunks, embedding_engine)
        return f"✨ Success! Analyzed document and created {len(chunks)} chunks. Your Assistant is ready!"
    except Exception as e:
        return f"❌ Connection Error: Still unable to reach cloud server. (Details: {e})"

def chat_with_pdf(user_message, history):
    global vector_db
    if vector_db is None:
        return "Please input your PDF path and initialize the database first!"
        
    # Search vector database
    relevant_docs = vector_db.similarity_search(user_message, k=3)
    context_text = "\n\n--- Chunk ---\n".join([doc.page_content for doc in relevant_docs])
    
    system_prompt = f"""You are an AI Study Assistant. 
Answer the user's question using ONLY the provided context extracted from their textbook/notes below.
If the answer cannot be found in the context, say 'I cannot find that in the provided document.'

Context:
{context_text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq Cloud Error: Your Wi-Fi connection interrupted the request. ({e})"

# --- CUSTOM GRADIO 6 LAYOUT ---
with gr.Blocks() as app:
    
    gr.Markdown("""
    # 🧠 AI Study Assistant Matrix
    ### *Transforming static textbooks into conversational knowledge networks.*
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            pdf_input = gr.Textbox(
                label="📁 System PDF absolute path", 
                placeholder="Paste your path here (e.g., C:\\Users\\LENOVO\\Desktop\\dsad\\philosphy.pdf)"
            )
            load_btn = gr.Button("Initialize Vector Core", variant="primary")
            status_output = gr.Textbox(label="System Status Node", interactive=False, placeholder="Awaiting initialization...")
            
        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(
                fn=chat_with_pdf,
                title="⚡ Central Intelligence Interface"
            )
            
    load_btn.click(fn=load_and_build_db, inputs=pdf_input, outputs=status_output)

if __name__ == "__main__":
    # In Gradio 6, theme and custom CSS styles must pass directly into launch()
    custom_css = """
    .gradio-container { background: linear-gradient(135deg, #0f172a, #1e1b4b) !important; color: #e2e8f0 !important; }
    button.primary { background: linear-gradient(90deg, #6366f1, #a855f7) !important; color: white !important; border: none !important; }
    input, textarea { background-color: #1e293b !important; color: #f8fafc !important; border: 1px solid #475569 !important; }
    """
    app.launch(theme=gr.themes.Monochrome(), css=custom_css)