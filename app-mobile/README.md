# Backend - Iporã Premiada

## Estrutura

backend/
 └── app/
      ├── __init__.py
      ├── database.py
      ├── models.py
      └── routes/
            ├── __init__.py
            ├── notas.py
            ├── usuarios.py
            └── sorteios.py

## Como rodar

1. Crie e ative o ambiente virtual (opcional).
2. Instale dependências:

   pip install fastapi uvicorn sqlalchemy pydantic requests beautifulsoup4

3. Rode o backend:

   python main.py

4. A API ficará em:

   http://127.0.0.1:8000

5. Documentação automática (Swagger):

   http://127.0.0.1:8000/docs
