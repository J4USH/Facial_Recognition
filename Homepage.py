import tkinter
from tkinter import * 
from tkinter.ttk import *
import customtkinter

from PIL import ImageTk, Image
import os 



def register():
    help_box.destroy()
    os.system('python FacialRecognition/registration_haar.py')




def enter_register():
    w.quit()
    global help_box
    help_box = customtkinter.CTkToplevel()
    help_box.geometry("600x440")
    help_box.title('How to Register Your Face')
    # warnphoto_1 = PhotoImage(file = r"FacialRecognition/Resources/Face_warning.png") 
    # warnphoto_2 = PhotoImage(file = r"FacialRecognition/Resources/Face_warning_2.png")
    # warnphoto_3 = PhotoImage(file = r"FacialRecognition/Resources/Face_warning_3.png")
    resize_img_1 = Image.open("FacialRecognition/Resources/Face_warning.png")
    resize_img_1 = resize_img_1.resize((220,200), Image.ANTIALIAS)
    resize_img_2 = Image.open("FacialRecognition/Resources/Face_warning_2.png")
    resize_img_2 = resize_img_2.resize((220,200), Image.ANTIALIAS)
    resize_img_3 = Image.open("FacialRecognition/Resources/Face_warning_3.png")
    resize_img_3 = resize_img_3.resize((220,200), Image.ANTIALIAS)

    warnphoto_1=ImageTk.PhotoImage(resize_img_1)
    warnphoto_2=ImageTk.PhotoImage(resize_img_2)
    warnphoto_3=ImageTk.PhotoImage(resize_img_3)


    
    warn_text = customtkinter.CTkLabel(master=help_box,text="Advice on How to Register Your Face",font=("Arial", 18, "bold"))
    warn_text.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    

    warn_image_1=customtkinter.CTkLabel(master=help_box,image=warnphoto_1,text="")
    warn_image_1.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)
    
    warn_image_2 = customtkinter.CTkLabel(master=help_box,image=warnphoto_2,text="")
    warn_image_2.place(relx=0.4, rely=0.3, anchor=tkinter.CENTER)
    
    warn_image_3 = customtkinter.CTkLabel(master=help_box,image=warnphoto_3,text="")
    warn_image_3.place(relx=0.6, rely=0.3, anchor=tkinter.CENTER)

    advice_text= customtkinter.CTkLabel(master=help_box,text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ultrices neque sapien, id imperdiet odio vehicula vitae.",font=("Arial", 18, "bold"))
    advice_text.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
    advice_text_2= customtkinter.CTkLabel(master=help_box,text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ultrices neque sapien, id imperdiet odio vehicula vitae.",font=("Arial", 18, "bold"))
    advice_text_2.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    advice_text_3= customtkinter.CTkLabel(master=help_box,text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ultrices neque sapien, id imperdiet odio vehicula vitae.",font=("Arial", 18, "bold"))
    advice_text_3.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    
    Proceed_button=customtkinter.CTkButton(master=help_box,text="Ok",command=register)
    Proceed_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)


    help_box.attributes('-topmost', True)
    help_box.mainloop()

    


def enter_Attendance():
    w.destroy()
    os.system('python FacialRecognition/recognition.py')


def enter_Encoding():
    w.destroy()
    os.system('python FacialRecognition/encoding.py')


help_box=NONE


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
