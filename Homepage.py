import tkinter
from tkinter import * 
from tkinter.ttk import *
import customtkinter
import registration
from PIL import ImageTk, Image
import os 




def enter_register():
    w.destroy()
    os.system('python FacialRecognition/registration_haar.py')


def enter_Attendance():
    w.destroy()
    os.system('python FacialRecognition/recognition.py')


def enter_Encoding():
    w.destroy()
    os.system('python FacialRecognition/encoding.py')


w = customtkinter.CTk()
w.geometry("1280x720")
w.title('Facial Recognition')
image_1 = PhotoImage(file=r'FacialRecognition/Resources/Venuratech.png').zoom(2,2)

resgi_img = Image.open('FacialRecognition/Resources/Registration.png')
resgi_img = resgi_img.resize((220,220), Image.ANTIALIAS)
photo_1=ImageTk.PhotoImage(resgi_img)
photo_2 = PhotoImage(file = r"FacialRecognition/Resources/Attendance.png") 
photo_3 = PhotoImage(file = r"FacialRecognition/Resources/Manage.png") 


label_img=customtkinter.CTkLabel(master=w,image=image_1,text="")
label_img.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
l1 = customtkinter.CTkFrame(master=w, width=200, height=220, corner_radius=15)
l1.place(relx=0.1, rely=0.3)
b1= customtkinter.CTkButton(master=l1, text="",command=enter_register,image=photo_1)
b1.place(relx=0.5, rely=0.4,anchor=tkinter.CENTER)
t1 = customtkinter.CTkLabel(master=l1,text="Register your Face")
t1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
l2 = customtkinter.CTkFrame(master=w, width=200, height=220, corner_radius=15)
l2.place(relx=0.4, rely=0.3)
b2= customtkinter.CTkButton(master=l2, text="",command=enter_Attendance,image=photo_2)
b2.place(relx=0.5, rely=0.4,anchor=tkinter.CENTER)
t2 = customtkinter.CTkLabel(master=l2,text="Take Attendance")
t2.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
l3 = customtkinter.CTkFrame(master=w, width=200, height=220, corner_radius=15)
l3.place(relx=0.7, rely=0.3)
b3= customtkinter.CTkButton(master=l3, text="",command=enter_Encoding,image=photo_3)
b3.place(relx=0.5, rely=0.4,anchor=tkinter.CENTER)
t3 = customtkinter.CTkLabel(master=l3,text="Manage Encoding")
t3.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
w.mainloop()
