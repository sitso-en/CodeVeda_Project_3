import os
from cryptography.fernet import Fernet

# --- Caesar Cipher Functions ---
def caesar_encrypt(text, shift=3):
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift=3):
    return caesar_encrypt(text, -shift)

# --- Fernet Functions ---
def generate_key():
    key = Fernet.generate_key()
    with open('fernet.key', 'wb') as f:
        f.write(key)
    return key

def load_key():
    with open('fernet.key', 'rb') as f:
        return f.read()

def fernet_encrypt(text):
    key = generate_key()
    f = Fernet(key)
    return f.encrypt(text.encode())

def fernet_decrypt(token):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(token).decode()

# --- File Operations ---
def process_file(filename, mode, method):
    with open(filename, 'r') as f:
        content = f.read()

    if method == 'caesar':
        if mode == 'encrypt':
            processed = caesar_encrypt(content)
        else:
            processed = caesar_decrypt(content)
        out_file = f"{filename}.{mode}.caesar.txt"
        with open(out_file, 'w') as f:
            f.write(processed)

    elif method == 'fernet':
        if mode == 'encrypt':
            processed = fernet_encrypt(content)
            out_file = f"{filename}.{mode}.fernet.txt"
            with open(out_file, 'wb') as f:
                f.write(processed)
        else:
            with open(filename, 'rb') as f:
                token = f.read()
            processed = fernet_decrypt(token)
            out_file = f"{filename}.decrypted.fernet.txt"
            with open(out_file, 'w') as f:
                f.write(processed)

    print(f"{mode.capitalize()}ed file saved as: {out_file}")

# --- Main ---
if __name__ == "__main__":
    filename = input("Enter filename: ")
    mode = input("Choose mode (encrypt/decrypt): ").strip().lower()
    method = input("Choose method (caesar/fernet): ").strip().lower()

    if os.path.exists(filename):
        process_file(filename, mode, method)
    else:
        print("File not found.")