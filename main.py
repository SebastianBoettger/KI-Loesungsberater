from fastapi import FastAPI

app = FastAPI(title="KI-Lösungsberater")


@app.get("/")
def start():
    return {
        "status": "online",
        "message": "KI-Lösungsberater API läuft"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
