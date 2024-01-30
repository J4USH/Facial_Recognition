
import tkinter
import customtkinter
import os
import csv
import face_recognition



def submit():
    
    root.destroy()
    
    global id_t
    global name
    global dob
    global position

    id_t = id_entry.get()
    name = name_entry.get()
    dob = dob_entry.get()
    position = position_entry.get()
    

def fill_form():
    global root
    root = customtkinter.CTk()
    root.title("Registration")
    root.geometry("600x600")
    root.resizable(False, False)
    
    global id_entry
    global name_entry
    global dob_entry
    global position_entry
    

    # Create a label for the title
    title_label = customtkinter.CTkLabel(master=root, text="Registration", font=("Arial", 18, "bold"))
    title_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

    # Create a label for ID
    id_label = customtkinter.CTkLabel(master=root, text="ID:", font=("Arial", 14))
    id_label.place(relx=0.2, rely=0.2, anchor=tkinter.CENTER)

    # Create a label for Name
    name_label = customtkinter.CTkLabel(master=root, text="Name:", font=("Arial", 14))
    name_label.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

    # Create a label for Date of Birth
    dob_label = customtkinter.CTkLabel(master=root, text="Date of Birth:", font=("Arial", 14))
    dob_label.place(relx=0.2, rely=0.4, anchor=tkinter.CENTER)

    # Create a label for Position
    position_label = customtkinter.CTkLabel(master=root, text="Position:", font=("Arial", 14))
    position_label.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)

    # Create a label for ID
    id_entry = customtkinter.CTkEntry(master=root, font=("Arial", 14))
    id_entry.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

    # Create a label for Name
    name_entry = customtkinter.CTkEntry(master=root, font=("Arial", 14))
    name_entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

    # Create a label for Date of Birth
    dob_entry = customtkinter.CTkEntry(master=root, font=("Arial", 14))
    dob_entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    # Create a label for Position
    position_entry = customtkinter.CTkEntry(master=root, font=("Arial", 14))
    position_entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # Create a button to submit the form
    button = customtkinter.CTkButton(master=root, text="Submit", font=("Arial", 14), command=submit)
    button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
    root.mainloop()



def process_folder(folder_path):
    # Load captured photos and find facial encodings
    face_encodings = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".jpg"):
                image_path = os.path.join(root, filename)
                image = face_recognition.load_image_file(image_path)

                # Assuming there's only one face in the image
                face_encoding = face_recognition.face_encodings(image)[0]
                face_encodings.append(face_encoding)

    return face_encodings

def save_encodings_to_csv(face_encodings, csv_file_path):
    # Save facial encodings to a CSV file
    fill_form()
    global id_t
    global name
    global dob
    global position

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID.", "Face Encoding","Name","DOB","Position"])

        for ID, face_encoding in enumerate(face_encodings, start=1):
            writer.writerow([ID, face_encoding,name,dob,position])

    print(f'Facial encodings saved to: {csv_file_path}')

if __name__ == "__main__":
    # Specify the folder path where photos are stored
    
    root_folder_path = 'FacialRecognition/ImageDataset'  # Update with the actual path

    # Create a list to store all face encodings
    all_face_encodings = []

    for folder_name in os.listdir(root_folder_path):
        folder_path = os.path.join(root_folder_path, folder_name)

        if os.path.isdir(folder_path):
            print(f'Processing folder: {folder_path}')

            # Run the function to process the folder and get facial encodings
            face_encodings = process_folder(folder_path)

            if face_encodings:
                # Extend the list with the current folder's encodings
                all_face_encodings.extend(face_encodings)

    # Specify the CSV file path for the combined encodings
    combined_csv_file_path = os.path.join(root_folder_path, "facial_encodings_combined.csv")

    # Run the function to save combined facial encodings to CSV
    save_encodings_to_csv(all_face_encodings, combined_csv_file_path)
