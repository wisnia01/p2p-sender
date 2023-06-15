import secrets
import string

def read_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        content = f.read()
    return content

def save_file(output_file_path, file):
    with open(output_file_path, 'wb') as f:
        f.write(file.encode('latin-1'))

def generate_random_key(length):
    characters = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(characters) for _ in range(length))
    return key