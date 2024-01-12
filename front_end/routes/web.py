from app import app
from datetime import datetime
import requests
from flask import render_template, request, abort, redirect, url_for, flash, session

from flask_login import LoginManager, login_user, login_required, logout_user
import json

from src.classes.user import User  

# Accède à la variable globale depuis la configuration Flask
server_front_end_url = app.config['SERVER_FRONT_END_URL']

"""
|   This file contains all the routes for the frontend of this application.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 15, 2023
"""

# Initialisation de LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#
#   Authentification
#

# Rechargement de l'utilisateur
@login_manager.user_loader
def load_user(user_id):
    user_info = session.get('user_info')
    if user_info and user_id == user_info.get('id'):
        return User(user_id, user_info.get('first_name'), user_info.get('email'))
    return None


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    """
    Summary:
        Cette route renvoie une vue HTML permettant de s'inscrire.
        Elle gère également le processus d'inscription.

    Returns:
            str: Une vue HTML.
    """
    
    if request.method == 'GET':
        return render_template('signIn-signUp/sigUp.html')
    
    elif request.method == 'POST':
        firstName = request.form['firstName']
        email = request.form['email']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']
        
        # Vérifie si les mots de passe correspondent
        if password != passwordConfirm:
            flash('Les mots de passe ne correspondent pas. Veuillez réessayer.')
            return redirect(url_for('signUp')) 
        
        # Je forge les données de la requête pour le fichier api.py du serveur front 
        # Ce n'est pas idéal..
        data = {
            "firstName": firstName,
            "email": email,
            "password": password
        }
        # Convertir le dictionnaire en une chaîne JSON
        user_data = json.dumps(data)
        # Spécification de l'en-tête "Content-Type" pour indiquer que vous envoyez du JSON
        headers = {'Content-Type': 'application/json'}
        api_url = f"{server_front_end_url}/api/signUp"
        
        try:
            response = requests.post(api_url, data=user_data, headers=headers)
            response.raise_for_status()
            
            # if response.status_code == 201:
            #     response_data = response.json()
                
            #     print('DONNES :', response_data.get('first_name'), response_data.get('id'), response_data.get('email'))
            #     first_name = response_data.get('first_name')
            #     id = response_data.get('id')
            #     email = response_data.get('email')
            #     user = User(id, first_name, email)
            #     login_user(user)
            #     return redirect(url_for('index'))
            
            #     print("La requête a réussi (statut 201).")
                
            #     # Pour afficher le message contenu dans la réponse JSON
                
            #     message = response_data.get('message')
            #     print(f"Message du serveur : {message}")
            #     flash(message)
            #     return redirect(url_for('login')) 
            
            if response.status_code == 201:
                response_data = response.json()
                user = User(response_data.get('id'), response_data.get('first_name'), response_data.get('email'))
                login_user(user)
                # Stocker les informations dans la session
                session['user_info'] = {'id': user.id, 'first_name': user.first_name, 'email': user.email}
                return redirect(url_for('index'))
            elif response.status_code == 409:
                flash("L'email est déjà utilisé.")
                return redirect(url_for('signUp')) 
            else:
                flash("Une erreur s'est produite web.py.")
                return redirect(url_for('signUp')) 
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur de requête vers l'URL distante : {str(e)}"
            flash(error_message)
            return redirect(url_for('signUp')) 
    abort(405)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ici, envoie la requête à l'API du serveur back-end
        username = request.form['username']
        password = request.form['password']
        response = requests.post('http://adresse_du_serveur_backend/login', json={'username': username, 'password': password})

        if response.status_code == 200:
            user_data = response.json()
            if user_data['auth']:
                user = User(user_data['user_id'])
                login_user(user)
                return redirect(url_for('protected_route'))
        return 'Échec de la connexion'

    return render_template('signIn-signUp/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Au revoir !")
    return redirect(url_for('login'))

#
#   Application Web
#

@app.route('/', methods=['GET'])
@login_required
def index():
    """
    Summary:
        Cette route renvoie une vue HTML représentant la page d'accueil de l'application.

    Returns:
            str: Une vue HTML de la page d'accueil.
    """
    if request.method == 'GET':
        return render_template('index.html')
    abort(405)
    
@app.route('/edit-movie/<int:movie_id>', methods=['GET'])
@login_required
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

        return render_template('videotheque/views/edit-movie.html', movie=movie_data)
    abort(405)

@app.route('/show-movie', methods=['POST'])
@login_required
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

        return render_template('videotheque/views/show-movie.html', movie=movie_data)
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
        return render_template('themoviedb/views/themoviedb-index.html')
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
        
        return render_template('themoviedb/views/show-movie-details.html', movie=movie_data)
    
    # Si la méthode HTTP n'est pas POST, retourner une erreur 405
    abort(405)
