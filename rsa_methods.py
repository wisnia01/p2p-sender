from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_rsa_keys():
    
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    return public_key, private_key

def encrypt_message_with_publickey(message, public_key):
    
    loaded_public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(loaded_public_key)
    ciphertext = cipher.encrypt(message.encode('latin-1'))
    ciphertext_to_string = base64.b64encode(ciphertext).decode('latin-1')

    return ciphertext_to_string

def decrypt_message_with_privatekey(ciphertext_to_string, private_key):
    
    ciphertext = base64.b64decode(ciphertext_to_string.encode('latin-1'))
    loaded_private_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(loaded_private_key)
    message = cipher.decrypt(ciphertext)
    
    return message.decode('latin-1')