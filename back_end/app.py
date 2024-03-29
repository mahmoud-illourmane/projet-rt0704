"""
|
|   This file encompasses all configuration settings for the back-end functionality of this application.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 20, 2023
|
"""

# Importation des packages nécessaires au bon fonctionnement du projet Flask
from flask import Flask

"""
|
| App Configurations
|
"""

app = Flask(__name__)

# Activation du mode de débogage
app.debug = True

# Importation du fichier api.py
from routes.api import *

# Importation de la classe Movie
from src.classes.movie import Movie

# Clé api de theMovieDB
app.config['API_KEY'] = 'xx'

if __name__ == '__main__':
    # En VM
    # app.run(host='0.0.0.0', port=5000)
    
    # En Local
    app.run(host='0.0.0.0', port=5001)
