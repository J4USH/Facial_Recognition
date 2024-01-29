import cv2
import face_recognition
import numpy as np
import csv
import os

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
    combined_encodings = {}
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            person_id, encoding_str = row[0], row[1]
            encoding = np.fromstring(encoding_str[1:-1], sep=' ')
            combined_encodings[person_id] = encoding
    return combined_encodings


# def load_combined_encodings(csv_file_path):
#     combined_encodings = {}
#     with open(csv_file_path, mode='r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             person_id, encoding = row[0], np.array([float(val) for val in row[1:]])
#             combined_encodings[person_id] = encoding
#     return combined_encodings

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
            y1, x2, y2, x1 = face_loc
            print(face_loc)

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, person_id, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

if __name__ == "__main__":
    # Specify the CSV file path with combined encodings
    csv_file_path = 'FacialRecognition/Facial_Recognition/ImageDataset/facial_encodings_combined.csv'  # Update with the actual path

    # Load combined encodings from the CSV file
    combined_encodings = load_combined_encodings(csv_file_path)

    # Start video capture
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        success, img = cap.read()

        if not success:
            print("Error: Unable to capture an image.")
            break

        # Recognize faces in the current frame
        recognize_faces(img, combined_encodings)

        # Display the frame
        cv2.imshow("FacialDetection", img)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture object and destroy the window
    cap.release()
    cv2.destroyAllWindows()
