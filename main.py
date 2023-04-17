from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


#AES Implementation
key = b'Sixteen byte key'
iv = b'This is an IV456'

plaintext = b'This is a secret message.'

def encrypt_ebc(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext, AES.block_size)
    print(padded_plaintext)
    print("dada")
    ciphertext = cipher.encrypt(padded_plaintext)

    return ciphertext

def decrypt_ebc(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext)
    print(padded_plaintext)
    plaintext = unpad(padded_plaintext, AES.block_size)

    return plaintext


def encrypt_cbc(plaintext, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)

    return iv, ciphertext

def decrypt_cbc(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)

    return plaintext

def main():
    print("start")
    print(decrypt_ebc(encrypt_ebc(plaintext, key),key))

    print("cbc now")
    iv, cipher = encrypt_cbc(plaintext, key)
    print(decrypt_cbc(cipher, key, iv))
    print("stop")

if __name__ == "__main__":
    main()