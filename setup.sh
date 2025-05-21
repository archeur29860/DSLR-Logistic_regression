#!/bin/bash

# Arrêter si une commande échoue
set -e

# Créer l'environnement virtuel
mkdir img
python3 -m venv .env

# Activer l'environnement virtuel
source .env/bin/activate

# Vérifier que le fichier requirements.txt existe
if [ ! -f requirements.txt ]; then
    echo "Erreur : le fichier requirements.txt est introuvable."
    exit 1
fi

# Installer les dépendances
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

echo "Environnement virtuel prêt et dépendances installées."
