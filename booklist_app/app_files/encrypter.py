from cryptography.fernet import Fernet


def get_encrypted(plain):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted = cipher_suite.encrypt(bytes(plain, "utf-8"))
    return encrypted
