import os
import gradio as gr

# Track system state globally
system_state = {"pdf_loaded": False, "pdf_path": ""}

def initialize_vector_core(path):
    if not path.strip():
        return "❌ Error: Please enter a file path."
    
    if os.path.exists(path):
        system_state["pdf_loaded"] = True
        system_state["pdf_path"] = path
        return f"✅ Success: Vector Core initialized using path:\n{path}"
    else:
        system_state["pdf_loaded"] = False
        return "❌ Error: The file path you entered does not exist. Please check it!"

# Classic Gradio chat logic (handles older version formats)
def chat_with_pdf(message, history):
    if not system_state["pdf_loaded"]:
        return "⚠️ Please initialize a valid System PDF absolute path first before chatting."
    
    filename = os.path.basename(system_state["pdf_path"])
    return f"I am analyzing '{filename}'. You said: '{message}'."


# Building the UI Layout
with gr.Blocks(title="Knowledge Network Builder") as demo:
    gr.Markdown("### *Transforming static textbooks into conversational knowledge networks.*")
    
    with gr.Row():
        # Left Column
        with gr.Column(scale=1):
            gr.Markdown("#### 📁 System PDF absolute path")
            path_input = gr.Textbox(label="Textbox", placeholder="Paste path here...")
            init_btn = gr.Button("Initialize Vector Core", variant="primary")
            
            gr.Markdown("#### System Status Node")
            status_output = gr.Textbox(label="Textbox", interactive=False)
            
        # Right Column
        with gr.Column(scale=2):
            gr.Markdown("#### ⚡ Central Intelligence Interface")
            
            # Removed the type parameter so it works perfectly on older Gradio versions
            gr.ChatInterface(fn=chat_with_pdf)

    # Connect the left side button
    init_btn.click(fn=initialize_vector_core, inputs=path_input, outputs=status_output)

if __name__ == "__main__":
    demo.launch(share=True)