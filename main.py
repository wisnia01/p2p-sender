import tkinter as tk
import ecb_methods as ecb
import cbc_methods as cbc

#AES Implementation
key = b'Sixteen byte key'
iv = b'This is an IV456'

plaintext = b'This is a secret message.'


def main():
    print("start")
    print(ecb.decrypt_ecb(ecb.encrypt_ecb(plaintext, key),key))

    print("cbc now")
    iv, cipher = cbc.encrypt_cbc(plaintext, key)
    print(cbc.decrypt_cbc(cipher, key, iv))

    print("GUI")
    root = tk.Tk()
    root.title("My GUI")

    print("stop")


if __name__ == "__main__":
    main()