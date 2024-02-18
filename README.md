# Mon Projet Flask

## Description

Ce dépôt contient un projet Flask structuré en trois composantes principales : le front-end, le back-end, et la configuration Docker. Cette structure vise à fournir une séparation claire des responsabilités et une maintenance aisée.

## Structure du Projet

Le projet est organisé comme suit :

- **`front_end/`** : Hégerge le serveur Flask Front. Contient tous les fichiers relatifs à l'interface utilisateur du projet. Cela inclut les templates HTML, les scripts JavaScript, et les fichiers CSS. Il contient également les fichiers de routes web.py et api.py pour intéragir avec l'api REST du serveur Backend.
- **`back_end/`** : Héberge le code serveur Flask Backend, y compris les routes API, la logique métier avec les classes Movie, User et TheMovieDb, et les interactions avec les fichiers jSon.
- **`dockers/`** : 
  - **`front_end/`** : Contient les fichiers Dockerfile et Docker-compose pour la configuration et le déploiement du front-end.
  - **`back_end/`** : Contient les fichiers Dockerfile et Docker-compose pour la configuration et le déploiement du back-end.

## Comment Utiliser

### Prérequis

- Python 3.8+
- Flask, requests : Docker compose les installera
- Docker
- Avoir un réseau Docker : docker network create projetRt0704Network
### Installation et Configuration

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/mahmoud-illourmane/projet-rt0704

2. **Lancer les conteneurs :**
   ```bash
   ubuntu@esys:~/projet-rt0704/dockers/back_end$ docker compose up -d
   ubuntu@esys:~/projet-rt0704/dockers/front_end$ docker compose up -d
4. **Utiliser l'application :**
   Entrez l'url dans un navigateur : addresse_ip:5000
