import uvicorn
from app import app
from app.database import Base, engine
from app import models  # garante que os models são importados

def criar_tabelas():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    criar_tabelas()
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
