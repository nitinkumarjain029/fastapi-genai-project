from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks
from app.routers.users import router as users_router
from app.db.database import Base, engine
from app.db import models
from fastapi import Request
from app.core.exceptions import global_exception_handler, UserNotFoundException,EmailAlreadyExistsException, user_not_found_exception_handler, email_already_exists_exception_handler
from fastapi.middleware.cors import CORSMiddleware
import time
import asyncio
import logging
from fastapi import UploadFile, File
from pathlib import Path
import uuid
from fastapi.responses import JSONResponse

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title = "FastAPi Gen Ai Project",
    description = "Generating FastAPi project",
    version = "1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled error on %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request : Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
    f"{request.method} {request.url.path} "
    f"status={response.status_code} "
    f"time={process_time:.4f}s"
)


    return response



Base.metadata.create_all(bind=engine)





app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)

app.add_exception_handler(Exception, global_exception_handler)

app.add_exception_handler(EmailAlreadyExistsException, email_already_exists_exception_handler)


app.include_router(users_router)

@app.get("/")
def home():
    return {
        "message": "Hi All This is Gen Ai Project"
    }


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
CHUNK_SIZE = 1024 * 1024          # 1 MB


def process_file():
    print("task Started")

    time.sleep(4)

    print("task Completed")

@app.post("/background-test")
def background_test(background_tasks : BackgroundTasks):
    background_tasks.add_task(process_file)

    return {
        "message": "Task added Successfully"
    }


@app.post("/uploads")
async def upload_file(file: UploadFile = File(...)):

    # 1️⃣ Extension check
    file_extension = Path(file.filename).suffix.lower()

    if file_extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # 2️⃣ MIME type check
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )

    # 3️⃣ Actual PDF signature check
    file_header = await file.read(5)

    if file_header != b"%PDF-":
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    # Pointer ko wapas beginning par lao
    await file.seek(0)

    # 4️⃣ Unique filename generate karo
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # 5️⃣ Final path
    file_path = UPLOAD_DIR / unique_filename

    # 6️⃣ Size + save
    total_size = 0
    CHUNK_SIZE = 1024 * 1024

    try:
        with open(file_path, "wb") as buffer:

            while True:
                chunk = await file.read(CHUNK_SIZE)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File size must be less than 5 MB"
                    )

                buffer.write(chunk)

    except HTTPException:
        if file_path.exists():
            file_path.unlink()
        raise

    return {
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "content_type": file.content_type,
        "size": total_size
    }
