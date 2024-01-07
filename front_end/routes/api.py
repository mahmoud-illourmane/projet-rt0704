from app import app
from flask import request, jsonify
import requests, base64
from typing import Dict, Any

"""
|
|   This file contains all API routes that can be called to interact with the back-end.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 21, 2023
|
"""

# Accède à la variable globale depuis la configuration Flask
server_back_end_url = app.config['SERVER_BACK_END_URL']

@app.route('/api/get-movies/index', methods=['GET'])
def getMoviesIndex():
    """
        Summary:
            Cette route permet de récupérer la liste complète des films depuis une URL d'API sur le serveur back-end.

        Returns:
            JSON: Une réponse JSON contenant la liste des films récupérée depuis l'URL distante.

        Raises:
            requests.exceptions.RequestException: Si une erreur de requête se produit lors de la communication avec l'URL distante.

        HTTP Status Codes:
            - 200 OK: Si la liste des films est récupérée avec succès depuis l'URL distante.
            - Autres codes d'erreur HTTP : Si une erreur de requête se produit lors de la communication avec l'URL distante.
    """
    
    if request.method == 'GET':
        api_url = f"{server_back_end_url}/api/get-movies/index"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête vers l'URL distante : {e}")
            
            return jsonify({
                "status": "500", 
                "message": "Erreur de communication avec l'URL distante"
            }), 500
            
    return jsonify({
        "status": "error", 
        "error": "Method Not Allowed"
    }), 405

@app.route('/api/get-movies/gestions', methods=['GET'])
def getMoviesGestions():
    """
        Récupère tous les films pour l'affichage dans le modal "gestion des films".

        Cette route permet de récupérer la liste complète des films depuis une URL d'API sur le serveur back-end.
        
        Returns:
            JSON: Une réponse JSON contenant la liste des films récupérée depuis l'URL distante.

        Raises:
            requests.exceptions.RequestException: Si une erreur de requête se produit lors de la communication avec l'URL distante.

        HTTP Status Codes:
            - 200 OK: Si la liste des films est récupérée avec succès depuis l'URL distante.
            - Autres codes d'erreur HTTP : Si une erreur de requête se produit lors de la communication avec l'URL distante.
    """
    
    if request.method == 'GET':
        api_url = f"{server_back_end_url}/api/get-movies/gestions"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête vers l'URL distante : {e}")
            
            return jsonify({
                "status": "500", 
                "message": "Erreur de communication avec l'URL distante"
            }), 500
            
    return jsonify({
        "status": "error", 
        "error": "Method Not Allowed"
    }), 405
    
@app.route('/add-movie', methods=['POST'])
def add_movie():
    """
        Appelle la route API du back-end pour ajouter un nouveau film.

        Cette route permet à l'utilisateur d'ajouter un nouveau film en utilisant une requête POST.
        Elle prend en charge les données du formulaire, y compris les informations du film telles que le nom,
        l'année de création, le réalisateur, la catégorie, la synopsis, la notation et une éventuelle couverture d'image.
        Les données du film sont envoyées au back-end via une requête POST vers l'URL de l'API.

        Returns:
            JSON: Une réponse JSON renvoyée par l'API du back-end indiquant le statut de l'ajout du film.

        Raises:
            requests.exceptions.RequestException: Si une erreur de requête se produit lors de la communication avec l'API du back-end.

        HTTP Status Codes:
            - 200 OK: Si le film est ajouté avec succès.
            - 405 Method Not Allowed: Si la route est appelée avec une méthode autre que POST.
            - Autres codes d'erreur HTTP : Si une erreur de requête se produit lors de la communication avec l'API du back-end.
    """
    
    if request.method == 'POST':
        try:
            # Gestion de la couverture d'image du film
            cover_image = request.files.get('cover_image')
            if cover_image and cover_image.filename:
                image_data = cover_image.read()
                cover_image_base64 = base64.b64encode(image_data).decode('utf-8')
            else:
                # Indique que le film n'a pas de couverture
                cover_image_base64 = 'null'
            
            # Traitement des données du formulaire
            film_data = {
                'movie_name': request.form['movie_name'],
                'year_of_creation': request.form['year_of_creation'],
                'director': request.form['director'],
                'categorie': request.form['categorie'],
                'synopsis': request.form['synopsis'],
                'notation': request.form['notation'],
                'cover_image': cover_image_base64
            }
            
            api_url = f"{server_back_end_url}/api/add-movie"
            
            # Envoi des données au serveur en utilisant une requête POST
            response = requests.post(api_url, json=film_data)
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête vers l'API du back-end : {e}")
            
            return jsonify({
                "status": "500", 
                "message": "Erreur de communication avec l'API du back-end"
            }), 500
   
    response = {
        "status": "405",
        "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405

@app.route('/delete-movie', methods=['DELETE'])
def delete_movie() -> Dict[str, Any]:
    """
        Cette route appel la route API du back-end pour supprimer un film.
        
        Return
            Une réponse json
    """
    if request.method == 'DELETE':
        data = request.json
        movieId = data.get('movieId')
    
        # Url du serveur distant pour l'appel API 
        api_url = f"{server_back_end_url}/api/delete-movie"
        
        # Envoi les données au serveur en utilisant une requête POST
        response = requests.delete(api_url, json={"movieId": movieId})
        return response.json()
    response = {
        "status": "405",
        "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405

@app.route('/edit-movie/send', methods=['PATCH'])
def edit_movie() -> Dict[str, Any]:
    """
        Envoie une requête PATCH au serveur distant pour modifier les informations d'un film.

        Cette route permet à l'utilisateur de modifier les informations d'un film en utilisant une requête PATCH.
        Les données de modification sont envoyées au serveur distant via une requête PATCH vers l'URL de l'API du serveur distant.

        Returns:
            JSON: Une réponse JSON renvoyée par le serveur distant indiquant le statut de la modification des informations du film.

        Raises:
            Exception: Si une exception non gérée se produit lors de la communication avec le serveur distant.

        HTTP Status Codes:
            - 200 OK: Si les informations du film sont modifiées avec succès sur le serveur distant.
            - 403 Forbidden: Si la route est appelée avec une méthode autre que PATCH.
            - Autres codes d'erreur HTTP : Si une erreur se produit lors de la communication avec le serveur distant.
    """
    
    if request.method == 'PATCH':
        data = request.json
    
        api_url = f"{server_back_end_url}/api/edit-movie"
        
        try:
            # Envooi des données avec la requête PATCH
            response = requests.patch(api_url, json=data)
            
            # Vérifi si la réponse du serveur distant est réussie
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify(response.json())
        except Exception as e:
            return jsonify({
                "status": "500",
                "error": str(e)
            }), 500

    response = {
        "status": "405",
        "error": "Vous devez utiliser une requête POST pour cette route."
    }
    return jsonify(response), 405
    
#
#
#   API themoviedb
#
#

@app.route('/api/themoviedb/get', methods=['GET'])
def api_themoviedb_get():
    """
        Cette route permet d'interagir avec l'API themoviedb pour récupérer des films selon certains critères :
        Soit par le nom d'un film
        Soit par une ou plusieurs catégories de films
        Soit par une année de sortie d'un film
        
    Returns:
        _type_: JSON, les films retournés ou rien
    """
    
    if request.method == 'GET':
        operationId = request.args.get('operationId')
        inputContent = request.args.get('searchInputValue')
        data = {
            "operationId": operationId,
            "inputContent": inputContent
        }
        
        api_url = f"{server_back_end_url}/api/themoviedb/get"
        
        try:
            # envoi les données au serveur en utilisant une requête PATCH
            response = requests.get(api_url, params=data)
            
            # Vérifie si la réponse du serveur distant est réussie
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify(response.json())
        except Exception as e:
            return jsonify({
                "status": "500",
                "error": str(e)
            }), 500

    return jsonify({
        "status": "405",
        "error": "Vous devez utiliser une requête GET pour cette route."
    })
    
@app.route('/api/themoviedb/get/movie', methods=['GET'])
def api_themoviedb_get_movie_details():
    if request.method == 'GET':
        movieId = request.args.get('movieId')

        data = {
            "movieId": movieId
        }
        
        api_url = f"{server_back_end_url}/api/themoviedb/get/movie"
        
        try:
            # envoi les données au serveur en utilisant une requête PATCH
            response = requests.get(api_url, params=data)
            
            # Vérifie si la réponse du serveur distant est réussie
            if response.status_code == 200:
                return response.json()
            
        except Exception as e:
            return jsonify({
                "status": "500",
                "error": str(e)
            }), 500
            
    return jsonify({
        "status": "405",
        "error": "Vous devez utiliser une requête GET pour cette route."
    })
    
@app.route('/api/themoviedb/get/fast-search', methods=['GET'])
def api_themoviedb_get_fast_search():
    if request.method == 'GET':
        operationId = int(request.args.get('operationId'))
        if operationId not in [1, 2, 3]:
            return jsonify({
                "status": "422",
                "error": "Le choix n'est pas reconnu."
            }), 422
        
        data = {
            "operationId": operationId
        }
        
        api_url = f"{server_back_end_url}/api/themoviedb/get/fast-search"
        
        try:
            # envoi les données au serveur en utilisant une requête PATCH
            response = requests.get(api_url, params=data)
            
            # Vérifie si la réponse du serveur distant est réussie
            if response.status_code == 200:
                return response.json()
            
        except Exception as e:
            return jsonify({
                "status": "500",
                "error": str(e)
            }), 500
            
    return jsonify({
        "status": "405",
        "error": "Vous devez utiliser une requête GET pour cette route."
    }), 405
