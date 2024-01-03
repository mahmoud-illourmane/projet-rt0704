"""
|
|   This file contains the REST API routes for the application.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 20, 2023
|
"""

# Importation du fichier de configuration Flask
from app import app

from flask import jsonify, request
import json, base64

# Importation de la classe Movie
from src.classes.movie import Movie

# Importation de la classe TheMovieDB
from src.classes.themoviedb import TheMovieDB

"""
|   ===============
|   API REST ROUTES
|   ===============
"""

@app.route('/api/get-movies/index', methods=['GET'])
def get_movies_index():
    """
        Récupère tous les films d'un utilisateur avec les images.

        Cette route renvoie la liste complète des films d'un utilisateur depuis un fichier JSON.
        Les images de couverture des films sont encodées en base64 et incluses dans la réponse.

        Returns:
            JSON: Une réponse JSON contenant la liste des films de l'utilisateur avec les images encodées en base64.
                - "status": "200" en cas de succès.
                - "data": Un dictionnaire contenant la liste des films et leurs détails.

        Raises:
            FileNotFoundError: Si le fichier de films ou une image de film n'a pas été trouvé.
            HTTPError (404): Réponse JSON avec le statut "404" et un message d'erreur en cas de fichier manquant.

        HTTP Status Codes:
            - 200 OK: Si la liste des films est récupérée avec succès.
            - 404 Not Found: Si le fichier de films ou une image de film n'a pas été trouvé.
    """
    
    try:
        with open('storage/movies.json', 'r') as file:
            movies = json.load(file)

        for movie in movies["movies"]:
            image_path = movie["cover_image_path"].replace("\\", "/")

            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                movie["cover_image_base64"] = encoded_string

        response = {
            "status": "200",
            "data": movies,
        }

        return jsonify(response), 200
    except FileNotFoundError:
        response = {
            "status": "404",
            "error": "Le fichier de films ou une image de film n'a pas été trouvé"
        }
        return jsonify(response), 404
    
@app.route('/api/get-movies/gestions', methods=['GET'])
def get_movies_gestions():
    """
        Récupère tous les films d'un utilisateur sans les images pour la gestion.

        Cette route renvoie la liste complète des films d'un utilisateur depuis un fichier JSON,
        mais sans inclure les images de couverture des films. Les données sont préparées pour
        être affichées dans un tableau de gestion où l'utilisateur pourra effectuer des opérations
        telles que la suppression de films.

        Returns:
            JSON: Une réponse JSON contenant la liste des films de l'utilisateur sans les images de couverture.
                - "status": "ok" en cas de succès.
                - "nb_movies": Le nombre total de films de l'utilisateur.
                - "movies": Une liste des films de l'utilisateur sans les images.

        Raises:
            FileNotFoundError: Si le fichier de films n'a pas été trouvé.
            HTTPError (404): Réponse JSON avec un message d'erreur en cas de fichier manquant.

        HTTP Status Codes:
            - 200 OK: Si la liste des films est récupérée avec succès.
            - 404 Not Found: Si le fichier de films n'a pas été trouvé.
    """
    
    try:
        # Ouvrir le fichier JSON où se trouvent les données de la vidéothèque
        with open('storage/movies.json', 'r') as file:
            data = json.load(file)
        
        # Récupérer le nombre de films et la liste des films
        nb_movies = data["nb_movies"]
        movies = data["movies"]
        
        # Supprimer les chemins des images pour alléger la réponse
        for movie in movies:
            movie.pop('cover_image_path', None)
        
        # Créer une réponse JSON avec le nombre de films et la liste des films
        response = {
            "status": "200",
            "nb_movies": nb_movies,
            "movies": movies
        }
        
        return jsonify(response), 200
    except FileNotFoundError:
        # Si le fichier n'est pas trouvé, je renvoye une réponse avec un message d'erreur
        return jsonify({"error": "Le fichier de films n'a pas été trouvé"}), 404

@app.route('/api/add-movie', methods=['POST'])
def addMovie():
    """
        Ajoute un film à la vidéothèque de l'utilisateur à partir des données fournies par le client distant.

        Cette route permet à un client distant d'envoyer des données pour ajouter un film à la vidéothèque de l'utilisateur.
        Les données du film sont reçues au format JSON et utilisées pour créer une instance de la classe `Movie`.
        Ensuite, cette instance est ajoutée au fichier JSON contenant la vidéothèque de l'utilisateur.

        Returns:
            JSON: Une réponse JSON indiquant le statut de l'ajout du film.
                - "status": "ok" en cas de succès.
                - "message": Un message indiquant que le film a été ajouté avec succès.

        Raises:
            Any Exception: Si une exception non gérée se produit lors du traitement des données du film.

        HTTP Status Codes:
            - 200 OK: Si le film est ajouté avec succès.
            - 500 Internal Server Error: Si une exception non gérée se produit pendant le traitement.
    """
    
    if request.method == 'POST':
        try:
            movie_data = request.json

            movie = Movie(movie_data)
            response = movie.save_movie(movie)

            return response
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Erreur interne du serveur lors de l'ajout du film.",
                "error": str(e)
            }), 500

@app.route('/api/delete-movie', methods=['DELETE'])
def delete_movie():
    """
        Supprime un film de la vidéothèque de l'utilisateur.

        Cette route permet à l'utilisateur de supprimer un film de sa vidéothèque en fournissant
        l'identifiant du film à supprimer dans les données au format JSON.

        Returns:
            JSON: Une réponse JSON indiquant le statut de la suppression du film.
                - "status": "ok" en cas de succès.
                - "message": Un message indiquant que le film a été supprimé avec succès.

        Raises:
            Any Exception: Si une exception non gérée se produit lors de la suppression du film.

        HTTP Status Codes:
            - 200 OK: Si le film est supprimé avec succès.
            - 500 Internal Server Error: Si une exception non gérée se produit pendant le traitement.
    """
    
    try:
        data = request.json
        movieId = data["movieId"]
        
        response = Movie.delete_movie_(movieId)

        return response  # Je n'utilise pas jsonify(response) car la méthode delete_movie_ le fait déjà.
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Erreur interne du serveur lors de la suppression du film.",
            "error": str(e)
        }), 500

@app.route('/api/edit-movie', methods=['PATCH'])
def edit_movie():
    """
        Modifie une information sur un film dans la vidéothèque de l'utilisateur.

        Cette route permet à l'utilisateur de modifier une information spécifique d'un film en fournissant
        les données de modification au format JSON. Les modifications peuvent inclure le titre, l'année,
        le réalisateur, la catégorie, la notation, la synopsis, ou d'autres informations liées au film.

        Returns:
            JSON: Une réponse JSON indiquant le statut de la modification de l'information du film.
                - "status": "ok" en cas de succès.
                - "message": Un message indiquant que l'information du film a été mise à jour avec succès.

        Raises:
            Any Exception: Si une exception non gérée se produit lors de la modification de l'information du film.

        HTTP Status Codes:
            - 200 OK: Si l'information du film est modifiée avec succès.
            - 500 Internal Server Error: Si une exception non gérée se produit pendant le traitement.
        """
    try:
        data = request.json
        
        # Gestion des notations
        input_name = data.get("inputName")
        input_content = data.get("inputContent")
        
        if input_name == "notation":
            # Si la note est inférieure à 1, affecter automatiquement la valeur 1
            if int(input_content) < 1:
                data["inputContent"] = str(1)
            # Si la note est supérieure à 5, affecter automatiquement la valeur 5
            elif int(input_content) >= 5:
                data["inputContent"] = str(5)
                
        response = Movie.edit_movie(data)
        return response
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Erreur interne du serveur lors de la modification de l'information du film.",
            "error": str(e)
        }), 500

#
#
#   API themoviedb
#
#

@app.route('/api/themoviedb/get', methods=['GET'])
def api_themoviedb_get():
    """
    Récupère des films à partir de l'API TheMovieDB en fonction de l'opération spécifiée.

    Cette route permet à l'utilisateur de récupérer des films à partir de l'API TheMovieDB en spécifiant
    une opération (1: Recherche par nom, 2: Recherche par catégorie(s), 3: Recherche par année de sortie).
    Les données de l'opération sont passées en tant que paramètres dans la chaîne de requête.

    Returns:
        JSON: Une réponse JSON contenant les films retournés ou un message d'erreur le cas échéant.

    Raises:
        Any Exception: Si une exception non gérée se produit lors de la récupération des films depuis l'API.

    HTTP Status Codes:
        - 200 OK: Si les films sont récupérés avec succès depuis l'API.
        - 400 Bad Request: Si une opération incorrecte ou un format de catégorie de genre invalide est spécifié.
        - 500 Internal Server Error: Si une exception non gérée se produit pendant le traitement.
    """
    
    try:
        # Récupération des données de la chaîne de requête
        operationId = request.args.get("operationId")
        inputContent = request.args.get("inputContent")
        
        api_key = app.config['API_KEY']
        tmdb = TheMovieDB(api_key)
        
        if int(operationId) == 1:
            response = tmdb.search_movie_by_name(inputContent)
        elif int(operationId) == 2:
            try:
                genre_names = json.loads(inputContent)
                response = tmdb.get_movies_by_category(genre_names)
            except json.JSONDecodeError:
                return jsonify({"status": "400", "message": "Format de catégorie de genre invalide"}), 400
        elif int(operationId) == 3:
            response = tmdb.get_movies_by_year(inputContent)
        else:
            response = {
                "status": "404",
                "error": "Requête non reconnue par le serveur distant."
            }
            return jsonify(response), 404

        return response
    except Exception as e:
        return jsonify({
            "status": "500",
            "error": str(e)
        }), 500

@app.route('/api/themoviedb/get/movie', methods=['GET'])
def api_themoviedb_get_movie_details():
    try:
        movieId = request.args.get("movieId")
        
        api_key = app.config['API_KEY']
        tmdb = TheMovieDB(api_key)
        
        response = tmdb.get_movie_details_by_id(movieId)
        
        return response
    except Exception as e:
        return jsonify({
            "status": "500",
            "error": str(e)
        }), 500
    
    
    

