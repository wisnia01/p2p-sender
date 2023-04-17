from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


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


def main():
    print("start")
    print(decrypt_ebc(encrypt_ebc(plaintext, key),key))
    print("stop")

if __name__ == "__main__":
    main()