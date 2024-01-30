import tkinter
from CTkMessagebox import CTkMessagebox
import customtkinter
from PIL import ImageTk, Image
import os

class LoginApp:
    def __init__(self):
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        self.app = customtkinter.CTk()  # creating custom tkinter window
        self.app.geometry("600x440")
        self.app.title('Login')

        self.button_function = self.button_function  # bind the function to the instance

        self.img1 = ImageTk.PhotoImage(Image.open("FacialRecognition/Resources/pattern.png"))
        self.l1 = customtkinter.CTkLabel(master=self.app, image=self.img1, text=" ")
        self.l1.pack()

        # creating custom frame
        self.frame = customtkinter.CTkFrame(master=self.l1, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.img3 = ImageTk.PhotoImage(Image.open("FacialRecognition/Resources/Venuratech.png"))

        self.image = customtkinter.CTkLabel(master=self.frame, image=self.img3, text="")
        self.image.place(x=35, y=3)

        self.l2 = customtkinter.CTkLabel(master=self.frame, text="Log into your Account", font=('Century Gothic', 20))
        self.l2.place(x=50, y=45)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Username')
        self.entry1.place(x=50, y=110)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Password', show="*")
        self.entry2.place(x=50, y=165)

        self.l3 = customtkinter.CTkButton(master=self.frame, text="Forget password?", font=('Century Gothic', 12),command=self.forgetPassword,hover=False)
        self.l3.place(x=155, y=195)

        # Create custom button
        self.button1 = customtkinter.CTkButton(master=self.frame, width=220, text="Login", command=self.button_function, corner_radius=6)
        self.button1.place(x=50, y=240)

        self.l4 = customtkinter.CTkLabel(master=self.frame, text="", font=('Century Gothic', 12))
        self.l4.place(x=50, y=290)

    def button_function(self):
        if (self.entry1.get() == "Agnibha" and self.entry2.get() == "password"):
            self.app.destroy()  # destroy current window and creating new one
            os.system('python FacialRecognition/Homepage.py')
           
        else:
            self.l4.configure(text="Wrong Password/Username", fg_color=("red"))



    def forgetPassword(self):
        CTkMessagebox(title="Warning",icon='warning', message="Please contact your administrator for the password")
        





if __name__ == "__main__":
    login_app = LoginApp()
    login_app.app.mainloop()