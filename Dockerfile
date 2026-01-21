FROM python:3.11-slim

LABEL maintainer="SAE DDAW - Sup Galilée"
LABEL description="API REST de gestion de projets collaboratifs"

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier TOUT le projet (pas seulement app/)
COPY . .

EXPOSE 8000

# Lancer FastAPI
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
