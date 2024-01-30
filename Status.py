import socket
import tkinter
import customtkinter
import cv2
from PIL import ImageTk, Image

class StatusApp:
    def __init__(self):

        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")

   
        self.window = customtkinter.CTk()
        self.window.title("Attendance App")
        self.window.geometry("440x300")
        self.window.resizable(False, False)
       

        self.img1 = ImageTk.PhotoImage(Image.open("D:\CODE\FacialRecognition\Resources\d7e10329fef2ed0797580571ee7e48fb.jpg"))
        self.l1 = customtkinter.CTkLabel(master=self.window, image=self.img1, text=" ")
        self.l1.pack()
      

        self.frame = customtkinter.CTkFrame(master=self.l1,width=420, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.available_net = False
        self.available_camera = False
        self.img2 = ImageTk.PhotoImage(Image.open("D:\CODE\FacialRecognition\Resources\Venuratech.png"))
        self.l2 = customtkinter.CTkLabel(master=self.frame, image=self.img2, text=" ")
        self.l2.pack(pady=10)

        self.text_label = customtkinter.CTkLabel(self.frame, text="Welcome To The Attendance App", font=("Arial", 18, "bold"))
        self.text_label.pack(pady=10)
        self.check_label = customtkinter.CTkLabel(self.frame, text="Press Start", font=("Arial", 20, "bold"))
        self.check_label.pack(pady=10)
        self.check_button = customtkinter.CTkButton(self.frame, text='Start', command=self.connect,  font=("Arial", 12, "bold"))
        self.check_button.pack(pady=10)
        self.status_label = customtkinter.CTkLabel(self.frame, text="",  font=("Arial", 20, "bold"))
        self.status_label.pack(pady=10)
        self.camera_status = customtkinter.CTkLabel(self.frame, text="", font=("Arial", 20, "bold"))
        self.camera_status.pack(pady=10)
        

        self.window.mainloop()

    def login(self):
        self.window.destroy()
        import Custom_login
        
        app = Custom_login.LoginApp()
        app.app.mainloop()




    def check_cameras(self):
        cameras = []
        for i in range(5):
            try:
                cap = cv2.VideoCapture(i)
                if cap is None or not cap.isOpened():
                    pass
                else:
                    cameras.append(i)

                cap.release()
            except:
                continue
        return len(cameras)

    def is_connected(self):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("1.1.1.1", 53))
            return True
        except OSError:
            pass
        return False

    def connect(self):
        self.check_button.configure(text="Checking...")
        self.window.update()
        if self.is_connected():
            self.status_label.configure(text="✔️Connected to The Internet")
            self.available_net = True
        else:
            self.status_label.configure(text="❌Not Connected to the Internet")

        if self.check_cameras() == 0:
            self.camera_status.configure(text="❌No Cameras Detected")
        else:
            self.camera_status.configure(text=f"✔️{self.check_cameras()} Cameras Detected")
            self.available_camera = True

        if self.available_camera and self.available_net:
            self.check_label.configure(text="✔️Everything is Working")
            self.check_button.configure(text="Proceed -->", command=self.login)
        else:
            self.check_button.configure(text="⟳ Retry")

if __name__ == "__main__":
    app = StatusApp()