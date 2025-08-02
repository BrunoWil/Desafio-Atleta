from fastapi import FastAPI
from routers import api_router
from configs.settings import settings

app = FastAPI(title="Desafio Atleta API", description="API para gerenciar informações de atletas", version="1.0.0")
app.include_router(api_router)

# if __name__ == "__main__":

#     import uvicorn

#     uvicorn.run(app, host="0.0.0", port=8000, log_level="info", reload=True)

