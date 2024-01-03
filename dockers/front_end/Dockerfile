# Utiliser l'image de base Alpine avec Python 3.8
FROM python:3.8-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY /requirements.txt /app/

# Installer les dépendances
# gcc et musl-dev sont nécessaires pour compiler certaines dépendances Python
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --no-cache-dir -r requirements.txt

# Installer Flask
RUN pip install Flask

# Installer requests
RUN pip install requests

# Exposer le port (peut différer entre front et back)
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["python", "/app/app.py"]
