from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from rotas import marcacoes, utilizadores, equipamentos

# Criar as tabelas na base de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Booklytic API",
    description="API de agendamento para servicos tecnicos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir as rotas
app.include_router(marcacoes.router, prefix="/api/v1", tags=["Marcacoes"])
app.include_router(utilizadores.router, prefix="/api/v1", tags=["Utilizadores"])
app.include_router(equipamentos.router, prefix="/api/v1", tags=["Equipamentos"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo a API do Booklytic"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
