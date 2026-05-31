# utils/crypto_master.py
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

        if meta_file.exists():
            return False

        key = Fernet.generate_key()
        cipher = Fernet(key)

        encrypted_password = cipher.encrypt(password.encode())
        
        auth_data = {
            'key': key.decode(),
            'password': encrypted_password.decode()
        }
        
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(auth_data, f, indent=2)

        return True

    
    def check_password(self, username, password):
        user_folder = self.users_folder / username
        meta_file = user_folder / 'meta.json'

        with open(meta_file, 'r', encoding='utf-8') as f:
            meta_data = json.load(f)
        
        key = meta_data['key'].encode()
        cipher = Fernet(key)
        stored_password = cipher.decrypt(meta_data['password'].encode()).decode()
        
        return stored_password == password

cm = CryptoMaster()