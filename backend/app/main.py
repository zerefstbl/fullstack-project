from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.main import router as api_router

app = FastAPI(title="rocketman-challenge")

app.include_router(api_router, prefix="/api")

@app.get("/", include_in_schema=False)
async def ping() -> JSONResponse:
    return JSONResponse({"ping": "pong"})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
