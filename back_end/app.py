"""
|
|   This file contains all the configuration settings for the back-end of this application.
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

app.config['API_KEY'] = '0a40109164d6a67baadc4a7993451212'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
