from fastapi import FastAPI

app = FastAPI(title="Homelab Atlas")


@app.get("/health")
def health():
    return {"status": "ok"}
