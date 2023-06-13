from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_ecb(plaintext, key):
    b_plaintext = plaintext.encode('latin-1')
    b_key = key.encode('latin-1')
    
    cipher = AES.new(b_key, AES.MODE_ECB)
    padded_plaintext = pad(b_plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)

    return ciphertext.decode('latin-1')

def decrypt_ecb(ciphertext, key):
    b_ciphertext = ciphertext.encode('latin-1')
    b_key = key.encode('latin-1')
    
    cipher = AES.new(b_key, AES.MODE_ECB)
    padded_plaintext = cipher.decrypt(b_ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)

    return plaintext.decode('latin-1')