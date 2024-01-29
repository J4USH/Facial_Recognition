

import os
import csv
import face_recognition

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
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID.", "Face Encoding"])

        for ID, face_encoding in enumerate(face_encodings, start=1):
            writer.writerow([ID, face_encoding])

    print(f'Facial encodings saved to: {csv_file_path}')

if __name__ == "__main__":
    # Specify the folder path where photos are stored
    root_folder_path = 'ImageDataset'  # Update with the actual path

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
