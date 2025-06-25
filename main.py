from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from db import SessionLocal
from models import FileMeta
from process import remove_img
import uuid
import os
import datetime
import asyncio

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def image(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    contents = await file.read()

    file_id = str(uuid.uuid4())
    unique_filename = f"{file_id}.png"
    output_path = f"outputs/{unique_filename}"
    os.makedirs("outputs", exist_ok=True)

    result = remove_img(contents)
    with open(output_path, "wb") as f:
        f.write(result)

    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    token = str(uuid.uuid4())

    db = SessionLocal()
    meta = FileMeta(id=file_id, filename=unique_filename, expires_at=expiry, token=token)
    db.add(meta)
    db.commit()
    db.close()

    background_tasks.add_task(auto_delete_file, unique_filename, expiry)

    return {
        "image_url": f"/output/{file_id}?token={token}",
        "download_url": f"/download/{file_id}?token={token}"
    }

@app.get("/output/{file_id}")
def serve_image(file_id: str, token: str):
    file_info = validate_file(file_id, token)
    return FileResponse(f"outputs/{file_info.filename}")

@app.get("/download/{file_id}")
def download_image(file_id: str, token: str):
    file_info = validate_file(file_id, token)
    return FileResponse(f"outputs/{file_info.filename}", filename=file_info.filename)

def validate_file(file_id, token):
    db = SessionLocal()
    file_info = db.query(FileMeta).filter(FileMeta.id == file_id).first()
    db.close()

    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    if file_info.token != token:
        raise HTTPException(status_code=403, detail="Invalid token")
    if datetime.datetime.utcnow() > file_info.expires_at:
        raise HTTPException(status_code=410, detail="File expired")

    return file_info

async def auto_delete_file(filename, expiry_time):
    now = datetime.datetime.utcnow()
    wait_time = (expiry_time - now).total_seconds()
    if wait_time > 0:
        await asyncio.sleep(wait_time)

    path = f"outputs/{filename}"
    if os.path.exists(path):
        os.remove(path)

    db = SessionLocal()
    db.query(FileMeta).filter(FileMeta.filename == filename).delete()
    db.commit()
    db.close()
