# ⚡ AI Study Assistant (Powered by Groq)

This is a fast, lightweight AI tool that turns your local PDF textbooks into an interactive chatbot. Instead of scrolling through hundreds of pages of a philosophy or science book, you can just upload it here and start asking questions directly.

It uses **Groq** on the backend to run Llama 3.3 models instantly, and **Gradio** to spin up a clean, simple web interface right on your screen.

---

## ✨ Features
* **Crazy Fast Answers:** Uses Groq's high-speed cloud processors to give you responses in milliseconds.
* **Secure API Setup:** Keeps your personal Groq API key safe by storing it inside a hidden `.env` file instead of pasting it directly into the code.
* **Simple Interface:** No complicated setups—just paste your PDF path, click initialize, and start chatting.

---

## 🧭 How the Data Flows

Here is a quick look at exactly what happens under the hood when you use the app:

1. **Reading the Book:** When you paste your PDF file path, the code uses `pypdf` to scrape all the text out of the file and save it into your app's temporary memory.
2. **Asking a Question:** When you type a question, your script takes your question and combines it with the text from your textbook into one single prompt.
3. **Getting the Answer:** The app grabs your secure API key from your hidden local variables, sends the prompt over the web to Groq, and prints out Llama's response inside your chat timeline.

---

## 🚀 How to Run it on Your Machine

Want to run this project locally? Just follow these steps:

### 1. Download the Code
Clone this repository to your desktop and jump into the project folder:
```bash
git clone [https://github.com/Azwad-Abid/AI-StudyAssistant.git](https://github.com/Azwad-Abid/AI-StudyAssistant.git)
cd AI-StudyAssistant
