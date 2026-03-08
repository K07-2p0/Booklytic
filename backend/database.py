# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. Carregar as senhas do ficheiro .env
load_dotenv()

# 2. Ir buscar o endereço da base de dados que guardámos no .env
URL_BASE_DADOS = os.getenv("DATABASE_URL")

# 3. Criar o "Motor" que faz a ligação direta ao PostgreSQL
engine = create_engine(URL_BASE_DADOS)

# 4. Criar a "fábrica" de sessões (cada vez que um utilizador pede algo, abrimos uma sessão)
SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. O Molde Base que vamos usar para criar as tabelas no próximo passo
Base = declarative_base()

# Função que o FastAPI vai usar para ligar e desligar a base de dados a cada pedido
def obter_bd():
    bd = SessaoLocal()
    try:
        yield bd
    finally:
        bd.close()