import tkinter as tk
from tkinter import filedialog
from main import run_encryption, run_decryption


def encrypt_message():
    message = input_text.get("1.0",'end-1c')
    original_image_path = filedialog.askopenfilename()
    encrypted_image_path = filedialog.asksaveasfilename(defaultextension=".png")
    run_encryption(message, original_image_path, encrypted_image_path)
    result_label.config(text="Encryption Successful!")

def decrypt_message():
    encrypted_image_path = filedialog.askopenfilename()
    decrypted_message = run_decryption(encrypted_image_path)
    result_label.config(text=f"Decrypted Message: {decrypted_message}")

root = tk.Tk()
root.title("Image Encryption and Decryption")

input_label = tk.Label(root, text="Enter Message:")
input_label.pack()

input_text = tk.Text(root, height=5, width=50)
input_text.pack()

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_message)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_message)
decrypt_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
