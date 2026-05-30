import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

HOST = simpledialog.askstring("Server IP", "Enter server IP:")
PORT = 5555

nickname = simpledialog.askstring("Nickname", "Choose a nickname:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except:
    messagebox.showerror("Error", "Unable to connect to server.")
    exit()

window = tk.Tk()
window.title(f"Chat - {nickname}")
window.geometry("500x500")

chat_area = scrolledtext.ScrolledText(window)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state=tk.DISABLED)

message_entry = tk.Entry(window)
message_entry.pack(padx=10, pady=5, fill=tk.X)

def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "NICK":
                client.send(nickname.encode())
            else:
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, message + "\n")
                chat_area.config(state=tk.DISABLED)
                chat_area.yview(tk.END)

        except:
            client.close()
            break

def send_message(event=None):
    message = message_entry.get()

    if message:
        full_message = f"{nickname}: {message}"
        client.send(full_message.encode())
        message_entry.delete(0, tk.END)

send_button = tk.Button(
    window,
    text="Send",
    command=send_message
)
send_button.pack(pady=5)

message_entry.bind("<Return>", send_message)

thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()

window.mainloop()