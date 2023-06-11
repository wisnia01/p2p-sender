from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate the key pair
key = RSA.generate(2048)

# Get the public and private keys
public_key = key.publickey().export_key()
private_key = key.export_key()

print(public_key)
# Save the keys to files
with open('public_key.pem', 'wb') as f:
    f.write(public_key)

with open('private_key.pem', 'wb') as f:
    f.write(private_key)

# Encrypt the plaintext message using the public key
plaintext = b'This is a secret message.'
public_key = RSA.import_key(public_key)
cipher_rsa = PKCS1_OAEP.new(public_key)
ciphertext = cipher_rsa.encrypt(plaintext)

print('Ciphertext:', ciphertext)