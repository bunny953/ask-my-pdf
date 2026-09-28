from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import io
import os

app = FastAPI()


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

    return {
        "filename": file.filename,
        "character_length": len(extracted_text)
    }