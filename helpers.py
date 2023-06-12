import secrets
import string

def read_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content

def generate_random_key(length):
    characters = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(characters) for _ in range(length))
    return key