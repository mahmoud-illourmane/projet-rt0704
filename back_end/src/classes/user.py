import json
import os
import uuid

class User:
    
    users_file_path = 'storage/users.json'

    def __init__(self, email, password, first_name):
        self.id = str(uuid.uuid4())  # Génère un identifiant unique
        self.first_name = first_name
        self.email = email
        self.password = password

    @classmethod
    def load_users(cls):
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
        users = cls.load_users()
        return any(user['email'] == email for user in users.values())
    
    @classmethod
    def save_user(cls, new_user):
        users = cls.load_users()
        users[new_user.id] = {
            'first_name': new_user.first_name,
            'email': new_user.email,
            'password': new_user.password  # Attention : stocker le mot de passe en clair n'est pas sécurisé
        }
        with open(cls.users_file_path, 'w') as file:
            json.dump(users, file, indent=4)

    @classmethod
    def register(cls, email, password, first_name):
        if cls.email_exists(email):
            return {
                'status': 409
            }

        new_user = cls(email, password, first_name)
        cls.save_user(new_user)
        return {
            'status': 201,
            'id': new_user.id,
            'first_name': new_user.first_name,
            'email': new_user.email
        }
    
    @staticmethod
    def authenticate_user(email, password):
        users_file_path = 'storage/users.json'
        
        if os.path.exists(users_file_path):
            with open(users_file_path, 'r') as file:
                users = json.load(file)
                for user_id, user_data in users.items():
                    if user_data['email'] == email and user_data['password'] == password:
                        # Les identifiants sont corrects, retournez les informations de l'utilisateur
                        return {
                            'status': 200,
                            'id': user_id,
                            'first_name': user_data['first_name'],
                            'email': user_data['email']
                        }
        return {
            'status': 401,
            'id': user_id,
            'first_name': user_data['first_name'],
            'email': user_data['email']
        }
