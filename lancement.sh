#!/bin/bash
set -e

echo "Création de l'environnement virtuel..."
python -m venv venv

echo "Activation de l'environnement virtuel..."
# Activation selon l'OS
if [ -f "venv/bin/activate" ]; then
    # Linux / macOS
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    # Windows (Git Bash / CMD)
    source venv/Scripts/activate
else
    echo "Erreur : le venv n'a pas été créé correctement."
    exit 1
fi

echo "Mise à jour de pip et installation des dépendances..."
# Toujours utiliser python -m pip pour éviter les erreurs Windows
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Installation du package en mode édition..."
python -m pip install -e .

echo "Démarrage du serveur avec pserve..."
# Utiliser python -m pserve si nécessaire
if command -v pserve >/dev/null 2>&1; then
    pserve development.ini
else
    python -m pyramid.scripts.pserve development.ini
fi
