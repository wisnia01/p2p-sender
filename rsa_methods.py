from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_rsa_keys():
    
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    return public_key, private_key

def encrypt_message_with_publickey(message, public_key):
    
    f = open('public_key.pem', 'rb')
    public_key = RSA.importKey(f.read())
    loaded_public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(loaded_public_key)
    ciphertext = cipher.encrypt(message)
    
    return ciphertext

def decrypt_message_with_privatekey(ciphertext, private_key):
    
    loaded_private_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(loaded_private_key)
    message = cipher.decrypt(ciphertext)
    
    return message
