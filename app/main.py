from fastapi import FastAPI

app = FastAPI(
    title = "FastAPi Gen Ai Project",
    description = "Generating FastAPi project",
    version = "1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Hi All This is Gen Ai Project"
    }

