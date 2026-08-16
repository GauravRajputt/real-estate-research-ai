# 🔎 ResearchAI

### AI-Powered Source-Grounded Research Assistant

ResearchAI is a **Retrieval-Augmented Generation (RAG)** application that lets users provide web articles, process their content, and ask questions about the information contained in those sources.

It uses **Mistral AI**, **Hugging Face embeddings**, and **ChromaDB** to retrieve relevant information and generate source-grounded answers.

---

## ✨ Features

- 🌐 Process up to 3 web sources
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic similarity search
- 🤖 Mistral AI-powered answers
- 📚 Source-grounded responses
- 💾 ChromaDB vector database
- 🎨 Premium Streamlit UI
- 🌙 Dark Mode
- ☀️ Light Mode
- 🔗 Displays research sources

---

## 🖥️ Screenshots

### 🌙 Dark Mode

<img src="screenshots/dashboard-dark.png" alt="ResearchAI Dark Mode" width="900">

### ☀️ Light Mode

<img src="screenshots/dashboard-light.png" alt="ResearchAI Light Mode" width="900">

### 🤖 AI Research Result

<img src="screenshots/research-result.png" alt="ResearchAI AI Result" width="900">

> Upload your screenshots to a `screenshots` folder in the repository. GitHub supports relative image paths such as `screenshots/dashboard-dark.png`. :contentReference[oaicite:1]{index=1}

---

## 🧠 RAG Workflow

```text
Web URLs
   ↓
Web Content Extraction
   ↓
Text Chunking
   ↓
Hugging Face Embeddings
   ↓
ChromaDB
   ↓
Similarity Search
   ↓
Relevant Context
   ↓
Mistral AI
   ↓
AI Answer + Sources
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Streamlit | Web interface |
| LangChain | RAG pipeline |
| Mistral AI | LLM |
| Hugging Face | Embeddings |
| ChromaDB | Vector database |
| Unstructured | Web content extraction |

---

## 📂 Project Structure

```text
real-estate-tool/
│
├── main.py
├── rag.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── dashboard-dark.png
    ├── dashboard-light.png
    └── research-result.png
```

---

## 🎯 Use Cases

- 📰 News Research
- 🏠 Real Estate Research
- 📊 Business Research
- 🎓 Academic Research
- 🔍 Multi-source Information Analysis

---

## 🚀 Future Improvements

- 📄 PDF & document support
- 💬 Conversation memory
- 🔗 Improved citations
- ⚡ Streaming responses
- 🗂️ Research history
- 🧠 Improved retrieval and reranking
- 🌐 Support for more sources

---

## 👨‍💻 Author

### Gaurav Rajput

**B.Tech — Artificial Intelligence & Data Science**

🔗 [GitHub](https://github.com/GauravRajput)

---

⭐ **If you like this project, consider giving it a star!**
