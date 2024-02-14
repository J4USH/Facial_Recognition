import cv2
import face_recognition
import numpy as np
import csv
import os
import time
import datetime
import pandas as pd
import tkinter
from CTkMessagebox import CTkMessagebox
import customtkinter
from PIL import ImageTk, Image
Check=False


# def load_combined_encodings(csv_file_path):
#     combined_encodings = {}
#     with open(csv_file_path, mode='r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header line
#         for row in reader:
#             person_id, encoding = row[0], np.array([float(val) for val in row[1:]])
#             combined_encodings[person_id] = encoding
#     return combined_encodings

def load_combined_encodings(csv_file_path):
    global name
    global details
    details={}
    combined_encodings = {}
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            person_id, encoding_str,name,dob,position = row[0], row[1],row[2],row[3],row[4]
            details[person_id]=[name,dob,position]
            encoding = np.fromstring(encoding_str[1:-1], sep=' ')
            combined_encodings[person_id] = encoding
    return combined_encodings

def confirmation_win(person_id):
    nm,db,pos=details[person_id]
    

    

    
    global app
    app = customtkinter.CTk()  # creating custom tkinter window
    app.title('Confirm')
    app.resizable(False, False)
    img1 = ImageTk.PhotoImage(Image.open("./Resources/screen5.png"))
    l1 = customtkinter.CTkLabel(master=app, image=img1, text="")
    l1.pack()
    l2 = customtkinter.CTkLabel(master=l1, text="Name:"+nm, font=("Arial", 14),bg_color="white",text_color="black")
    l2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    l3 = customtkinter.CTkLabel(master=l1, text="Date of Birth: "+db, font=("Arial", 14),bg_color="white",text_color="black")
    l3.place(relx=0.5, rely=0.57, anchor=tkinter.CENTER)
    l4 = customtkinter.CTkLabel(master=l1, text="Position: "+pos, font=("Arial", 14),bg_color="white",text_color="black")
    l4.place(relx=0.5, rely=0.64, anchor=tkinter.CENTER)
    yesBtn = customtkinter.CTkButton(master=app,text="Yes",command=lambda: updateAttendance(person_id,datetime.datetime.now()),corner_radius=15,hover_color="green",fg_color="blue",bg_color="white")
    yesBtn.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
    noBtn = customtkinter.CTkButton(master=app,text="No",command=app.destroy,corner_radius=15,hover_color="red",fg_color="blue",bg_color="white")
    noBtn.place(relx=0.6, rely=0.9, anchor=tkinter.CENTER)

    app.mainloop()

    


def updateAttendance(person_id,datetime):
    app.destroy()
    with open('./Attendance.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([person_id,datetime])
        print(f'Attendance stored to: Attendance.csv')
    global Check
    Check=True

def recognize_faces(img, combined_encodings):
    img_chc = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces_cur_frame = face_recognition.face_locations(img_chc)
    encodes_cur_frame = face_recognition.face_encodings(img_chc, faces_cur_frame)

    for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
        matches = face_recognition.compare_faces(list(combined_encodings.values()), encode_face)
        face_dis = face_recognition.face_distance(list(combined_encodings.values()), encode_face)
        match_index = np.argmin(face_dis)

        if matches[match_index]:
            person_id = list(combined_encodings.keys())[match_index]
            confirmation_win(person_id)
            
        
            # y1, x2, y2, x1 = face_loc
            

            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, person_id, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

if __name__ == "__main__":
    # Specify the CSV file path with combined encodings
    csv_file_path = './ImageDataset/facial_encodings_combined.csv'  # Update with the actual path

    # Load combined encodings from the CSV file
    combined_encodings = load_combined_encodings(csv_file_path)
    

    # Start video capture
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
    cap.set(3, 640)
    cap.set(4, 480)
    startIme=time.time()

    while True:
        success, img = cap.read()

        if not success:
            print("Error: Unable to capture an image.")
            break

        
        

        # Display the frame
        cv2.imshow("FacialDetection", img)
        
        cv2.waitKey(1)

        recognize_faces(img, combined_encodings)
        

        # Break the loop if the 'q' key is pressed
        if startIme-time.time()>8 or Check==True:
            break

    # Release the capture object and destroy the window
    cap.release()
    cv2.destroyAllWindows()
