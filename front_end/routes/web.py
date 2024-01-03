from flask import render_template, request, abort
from app import app
from datetime import datetime

"""
|   This file contains all the routes for the frontend of this application.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 15, 2023
"""

@app.route('/', methods=['GET'])
def index():
    """
        Affiche la page d'accueil de l'application.

        Cette route renvoie une vue HTML représentant la page d'accueil de l'application.

        Returns:
            str: Une vue HTML de la page d'accueil.
    """
    if request.method == 'GET':
        return render_template('index.html')
    abort(405)
    
@app.route('/edit-movie/<int:movie_id>', methods=['GET'])
def editMovie(movie_id):
    """
        Affiche le formulaire d'édition pour un film spécifique.

        Cette route gère une demande GET pour afficher le formulaire d'édition d'un film avec des données pré-remplies.

        Args:
            movie_id (int): L'identifiant unique du film à éditer.

        Returns:
            str: Une vue HTML représentant le formulaire d'édition du film.
    """
    
    if request.method == 'GET':
        name = request.args.get('name')
        year = request.args.get('year')
        director = request.args.get('director')
        synopsis = request.args.get('synopsis')
        category = request.args.get('category')
        rating = request.args.get('rating')

        movie_data = {
            'id': movie_id,
            'name': name,
            'year': year,
            'director': director,
            'category': category,
            'synopsis': synopsis,
            'rating': rating
        }

        return render_template('videotheque/edit-movie.html', movie=movie_data)
    abort(405)

@app.route('/show-movie', methods=['POST'])
def showMovie():
    """
        Affiche les détails d'un film.

        Cette route gère une demande POST contenant des données sur un film, puis affiche les détails de ce film
        à l'aide d'une vue HTML.

        Args:
            None (utilise les données de la demande POST)

        Returns:
            str: Une vue HTML représentant les détails du film.
    """

    if request.method == 'POST':
        movie_id = request.form.get('movieId')
        category = request.form.get('category')
        movie_name = request.form.get('movieName')
        year = request.form.get('year')
        director = request.form.get('director')
        synopsis = request.form.get('synopsis')
        notation = request.form.get('notation')
        image64 = request.form.get('image64')

        movie_data = {
            'id': movie_id,
            'category': category,
            'movie_name': movie_name,
            'year': year,
            'director': director,
            'synopsis': synopsis,
            'notation': notation,
            'image64': image64
        }

        return render_template('videotheque/show-movie.html', movie=movie_data)
    abort(405)
    
#
#
#   API themoviedb
#
#

@app.route('/themoviedb', methods=['GET'])
def themoviedb():
    """
        Affiche la page d'accueil pour utiliser l'API The Movie Database.

        Cette route renvoie une vue HTML qui permet aux utilisateurs d'accéder à l'API The Movie Database
        pour obtenir des informations sur les films et les séries.

        Returns:
            str: Une vue HTML représentant la page d'accueil de l'API The Movie Database.
    """
    if request.method == 'GET':
        return render_template('themoviedb/themoviedb-index.html')
    abort(405)
    
@app.route('/show-movie-themoviedb', methods=['POST'])
def showMovie_themoviedb():
    """
        Affiche les détails d'un film de l'API The Movie Database.

        Cette route gère une demande POST contenant des données sur un film, puis affiche les détails de ce film
        à l'aide d'une vue HTML.

        Args:
            None (utilise les données de la demande POST)

        Returns:
            str: Une vue HTML représentant les détails du film de l'API The Movie Database.
    """

    if request.method == 'POST':
        movieName = request.form.get('movieName')
        movieCategory = request.form.get('movieCategory')
        movieRelease_str = request.form.get('movieRelease')
        movieRelease = datetime.strptime(movieRelease_str, '%Y-%m-%d')
        movieNotation = request.form.get('movieNotation')
        movieSynopsis = request.form.get('movieSynopsis')
        movieCover = request.form.get('movieCover')
        
        movie_data = {
            'title': movieName,
            'category': movieCategory,
            'release': movieRelease,
            'notation': float(movieNotation),
            'synopsis': movieSynopsis,
            'cover': movieCover
        }

        return render_template('themoviedb/show-themovie-db.html', movie=movie_data)
    abort(405)
    
@app.route('/show-movie-themoviedb/details', methods=['POST'])
def show_movie_details_themoviedb():
    if request.method == 'POST':
        # Récupération des données depuis le formulaire
        movie_data = {
            'title': request.form.get('movieName'),
            'category': request.form.get('movieCategory'),
            'release': datetime.strptime(request.form.get('movieRelease'), '%Y-%m-%d'),
            'runtime': f"{int(request.form.get('runtime')) // 60}h {int(request.form.get('runtime')) % 60}min",
            'notation': float(request.form.get('movieNotation')),
            'synopsis': request.form.get('movieSynopsis'),
            'cover': f"https://image.tmdb.org/t/p/w400{request.form.get('movieCover')}" if request.form.get('movieCover') else None,
            'movieBackgroundImage': f"https://image.tmdb.org/t/p/w500{request.form.get('backgroundImage')}" if request.form.get('backgroundImage') else None
        }
        
        return render_template('themoviedb/show-movie-details.html', movie=movie_data)
    
    # Si la méthode HTTP n'est pas POST, retourner une erreur 405
    abort(405)
