from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)

    file_path = os.path.join("temp", file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "filename": file.filename,
        "message": "PDF uploaded successfully"
    }