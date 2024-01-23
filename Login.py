import tkinter as tk
from tkinter import messagebox

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login Page")
        self.geometry("400x300")
        self.resizable(False, False)

        self.background_color = "#F0F0F0"

        self.create_widgets()

    def create_widgets(self):
        # Frame for the login form
        login_frame = tk.Frame(self, bg=self.background_color)
        login_frame.pack(pady=20)

        # Label for the username
        username_label = tk.Label(login_frame, text="Username:", bg=self.background_color, font=("Arial", 12))
        username_label.grid(row=0, column=0, padx=(20, 0), pady=(0, 5))

        # Entry for the username
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=(0, 20), pady=(0, 5))

        # Label for the password
        password_label = tk.Label(login_frame, text="Password:", bg=self.background_color, font=("Arial", 12))
        password_label.grid(row=1, column=0, padx=(20, 0), pady=(5, 5))

        # Entry for the password
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, padx=(0, 20), pady=(5, 5))

        # Button for submitting the login form
        submit_button = tk.Button(login_frame, text="Login", bg="#2E86C1", fg="white", font=("Arial", 12, "bold"), command=self.login)
        submit_button.grid(row=2, column=1, padx=(0, 20), pady=(5, 20))

        # Label for the error message
        self.error_label = tk.Label(self, text="", fg="red", font=("Arial", 10))
        self.error_label.pack()

    def login(self):
        # Get the username and password from the entries
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate the username and password
        if username == "User" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            self.destroy()
        else:
            self.error_label.config(text="Invalid username or password")

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()