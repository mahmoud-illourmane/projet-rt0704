from __future__ import annotations
from flask import jsonify           # Permet d'utiliser le nom de la classe en tant que type dans les annotations de type
import requests, datetime

"""
|
|   Author Mahmoud ILLOURMANE
|   DATE 12-22-23 US DATE
|
"""

class TheMovieDB:
    """
    Classe pour interagir avec l'API de TheMovieDB.

    Attributes:
        api_key (str): La clé d'API pour accéder à l'API de TheMovieDB.
        base_url (str): L'URL de base de l'API de TheMovieDB.
        language (str): La langue des réponses de l'API (par défaut en français).

    Class Attributes:
        key_mapping (dict): Mapping des clés de données de l'API aux noms de clés souhaités.
        genre_id_to_name (dict): Mapping des IDs de genre aux noms de genre correspondants.

    Methods:
        extract_movie_data(api_response): Extrait les données de films à partir d'une réponse de l'API.
        extract_movie_data_by_movie_id(api_response): Extrait les données d'un film à partir d'une réponse de l'API.
        search_movie_by_name(movie_name): Recherche des films par nom.
        get_movies_by_category(genre_names): Récupère des films par catégorie de genre.
        get_movies_by_year(year): Récupère des films par année de sortie.
        get_api_response(endpoint, params): Effectue une requête à l'API et renvoie la réponse.

    """
    
    # Mapping des clés de données de l'API aux noms de clés souhaités
    key_mapping = {
        'id': 'id',
        'runtime': 'runtime', 
        'original_title': 'title',
        'genre_ids': 'genres',
        'vote_average': 'user_rating',
        'overview': 'synopsis',
        'release_date': 'release_date',
        'poster_path': 'cover_photo',
        'backdrop_path': 'background_image',
        'creators': 'creators',
        'genres': 'genres'
    }

    genre_id_to_name = {
        28: 'Action',
        12: 'Aventure',
        16: 'Animation',
        35: 'Comedie',
        18: 'Drame',
        878: 'Science-fiction',
        27: 'Horreur',
        14: 'Fantaisie',
        53: 'Thriller',
        10749: 'Romance',
        99: 'Documentaire',
        80: 'Crime',
        9648: 'Mystere',
        10752: 'Guerre',
        36: 'Historique',
        10402: 'Musique',
        10751: 'Familial',
        10770: 'Sport',
        100: 'Biographie',
        37: 'Western'
    }

    def __init__(self, api_key):
        """
            Initialise une instance de la classe TheMovieDB.

        Args:
            api_key (str): La clé d'API pour accéder à l'API de TheMovieDB.
        """
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.language = "fr-FR"
    
    """
    |
    |   Méthodes de classe
    |
    """
    
    def get_api_response(self, endpoint, params):
        """
                Effectue une requête à l'API et renvoie la réponse.

            Args:
                endpoint (str): L'endpoint de l'API à interroger.
                params (dict): Les paramètres de requête à inclure dans la requête.

            Returns:
                dict: La réponse de l'API sous forme de dictionnaire.
        """
        try:
            params["api_key"] = self.api_key
            params["language"] = self.language
            if "id" in params:                                                                      # Si l'utilisateur souhaite avoir les détails sur un film je dois modifier un peu la requête pour quelle soit correcte.
                response = requests.get(self.base_url + endpoint + params["id"], params=params)
            else:                                                                                   # Pour les autres requête ça sera la meme chose
                response = requests.get(self.base_url + endpoint, params=params)
            response.raise_for_status()                                                             # Lève une exception si la requête échoue (par exemple, une erreur HTTP)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête : {e}")
            response = {
                "status": "500",
                "message": "Erreur serveur distant"
            }
            return response
        
    def extract_movie_data(self, api_response):
        """
        Extrait les données de films à partir d'une réponse de l'API.

        Args:
            api_response (dict): La réponse de l'API contenant les données de films.

        Returns:
            list: Une liste de dictionnaires contenant les données extraites des films.
        """
        
        extracted_data = []                                                                         
        if 'results' in api_response:                                                               # Vérifie si la clé 'results' existe dans la réponse de l'API
            for movie_data in api_response['results']:                                              
                extracted_movie = {}                                                                # Initialise un dictionnaire pour stocker les données extraites du film actuel
                for original_key, new_key in self.key_mapping.items():                              # Parcourt chaque paire clé originale / nouvelle clé
                    if original_key == 'genre_ids':                                                 
                        genre_ids = movie_data.get(original_key, [])                                # Obtient les IDs de genre du film actuel (peut être une liste vide)
                        genres = [self.genre_id_to_name.get(genre_id) for genre_id in genre_ids]    # Mappe les IDs de genre aux noms de genre
                        extracted_movie[new_key] = genres                                           # Stocke les noms de genre dans la nouvelle clé du dictionnaire extrait
                    elif original_key in movie_data:                                                # Si la clé originale existe dans les données du film actuel
                        extracted_movie[new_key] = movie_data[original_key]                         # Copie la valeur correspondante dans la nouvelle clé du dictionnaire extrait
                extracted_data.append(extracted_movie)                                              
        return extracted_data    
    
    def extract_movie_data_by_movie_id(self, api_response):
        """
        Extrait les données d'un film à partir d'une réponse de l'API.

        Args:
            api_response (dict): La réponse de l'API contenant les données détaillé d'un film.

        Returns:
            dict: Un dictionnaire contenant les données extraites du film.
        """
        
        extracted_movie = {}  # Initialise un dictionnaire pour stocker les données extraites
        for original_key, new_key in self.key_mapping.items():
            if original_key in api_response:
                extracted_movie[new_key] = api_response[original_key]
        return extracted_movie
    
    def get_genre_ids(self, genre_names):
        """
            Obtient les identifiants des genres de films correspondant aux noms fournis.

            :param genre_names: Liste des noms de genres de films en minuscules.
            :type genre_names: list[str]

            :return: Liste des identifiants correspondants des genres de films trouvés.
            :rtype: list[int]

            Cette fonction parcourt la correspondance entre les noms de genres et leurs identifiants
            stockés dans le dictionnaire self.genre_id_to_name. Elle renvoie une liste des identifiants
            correspondants des genres de films trouvés dans genre_names.

            Si un nom de genre ne correspond à aucun identifiant, un message d'erreur est affiché, mais
            la recherche des autres genres se poursuit.

            Args:
                genre_names (list[str]): La liste des noms de genres de films à rechercher.

            Returns:
                list[int]: La liste des identifiants correspondants des genres de films trouvés.
        """
        genre_ids = []                                              # Initialise une liste pour stocker les identifiants des genres trouvés
        for name in genre_names:  
            found = False  
            for id, genre_name in self.genre_id_to_name.items():    # Parcourt chaque paire id/nom de genre dans self.genre_id_to_name
                if genre_name.lower() == name.lower():  
                    genre_ids.append(id) 
                    found = True                                    # Marque que le genre a été trouvé
                    break
            if not found: 
                print(f"Genre non trouvé : {name}")  
        return genre_ids
    
    """
    |
    |   Méthodes appelées par l'api REST.
    |
    """
    
    def search_movie_by_name(self, movie_name):
        """
            Recherche des films par nom.

            Args:
                movie_name (str): Le nom du film à rechercher.

            Returns:
                list: Une liste de dictionnaires contenant les données des films correspondants à la recherche.
        """
        
        try:
            api_response = self.get_api_response("/search/movie", {"query": movie_name})
            if api_response:
                response = {
                    "status": "200",
                    "message": "Données reçues",
                    "data": self.extract_movie_data(api_response)
                }
                return jsonify(response), 200
            else:
                response = {
                    "status": "404",
                    "message": "Aucun résultat trouvé"
                }
                return jsonify(response), 404
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            response = {
                "status": "500",
                "message": "Erreur serveur distant"
            }
            return jsonify(response), 500

    def get_movies_by_category(self, genre_names):
        """
            Récupère les films correspondant aux catégories de genre spécifiées.

            Args:
                genre_names (list[str]): Liste des noms de genres de films en minuscules à rechercher.

            Returns:
                dict: Un dictionnaire contenant les résultats de la requête.
                    - "status" (str): Le code de statut de la réponse.
                    - "message" (str): Un message décrivant le résultat de la requête.
                    - "data" (list): Une liste de dictionnaires contenant les données extraites des films correspondant aux genres spécifiés.
        """
        
        try:
            genre_ids = self.get_genre_ids(genre_names)
            
            if genre_ids:
                genre_ids_str = ','.join(map(str, genre_ids)) # Convertir la liste des identifiants en une chaîne séparée par des virgules
                params = {"with_genres": genre_ids_str}
                api_response = self.get_api_response("/discover/movie", params)

                if api_response:
                    response = {
                        "status": "200",
                        "message": "Données reçues",
                        "data": self.extract_movie_data(api_response)
                    }
                    return jsonify(response), 200
                else:
                    response = {
                        "status": "404",
                        "message": "Aucun résultat trouvé"
                    }
                    return jsonify(response), 404
            else:
                response = {
                    "status": "400",
                    "message": "Catégorie de genre invalide"
                }
                return jsonify(response), 400
            
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            response = {
                "status": "500",
                "message": "Erreur serveur distant"
            }
            return jsonify(response), 500

    def get_movies_by_year(self, year):
        """
            Récupère des films par année de sortie.

            Args:
                year (int): L'année de sortie des films à récupérer.

            Returns:
                list: Une liste de dictionnaires contenant les données des films correspondants à l'année donnée.
        """
        
        try:
            params = {"primary_release_year": year}
            api_response = self.get_api_response("/discover/movie", params)
            if api_response:
                response = {
                    "status": "200",
                    "message": "Données reçues",
                    "data": self.extract_movie_data(api_response)
                }
                return jsonify(response), 200
            else:
                response = {
                    "status": "404",
                    "message": "Aucun résultat trouvé"
                }
                return jsonify(response), 404
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            response = {
                "status": "500",
                "message": "Erreur serveur distant"
            }
            return jsonify(response), 500

    def get_movie_details_by_id(self, movie_id):
        """
            Summary:
                Récupère les détails d'un film en utilisant son ID.

            Args:
                movie_id (int): L'ID du film que l'utilisateur souhaite récupérer.

            Returns:
                dict: Un dictionnaire contenant les détails complets du film.
        """
        
        try:
            # Paramètre à mettre dans la requête API
            params = {"id": movie_id}
            # Le endPoint de la requête
            endPoint = "/movie/"
            
            # Appel à la méthode de classe pour effectuer la requête API avec les paramètres indiqués plus haut
            api_response = self.get_api_response(endPoint, params)    
            
            if api_response:
                data_extracted = self.extract_movie_data_by_movie_id(api_response)
                
                response = {
                    "status": "200",
                    "message": "Données envoyés avec succès",
                    "data": self.extract_movie_data_by_movie_id(api_response)
                }
                
                return jsonify(response), 200
            else:
                response = {
                    "status": "404",
                    "error": "Aucun résultat trouvé"
                }
            return jsonify(response), 404
        except Exception as e:
            print(f"Erreur inattendue 65 : {e}")
            response = {
                "status": "500",
                "error": "Erreur serveur distant"
            }
            return jsonify(response), 500

    def get_movies_horror(self):
        """
            Retourne les films français.
        """
        
        params = {
            "with_genres": "27",
        }
        
        endPoint = "/discover/movie"
            
        try:
            api_response = self.get_api_response(endPoint, params)    
    
            if api_response:
                extracted_data = self.extract_movie_data(api_response)
   
                response = {
                    "status": "200",
                    "message": "Voici les derniers films français.",
                    "data": extracted_data
                }
                
                return jsonify(response), 200
            else:
                response = {
                    "status": "404",
                    "error": "Aucun résultat trouvé"
                }
            return jsonify(response), 404
        
        except Exception as e:
            print(f"Erreur inattendue 65 : {e}")
            response = {
                "status": "500",
                "error": "Erreur serveur distant"
            }
            return jsonify(response), 500
      
    def get_movies_by_popularity(self):
        """
            Retournes les films les plus populaires
        """
        
        params = {
            "sort_by": "popularity.desc",
        }
        
        endPoint = "/discover/movie"
            
        try:
            api_response = self.get_api_response(endPoint, params)    
    
            if api_response:
                extracted_data = self.extract_movie_data(api_response)
   
                response = {
                    "status": "200",
                    "message": "Voici les derniers films français.",
                    "data": extracted_data
                }
                
                return jsonify(response), 200
            else:
                response = {
                    "status": "404",
                    "error": "Aucun résultat trouvé"
                }
            return jsonify(response), 404
        
        except Exception as e:
            print(f"Erreur inattendue 65 : {e}")
            response = {
                "status": "500",
                "error": "Erreur serveur distant"
            }
            return jsonify(response), 500
        
    def get_movies_now_playing(self):
        """
            Récupère les films actuellement en salle.
        """
        
        # Calcul des dates pour la plage souhaitée
        date_actuelle = datetime.datetime.now()
        date_debut = datetime.datetime(date_actuelle.year, 1, 1)
        date_fin = datetime.datetime(date_actuelle.year, 12, 31)

        # Formatage des dates au format YYYY-MM-DD
        date_debut_formattee = date_debut.strftime('%Y-%m-%d')
        date_fin_formattee = date_fin.strftime('%Y-%m-%d')
        params = {
            'release_date.gte': date_debut_formattee,
            'release_date.lte': date_fin_formattee,
            'sort_by': 'release_date.desc'
        }
        
        # Le endPoint de la requête
        endPoint = "/movie/now_playing"
            
        try:
            # Appel à la méthode de classe pour effectuer la requête API avec le paramètre indiqué plus haut
            api_response = self.get_api_response(endPoint, params)    
    
            if api_response:
                extracted_data = self.extract_movie_data(api_response)
   
                response = {
                    "status": "200",
                    "message": "Voici les derniers films français.",
                    "data": extracted_data
                }
                
                return jsonify(response), 200
            else:
                response = {
                    "status": "404",
                    "error": "Aucun résultat trouvé"
                }
            return jsonify(response), 404
        
        except Exception as e:
            print(f"Erreur inattendue 65 : {e}")
            response = {
                "status": "500",
                "error": "Erreur serveur distant"
            }
            return jsonify(response), 500