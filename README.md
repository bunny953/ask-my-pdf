# Ask My PDF 📄🤖

**Ask My PDF** is a lightweight Retrieval-Augmented Generation (RAG) backend API. It allows users to upload PDF documents and ask questions about the content, receiving AI-generated answers based strictly on the document's text.

This project is built from scratch as a hands-on learning journey into AI engineering, backend development, and open-source GitHub workflows (Issues, Branches, and Pull Requests).

## 🛠️ Tech Stack
* **Framework:** Python & FastAPI
* **AI Orchestration:** LangChain
* **Vector Database:** ChromaDB (Local)
* **LLM:** OpenAI API (or HuggingFace)

## 🚀 What it does
1. **Ingests** PDF documents and extracts raw text.
2. **Chunks** the text into manageable pieces.
3. **Embeds** and stores the text in a local vector database.
4. **Retrieves** the most relevant context based on user questions.
5. **Generates** accurate answers using a Large Language Model.
