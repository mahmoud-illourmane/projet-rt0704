import json # Pour la manipulation de fichiers JSON.
import os   # Pour les opérations sur le système de fichiers.
import uuid # Pour la génération d'identifiants uniques.

class User:
    """
        Cette classe représente un utilisateur dans un système d'authentification.

        Attributes:
            users_file_path (str): Le chemin vers le fichier JSON qui stocke les données des utilisateurs.

        Methods:
            __init__(self, email, password, first_name):
                Initialise un nouvel utilisateur avec un identifiant unique, une adresse e-mail,
                un mot de passe et un prénom.

            load_users(cls):
                Charge les utilisateurs à partir du fichier JSON et retourne un dictionnaire d'utilisateurs.

            email_exists(cls, email):
                Vérifie si l'adresse e-mail existe déjà parmi les utilisateurs enregistrés.

            save_user(cls, new_user):
                Enregistre un nouvel utilisateur dans le fichier JSON des utilisateurs.

            register(cls, email, password, first_name):
                Enregistre un nouvel utilisateur avec un identifiant unique, crée un fichier JSON associé
                et initialise les données de films pour cet utilisateur.

            authenticate_user(email, password):
                Authentifie un utilisateur en vérifiant l'e-mail et le mot de passe dans le fichier JSON des utilisateurs.

            delete_user(user_id):
                Supprime un utilisateur de la base de données des utilisateurs, ses données de films associées
                et les images de couverture associées à ses films.
    """
    
    users_file_path = 'storage/users.json'

    def __init__(self, email, password, first_name):
        """
            Initialise un nouvel utilisateur avec un identifiant unique, une adresse e-mail, un mot de passe et un prénom.

            Args:
                email (str): L'adresse e-mail de l'utilisateur.
                password (str): Le mot de passe de l'utilisateur.
                first_name (str): Le prénom de l'utilisateur.
        """
        
        self.id = str(uuid.uuid4())  # Génère un identifiant unique
        self.first_name = first_name
        self.email = email
        self.password = password

    @classmethod
    def load_users(cls):
        """
            Charge les utilisateurs à partir du fichier JSON et retourne un dictionnaire d'utilisateurs.

            Returns:
                dict: Un dictionnaire contenant les données des utilisateurs.
        """
        
        if not os.path.exists(cls.users_file_path):
            with open(cls.users_file_path, 'w') as file:
                json.dump({}, file)  # Initialise le fichier avec un objet JSON vide
            return {}

        with open(cls.users_file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Retourne un objet vide si le fichier JSON est mal formaté

    @classmethod
    def email_exists(cls, email):
        """
            Vérifie si l'adresse e-mail existe déjà parmi les utilisateurs enregistrés.

            Args:
                email (str): L'adresse e-mail à vérifier.

            Returns:
                bool: True si l'adresse e-mail existe déjà, False sinon.
        """
        
        users = cls.load_users()
        return any(user['email'] == email for user in users.values())

    @classmethod
    def save_user(cls, new_user):
        """
            Enregistre un nouvel utilisateur dans le fichier JSON des utilisateurs.

            Args:
                new_user (User): L'objet utilisateur à enregistrer.
        """
        
        users = cls.load_users()
        users[new_user.id] = {
            'first_name': new_user.first_name,
            'email': new_user.email,
            'password': new_user.password  # Le mot de passe en clair.
        }
        with open(cls.users_file_path, 'w') as file:
            json.dump(users, file, indent=4)

    @classmethod
    def register(cls, email, password, first_name):
        """
            Enregistre un nouvel utilisateur avec un identifiant unique, crée un fichier JSON associé
            et initialise les données de films pour cet utilisateur.

            Args:
                email (str): L'adresse e-mail de l'utilisateur.
                password (str): Le mot de passe de l'utilisateur.
                first_name (str): Le prénom de l'utilisateur.

            Returns:
                dict: Un dictionnaire de réponse indiquant le statut de l'enregistrement.
        """
        
        if cls.email_exists(email):
            return {
                'status': 409
            }

        new_user = cls(email, password, first_name)
        cls.save_user(new_user)

        # Crée un fichier JSON vide dans le répertoire "storage" avec le nom "movies_id.json"
        user_id = new_user.id
        file_name = os.path.join("storage", f"movies_{user_id}.json")
        data = {
            "nb_movies": 0,
            "movies": []
        }

        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return {
            'status': 201,
            'id': new_user.id,
            'first_name': new_user.first_name,
            'email': new_user.email
        }

    @staticmethod
    def authenticate_user(email, password):
        """
            Authentifie un utilisateur en vérifiant l'e-mail et le mot de passe dans le fichier JSON des utilisateurs.

            Args:
                email (str): L'adresse e-mail de l'utilisateur.
                password (str): Le mot de passe de l'utilisateur.

            Returns:
                dict: Un dictionnaire de réponse indiquant le statut de l'authentification et les informations de l'utilisateur.
        """
        
        users_file_path = 'storage/users.json'

        if os.path.exists(users_file_path):
            with open(users_file_path, 'r') as file:
                users = json.load(file)
                for user_id, user_data in users.items():
                    if user_data['email'] == email and user_data['password'] == password:
                        # Les identifiants sont corrects, retourner les informations de l'utilisateur
                        return {
                            'status': 200,
                            'id': user_id,
                            'first_name': user_data['first_name'],
                            'email': user_data['email']
                        }
        return {
            'status': 401,
            'error': 'Identifiants incorrects'
        }

    @staticmethod
    def delete_user(user_id):
        """
            Supprime un utilisateur de la base de données des utilisateurs, ses données de films associées
            et les images de couverture associées à ses films.

            Args:
                user_id (str): L'identifiant unique de l'utilisateur à supprimer.

            Returns:
                bool: True si la suppression a réussi, False sinon.
        """
        
        users_file_path = 'storage/users.json'

        # Supprimer l'utilisateur de users.json
        if os.path.exists(users_file_path):
            with open(users_file_path, 'r') as file:
                users = json.load(file)

            if user_id in users:
                del users[user_id]

                with open(users_file_path, 'w') as file:
                    json.dump(users, file, indent=4)
            else:
                return False

        # Supprimer le fichier movies_user_id.json
        movies_file_path = f'storage/movies_{user_id}.json'
        if os.path.exists(movies_file_path):
            os.remove(movies_file_path)

        # Supprimer les images de couverture associées
        covers_dir = 'storage/covers'
        if os.path.isdir(covers_dir):
            for filename in os.listdir(covers_dir):
                if filename.endswith(f'_{user_id}.jpg') or filename.endswith(f'_{user_id}.png') or filename.endswith(f'_{user_id}.webp') or filename.endswith(f'_{user_id}.jpeg'):
                    os.remove(os.path.join(covers_dir, filename))
        return True
