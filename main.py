from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import io

app = FastAPI()

CHROMA_DIR = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

vector_store = Chroma(
    collection_name="pdf_documents",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR,
)


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

    # Remove previously stored chunks for the same file
    vector_store.delete(
        where={"source": filename}
    )

    # Use deterministic IDs so each filename/chunk pair is identifiable
    chunk_ids = [
        f"{filename}_{index}"
        for index in range(len(chunks))
    ]

    vector_store.add_documents(
        documents=chunks,
        ids=chunk_ids,
    )

    return len(chunks)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    file_bytes = file.file.read()

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
