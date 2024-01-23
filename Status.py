import socket
import tkinter as tk
import cv2

class StatusApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Attendance App")
        self.window.geometry("440x300")
        self.window.resizable(False, False)
        self.frame = tk.Frame(self.window, background="orange")

        self.available_net = False
        self.available_camera = False

        self.text_label = tk.Label(self.frame, text="Welcome To The Attendance App", background="orange", fg='white', font=("Arial", 20, "bold"))
        self.text_label.pack(pady=10)
        self.check_label = tk.Label(self.frame, text="Press Start", background="orange", fg='white', font=("Arial", 20, "bold"))
        self.check_label.pack(pady=10)
        self.check_button = tk.Button(self.frame, text='Start', bd='5', command=self.connect, background="orange", fg='white', font=("Arial", 20, "bold"))
        self.check_button.pack(pady=10)
        self.status_label = tk.Label(self.frame, text="", background="orange", fg='white', font=("Arial", 20, "bold"))
        self.status_label.pack(pady=10)
        self.camera_status = tk.Label(self.frame, text="", background="orange", fg='white', font=("Arial", 20, "bold"))
        self.camera_status.pack(pady=10)
        self.frame.pack()

        self.window.mainloop()

    def login(self):
        self.window.destroy()
        import Custom_login
        
        app = Custom_login.LoginApp()
        app.app.mainloop()




    def check_cameras(self):
        cameras = []
        for i in range(10):
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
        if self.is_connected():
            self.status_label.config(text="✔️Connected to The Internet")
            self.available_net = True
        else:
            self.status_label.config(text="❌Not Connected to the Internet")

        if self.check_cameras() == 0:
            self.camera_status.config(text="❌No Cameras Detected")
        else:
            self.camera_status.config(text=f"✔️{self.check_cameras()} Cameras Detected")
            self.available_camera = True

        if self.available_camera and self.available_net:
            self.check_label.config(text="✔️Everything is Working")
            self.check_button.config(text="Proceed -->", command=self.login)
        else:
            self.check_button.config(text="⟳ Retry")

if __name__ == "__main__":
    app = StatusApp()