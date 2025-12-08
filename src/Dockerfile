FROM python:3.12-slim

# 1. Installation des dépendances système
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Création du dossier de l'application
WORKDIR /app

# 3. Copier les sources du projet
COPY . /app

# 4. Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
RUN git config --global --add safe.directory /app/git_data
# 5. Exposer le port Pyramid
EXPOSE 6543

# 6. Commande de lancement
CMD ["python3", "app/main.py"]

