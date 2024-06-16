from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.main import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="rocketman-challenge")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

app.include_router(api_router, prefix="/api")

@app.get("/", include_in_schema=False)
async def ping() -> JSONResponse:
    return JSONResponse({"ping": "pong"})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
