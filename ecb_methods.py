from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_ecb(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext, AES.block_size)
    print(padded_plaintext)
    print("dada")
    ciphertext = cipher.encrypt(padded_plaintext)

    return ciphertext

def decrypt_ecb(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext)
    print(padded_plaintext)
    plaintext = unpad(padded_plaintext, AES.block_size)

    return plaintext