import logging
import sqlite3
from tkinter import Tk, Label, Button, Entry

# Setup logging
logging.basicConfig(filename="cipher_log.txt", level=logging.INFO, format='%(asctime)s - %(message)s')

# Caesar Cipher
def caesar_encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)

# Substitution Cipher
def substitution_encrypt(text, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    for char in text.lower():
        if char in alphabet:
            idx = alphabet.index(char)
            result += key[idx]
        else:
            result += char
    return result

def substitution_decrypt(text, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    for char in text.lower():
        if char in key:
            idx = key.index(char)
            result += alphabet[idx]
        else:
            result += char
    return result

# Store operation in SQLite
def store_operation(operation, text, result):
    connection = sqlite3.connect("operations.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS operations
                      (operation TEXT, text TEXT, result TEXT)''')
    cursor.execute("INSERT INTO operations (operation, text, result) VALUES (?, ?, ?)",
                   (operation, text, result))
    connection.commit()
    connection.close()

# Tkinter GUI
def create_gui():
    root = Tk()
    root.title("Cipher App")

    Label(root, text="Enter Text:").grid(row=0, column=0)
    text_input = Entry(root)
    text_input.grid(row=0, column=1)

    Label(root, text="Enter Key:").grid(row=1, column=0)
    key_input = Entry(root)
    key_input.grid(row=1, column=1)

    result_label = Label(root, text="Result:")
    result_label.grid(row=3, column=0)

    def encrypt_action():
        text = text_input.get()
        key = int(key_input.get())
        result = caesar_encrypt(text, key)
        result_label.config(text=f"Result: {result}")
        store_operation("Caesar Encrypt", text, result)
        logging.info(f"Encrypted text: {result}")

    Button(root, text="Encrypt (Caesar)", command=encrypt_action).grid(row=2, column=0)

    def decrypt_action():
        text = text_input.get()
        key = int(key_input.get())
        result = caesar_decrypt(text, key)
        result_label.config(text=f"Result: {result}")
        store_operation("Caesar Decrypt", text, result)
        logging.info(f"Decrypted text: {result}")

    Button(root, text="Decrypt (Caesar)", command=decrypt_action).grid(row=2, column=1)

    root.mainloop()

# Main Execution
if __name__ == "__main__":
    create_gui()
