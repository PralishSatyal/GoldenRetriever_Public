from cryptography.fernet import Fernet
import json


"""Class to Encrypt or decrypt data"""
class SimpleCrypt:
    def __init__(self):
        self.key = Fernet.generate_key()  # We will need to save this key to use it for decryption
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt a plaintext string."""
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt an encrypted string."""
        return self.cipher.decrypt(ciphertext.encode()).decode()

"""Work in Progress Project Saver"""
class ProjectState:
    def __init__(self):
        # Initialize with some default state if required
        self.data = {
            "map_state": {},
            "slaves": [],
            "windows": []
        }

    def set_data(self, map_state, slaves, windows):
        self.data["map_state"] = map_state
        self.data["slaves"] = slaves
        self.data["windows"] = windows

    def save(self, filename="save_file.json"):
        with open(filename, "w") as file:
            json.dump(self.data, file)

    def load(self, filename="save_file.json"):
        with open(filename, "r") as file:
            self.data = json.load(file)
        return self.data

    # If you need to retrieve individual parts of the data:
    def get_map_state(self):
        return self.data["map_state"]

    def get_slaves(self):
        return self.data["slaves"]

    def get_windows(self):
        return self.data["windows"]

"""Function to read file data"""
def read_file(file_path):
    try:
        with open('login_details.txt', 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        # Handle the error, for example:
        raise Exception("Username file not found. Are you sure you're logged in?")
