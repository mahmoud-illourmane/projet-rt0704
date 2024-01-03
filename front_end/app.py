"""
|
|   This file contains all configuration for the front-end of this application.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 15, 2023
|
"""

"""
|
| App Configurations
|
"""
from flask import Flask

app = Flask(__name__)

# Activation du mode de débogage
app.debug = True

# Configuration du serveur pour reload le contenu des pages web
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Importations des fichier web.py et api.py
from routes.api import *
from routes.web import *

# Configuration de l'url du serveur flask back-end
app.config['SERVER_BACK_END_URL'] = 'http://127.0.0.1:5001'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
