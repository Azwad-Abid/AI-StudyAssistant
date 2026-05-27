import os
import customtkinter as ctk
from dotenv import load_dotenv
from groq import Groq

# 1. Load configuration and setup Groq Client
load_dotenv()
api_key = os.getenv("Groq_API_Key")
client = Groq(api_key=api_key)

# 2. Set up the AI Persona and chat history
system_prompt = """You are an AI Study Assistant.
Explain concepts clearly and simply.
Help students understand topics step by step."""

messages = [{"role": "system", "content": system_prompt}]

# 3. Initialize UI Theme Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StudyAssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Study Assistant")
        self.geometry("600x700")
        
        # --- UI LAYOUT COMPONENTS ---
        # Scrollable area where text messages appear
        self.chat_display = ctk.CTkScrollableFrame(self, width=560, height=550)
        self.chat_display.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Bottom frame containing input box and action button
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        # Input Text Entry Field
        self.user_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ask your study question here...", height=40)
        self.user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.user_entry.bind("<Return>", lambda event: self.send_message()) # Press Enter to send
        
        # Action Button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", width=100, height=40, command=self.send_message)
        self.send_button.pack(side="right")
        
        # Display greeting
        self.append_message_to_ui("Assistant: Hello! I am your AI Study Assistant. What are we learning today?", "grey")

    def append_message_to_ui(self, text, color):
        """Helper to inject new text boxes dynamically into the scrolling UI view"""
        msg_box = ctk.CTkLabel(
            self.chat_display, 
            text=text, 
            wraplength=500, 
            justify="left", 
            anchor="w",
            font=("Arial", 14),
            text_color=color
        )
        msg_box.pack(pady=10, padx=10, fill="x")
        # Auto scroll to the very bottom
        self.chat_display._parent_canvas.yview_moveto(1.0)

    def send_message(self):
        user_text = self.user_entry.get().strip()
        if not user_text:
            return
            
        # Clear entry box immediately for convenience
        self.user_entry.delete(0, 'end')
        
        # Render the User text locally onto screen
        self.append_message_to_ui(f"You: {user_text}", "#1f538d")
        
        # Save message text internally to history log array
        messages.append({"role": "user", "content": user_text})
        
        try:
            # Query the Groq Client engine
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )
            
            ai_reply = response.choices[0].message.content
            
            # Print AI text answer onto screen UI
            self.append_message_to_ui(f"Assistant: {ai_reply}", "#e5e5e5")
            
            # Commit AI response back to memory array history tracking
            messages.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            self.append_message_to_ui(f"System Error: Could not connect to API. Details: {e}", "red")

# 4. Fire up the execution loop
if __name__ == "__main__":
    app = StudyAssistantGUI()
    app.mainloop()