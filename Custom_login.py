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
        
        self.app.title('Login')
        self.app.resizable(False, False)

        self.button_function = self.button_function  # bind the function to the instance

        self.img1 = ImageTk.PhotoImage(Image.open("./Resources/Screen2.jpg"))
        self.l1 = customtkinter.CTkLabel(master=self.app, image=self.img1, text=" ")
        self.l1.pack()

        # creating custom frame
        self.frame = customtkinter.CTkFrame(master=self.l1, corner_radius=15,fg_color="white",bg_color="white",width=450)
        self.frame.place(relx=0.67, rely=0.6, anchor=tkinter.CENTER)

        


        

        self.entry1 = customtkinter.CTkEntry(master=self.frame, placeholder_text='Username',width=250)
        self.entry1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, placeholder_text='Password', show="*",width=250)
        self.entry2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.l3 = customtkinter.CTkButton(master=self.frame, text="Forget password?", font=('Century Gothic', 12),command=self.forgetPassword,hover_color="orange",fg_color="black")
        self.l3.place(relx=0.7, rely=0.45, anchor=tkinter.CENTER)

        # Create custom button
        self.button1 = customtkinter.CTkButton(master=self.frame,  text="Login", command=self.button_function, corner_radius=6,hover_color="orange",fg_color="black")
        self.button1.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

        self.l4 = customtkinter.CTkLabel(master=self.frame, text="", font=('Century Gothic', 12))
        self.l4.place(relx=0.5, rely=0.9 , anchor=tkinter.CENTER)

    def button_function(self):
        if (self.entry1.get() == "Agnibha" and self.entry2.get() == "password"):
            self.app.destroy()  # destroy current window and creating new one
            os.startfile('Homepage.py')
           
        else:
            self.l4.configure(text="Wrong Password/Username", fg_color=("red"))



    def forgetPassword(self):
        CTkMessagebox(title="Warning",icon='warning', message="Please contact your administrator for the password")
        





if __name__ == "__main__":
    login_app = LoginApp()
    login_app.app.eval('tk::PlaceWindow . center')
    login_app.app.mainloop()