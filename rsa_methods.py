from Crypto.PublicKey import RSA

def generate_rsa_keys():
    
    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    return public_key, private_key