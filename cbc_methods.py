from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_cbc(plaintext, key):
    b_plaintext = plaintext.encode('latin-1')
    b_key = key.encode('latin-1')
    
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(b_key, AES.MODE_CBC, iv)
    padded_plaintext = pad(b_plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)

    return iv.decode('latin-1'), ciphertext.decode('latin-1')

def decrypt_cbc(ciphertext, key, iv):
    b_ciphertext = ciphertext.encode('latin-1')
    b_key = key.encode('latin-1')
    b_iv = iv.encode('latin-1')
    
    cipher = AES.new(b_key, AES.MODE_CBC, b_iv)
    padded_plaintext = cipher.decrypt(b_ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)

    return plaintext.decode('latin-1')