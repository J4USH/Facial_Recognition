import tkinter
from tkinter import * 
from tkinter.ttk import *
import customtkinter

from PIL import ImageTk, Image
import os 



def register():
    help_box.destroy()
    os.startfile('registration_haar.exe')
    w.destroy()
    startup()




def enter_register():
    w.quit()
    global help_box
    help_box = customtkinter.CTkToplevel()
    help_box.resizable(False, False)
    
    help_box.title('How to Register Your Face')
    # warnphoto_1 = PhotoImage(file = r"./Resources/Face_warning.png") 
    # warnphoto_2 = PhotoImage(file = r"./Resources/Face_warning_2.png")
    # warnphoto_3 = PhotoImage(file = r"./Resources/Face_warning_3.png")
    resize_img_1 = Image.open("./Resources/Screen4.png")
    

    warnphoto_1=ImageTk.PhotoImage(resize_img_1)
    


    
    warn_text = customtkinter.CTkLabel(master=help_box,image=warnphoto_1,text="")
    warn_text.pack()
    

   
    
    Proceed_button=customtkinter.CTkButton(master=warn_text,text="Ok",command=register,corner_radius=15,hover_color="green",fg_color="blue",bg_color="white")
    Proceed_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)


    help_box.attributes('-topmost', True)
    
    help_box.mainloop()

    


def enter_Attendance():
    w.quit()
    
    os.startfile('recognition.exe')
    w.destroy()
    startup()


def enter_Encoding():
    w.quit()
    os.startfile('recordManage.exe')
    w.destroy()
    startup()
    




def startup():
    global w
    w = customtkinter.CTk()
    w.resizable(False, False)

    w.title('Facial Recognition')
    image_1 = PhotoImage(file=r'./Resources/Screen3.png')

 


    label_img=customtkinter.CTkLabel(master=w,image=image_1,text="")
    label_img.pack()
# l1 = customtkinter.CTkFrame(master=w, width=200, height=220, corner_radius=15)
# l1.place(relx=0.1, rely=0.3)
    buttonRegister= customtkinter.CTkButton(master=label_img, text="Register Face",command=enter_register,fg_color="#6670ff",height=65,width=200,corner_radius=18,bg_color="white")
    buttonRegister.place(relx=0.17, rely=0.67,anchor=tkinter.CENTER)
# t1 = customtkinter.CTkLabel(master=l1,text="Register your Face")
# t1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
# l2 = customtkinter.CTkFrame(master=w, width=200, height=220, corner_radius=15)
# l2.place(relx=0.4, rely=0.3)
    buttonAttendance= customtkinter.CTkButton(master=label_img, text="Take Attendance",command=enter_Attendance,fg_color="#6670ff",height=65,width=200,corner_radius=18,bg_color="white")
    buttonAttendance.place(relx=0.508, rely=0.67,anchor=tkinter.CENTER)
# t2 = customtkinter.CTkLabel(master=l2,text="Take Attendance")
# t2.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
# l3 = customtkinter.CTkFrame(master=w, width=200, height=220, corner_radius=15)
# l3.place(relx=0.7, rely=0.3)
    buttonEncoding= customtkinter.CTkButton(master=label_img, text="Record Editing",command=enter_Encoding,fg_color="#6670ff",height=65,width=200,corner_radius=18,bg_color="white")
    buttonEncoding.place(relx=0.83, rely=0.67,anchor=tkinter.CENTER)
# t3 = customtkinter.CTkLabel(master=l3,text="Manage Encoding")
# t3.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
    w.eval('tk::PlaceWindow . center')
    w.mainloop()

if __name__ == "__main__":
    startup()

