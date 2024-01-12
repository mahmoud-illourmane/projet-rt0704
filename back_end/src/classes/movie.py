from __future__ import annotations      # Permet d'utiliser le nom de la classe en tant que type dans les annotations de type
import json                             # Importation pour la manipulation de fichiers JSON
import base64                           # Importation pour la manipulation de données base64
import datetime                         # Importation pour la gestion des dates et heures
import os                               # Importation pour les opérations sur les fichiers et les répertoires
import re                               # Importation pour les expressions régulières
from flask import jsonify               # Importation du package jsonify de flask

"""
|
|   Author Mahmoud ILLOURMANE
|   DATE 12-22-23 US DATE
|
"""

class Movie:
    """
    Classe représentant un film avec ses données.

    Attributes:
        id (int): L'identifiant unique du film.
        movie_name (str): Le nom du film.
        year_of_creation (int): L'année de création du film.
        director (str): Le réalisateur du film.
        category (str): La catégorie du film.
        synopsis (str): Le résumé du film.
        rating (str): La notation du film.
        cover_image_base64 (str): La représentation base64 de l'image de couverture du film.
        creation_date (str): La date de création de l'instance de film.
        last_modified_date (str): La date de dernière modification de l'instance de film.
        cover_image_path (str): Le chemin du fichier image de couverture sauvegardé.

    Methods:
        to_dict(): Convertit l'instance de Movie en un dictionnaire.
        save_image(movie_name, base64_string): Sauvegarde l'image du film à partir d'une chaîne base64.
        save_movie(movie): Sauvegarde les données du film dans un fichier JSON.
        delete_movie_(movie_id): Supprime un film en fonction de son identifiant.
        edit_movie(data): Modifie une information d'un film en fonction de son identifiant.
    """
    
    def __init__(self, movie_data: dict):
        """
            Initialise une instance de la classe Movie avec les données d'un film.

        Args:
            movie_data (dict): Un dictionnaire contenant les données du film.
        """
        self.user_id = movie_data["user_id"]
        self.id = None
        self.movie_name = movie_data["movie_name"]
        self.year_of_creation = movie_data["year_of_creation"]
        self.director = movie_data["director"]
        self.category = movie_data["categorie"]       
        self.synopsis = movie_data["synopsis"]
        self.rating = movie_data["notation"]
        self.cover_image_base64 = movie_data["cover_image"]
        
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
        self.last_modified_date = self.creation_date

        # Traitement et sauvegarde de l'image
        self.cover_image_path = self.save_image(self.movie_name, self.cover_image_base64, self.user_id)

    def to_dict(self) -> dict:
        """
            Convertit l'instance de Movie en un dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les données du film.
        """
        
        return {
            "id": self.id,
            "movie_name": self.movie_name,
            "year_of_creation": self.year_of_creation,
            "director": self.director,
            "category": self.category,
            "synopsis": self.synopsis,
            "notation": self.rating,
            "cover_image_path": self.cover_image_path,
            "creation_date": self.creation_date,
            "last_modified_date": self.last_modified_date
        }

    def save_image(self, movie_name: str, base64_string: str, user_id: str) -> str:
        """
            Sauvegarde l'image du film à partir d'une chaîne base64.
            Le nom de l'image est fait avec le nom du film.
        
        Args:
            movie_name (str): Le nom du film pour générer le nom du fichier image.
            base64_string (str): La chaîne base64 représentant l'image.

        Returns:
            str: Le chemin du fichier image sauvegardé.
        """
        
        try:
            if base64_string == 'null':
                image_name = 'NOCOVERMOVIE.webp'
                image_path = os.path.join('storage', 'covers', image_name)
                return image_path
            else:
                format_match = re.search(r'data:image/(?P<format>[a-zA-Z]+);base64,', base64_string)
                image_format = format_match.group('format') if format_match else 'webp'
                if image_format == 'jpeg':
                    image_format = 'jpg'

                image_data = base64.b64decode(base64_string.split(',')[1] if format_match else base64_string)

                # Nettoie le nom du film pour l'utiliser dans le nom de fichier
                safe_movie_name = re.sub(r'[^A-Za-z0-9_]', '', movie_name)  # Remplace les caractères non alphanumériques

                image_name = f"{safe_movie_name}_{user_id}.{image_format}"
                image_path = os.path.join('storage', 'covers', image_name)

                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, 'wb') as file:
                    file.write(image_data)

                return image_path
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'image : {e}")
            return None

    @staticmethod
    def save_movie(movie: 'Movie', user_id) -> str:
        """
            Sauvegarde les données du film dans un fichier JSON.

            Args:
                movie (Movie): L'instance de Movie à sauvegarder.

            Returns:
                str: Une réponse JSON indiquant le statut de la sauvegarde.
        """
        
        try:
            # ouverture le fichier 'storage/movies.json' en mode lecture et écriture
            with open(f'storage/movies_{user_id}.json', 'r+') as file:
                data = json.load(file)              # Chargement du contenu JSON du fichier dans la variable 'data'
                movies = data["movies"]             # Accès à la liste 'movies' dans 'data'
                movie.id = data["nb_movies"] + 1    # Attribution d'un nouvel ID au film en ajoutant 1 au compteur 'nb_movies'
                movies.append(movie.to_dict())      # Ajout des données du film (sous forme de dictionnaire) à la liste 'movies'
                data["nb_movies"] += 1
                file.seek(0)                        # Positionnement de la position de lecture/écriture au début du fichier
                json.dump(data, file, indent=4)     # Écriture du contenu mis à jour dans le fichier JSON avec une mise en forme de 4 espaces
        except FileNotFoundError:
            try:
                # Si le fichier 'storage/movies_user_id.json' n'existe pas, je le crée en mode écriture
                # Normalement ce cas de figure ne devrai jamais arriver
                with open(f'storage/movies_{user_id}.json', 'w') as file:  
                    # Créeation d'un nouveau fichier JSON avec un compteur 'nb_movies' à 1
                    # et une liste 'movies' contenant les données du film en cours
                    json.dump({"nb_movies": 1, "movies": [movie.to_dict()]}, file, indent=4)
                    # Attribution de l'ID 1 au film s'il s'agit du premier film ajouté
                    movie.id = 1
            except Exception as e:
                error_message = f"Erreur lors de l'ouverture du fichier movies.json : {str(e)}"
                return jsonify({
                        "status": "500",
                        "error": error_message
                    }), 500

        return jsonify({
            "status": "200",
            "message": "Le film a bien été ajouté à votre vidéothèque."
        }), 200

    @staticmethod
    def delete_movie_(movie_id: int, user_id: str) -> str:
        """
            Supprime un film en fonction de son identifiant.

            Args:
                movie_id (int): L'identifiant unique du film à supprimer.

            Returns:
                str: Une réponse JSON indiquant le statut de la suppression.
        """
        
        try:
            int(movie_id)
        except ValueError:
            return jsonify({
                "status": "303",
                "error": "La veleur id doit être une valeur valide."
            }), 303
        
        try:
            # Ouvre le fichier JSON
            with open(f'storage/movies_{user_id}.json', 'r') as file:
                movies_data = json.load(file)
                
            # Trouve le film à supprimer
            movie_to_update = next((movie for movie in movies_data["movies"] if movie["id"] == movie_id), None)
            if not movie_to_update:
                return jsonify({
                    "status": "404",
                    "error": "Film non trouvé"
                }), 404

            # Récupère le chemin de l'image
            image_path = movie_to_update["cover_image_path"]

            # Vérifie si l'image n'est pas NOCOVERMOVIE.webp avant de la supprimer
            if image_path != 'storage\\covers\\NOCOVERMOVIE.webp' and os.path.exists(image_path):
                os.remove(image_path)

            # Supprime le film de la liste
            movies_data["movies"] = [movie for movie in movies_data["movies"] if movie["id"] != movie_id]
            movies_data["nb_movies"] -= 1  # Mettre à jour le compteur de films

            # Sauvegarde les modifications dans le fichier JSON
            with open(f'storage/movies_{user_id}.json', 'w') as file:
                json.dump(movies_data, file, indent=4)

            return jsonify({
                "status": "200",
                "message": "Le film a bien été supprimer de votre vidéothèque."
            }), 200
        
        except FileNotFoundError:
            return jsonify({
                "status": "404",
                "error": "Le fichier de films n'a pas été trouvé"
            }), 404
            
    @staticmethod
    def edit_movie(data: str, user_id: str) -> str:
        """
            Modifie une information d'un film en fonction de son identifiant.

            Args:
                data (str): Les données de modification du film.

            Returns:
                str: Une réponse JSON indiquant le statut de la modification.
        """
        
        movieId = data["movieId"]
        nameInfoToUpdate = data["inputName"]
        inputContent = data["inputContent"]
        try:
            # Ouvrre le fichier JSON
            with open(f'storage/movies_{user_id}.json', 'r') as file:
                movies_data = json.load(file)
                
            # Trouve le film à modifier
            movie_to_update = next((movie for movie in movies_data["movies"] if movie["id"] == int(movieId)), None)
            if not movie_to_update:
                return jsonify({
                    "status": "404",
                    "error": "Film non trouvé."
                }), 404

            # Modifie le champ nameInfoToUpdate du film avec inputContent
            movie_to_update[nameInfoToUpdate] = inputContent

            # Met à jour la date de dernière modification
            movie_to_update["last_modified_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Sauvegarde les modifications dans le fichier JSON
            with open(f'storage/movies_{user_id}.json', 'w') as file:
                json.dump(movies_data, file, indent=4)

            return jsonify({
                "status": "200",
                "message": "L'information du film a été mise à jour avec succès."
            }), 200
        
        except FileNotFoundError:
            return jsonify({
                "status": "404",
                "error": "Le fichier de films n'a pas été trouvé"
            }), 404
