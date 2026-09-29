from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import io
import os

app = FastAPI()

CHROMA_DIR = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def store_text_in_vector_db(text: str, filename: str) -> int:
    """Split extracted text, generate embeddings, and store them in ChromaDB."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = text_splitter.create_documents(
        [text],
        metadatas=[{"source": filename}],
    )

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        collection_name="pdf_documents",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    vector_store.add_documents(chunks)

    return len(chunks)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)

    file_bytes = await file.read()

    file_path = os.path.join("temp", file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file_bytes)

    reader = PdfReader(io.BytesIO(file_bytes))

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text() or ""
        extracted_text += text

    chunk_count = store_text_in_vector_db(
        extracted_text,
        file.filename,
    )

    return {
        "filename": file.filename,
        "character_length": len(extracted_text),
        "chunk_count": chunk_count,
        "message": "PDF processed and stored in ChromaDB",
    }
