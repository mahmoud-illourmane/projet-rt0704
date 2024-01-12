# Utiliser l'image de base Alpine avec Python 3.8
FROM python:3.8-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY /requirements.txt /app/

#
# Installation des dépendances
#

# gcc et musl-dev sont nécessaires pour compiler certaines dépendances Python
RUN apk add --no-cache gcc musl-dev linux-headers

# Installation des dépendances Python à partir du fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Installation de Flask
RUN pip install Flask

# Installation de Flask-Login
RUN pip install flask-login

# Installation du package requests
RUN pip install requests

# Exposition du port
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["python", "/app/app.py"]