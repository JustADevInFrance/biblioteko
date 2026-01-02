#!/bin/bash

# Sortir si une commande échoue
set -e

echo "Création de l'environnement virtuel..."
python3 -m venv venv

echo "Activation de l'environnement virtuel..."
# Vérifie le shell pour activation
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Erreur : le venv n'a pas été créé correctement."
    exit 1
fi

echo "Installation des dépendances depuis requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation du package en mode édition..."
pip install -e .

echo "Démarrage du serveur avec pserve..."
pserve development.ini

