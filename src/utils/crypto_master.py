import os
import json
from pathlib import Path
from cryptography.fernet import Fernet

BASE_DIR = Path(__file__).parent.parent
USERS_FOLDER_PATH = BASE_DIR / "users"

class CryptoMaster:
    def __init__(self):
        self.users_folder = USERS_FOLDER_PATH
        self.users_folder.mkdir(parents=True, exist_ok=True)
    
    def create_user(self, username, password):
        user_folder = self.users_folder / username
        meta_file = user_folder / 'meta.json'

        if not user_folder.exists():
            user_folder.mkdir(parents=True)
        
        try:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            
            encrypted_password = cipher.encrypt(password.encode())

            meta_data = {
                'key': key.decode(),
                'password': encrypted_password.decode()
            }
            
            with open(meta_file, 'w', encoding='utf-8') as file:
                json.dump(meta_data, file, indent=2)
            
            return True
            
        except Exception:
            return False
    
    def check_password(self, username, password):
        user_folder = self.users_folder / username
        meta_file = user_folder / 'meta.json'
        
        try:
            with open(meta_file, 'r', encoding='utf-8') as file:
                auth_data = json.load(file)
            
            key = auth_data['key'].encode()
            cipher = Fernet(key)
            stored_password = cipher.decrypt(auth_data['password'].encode()).decode()
            
            return stored_password == password
            
        except Exception:
            return False

cm = CryptoMaster()