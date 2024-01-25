# registration.py

import cv2
import os
from datetime import datetime
from mtcnn import MTCNN
import time

def capture_photos():
    path = 'ImageDataset'
    capture_count = 0

    # Create a new folder inside ImageDataset for the captured photos
    folder_name = f'CapturedPhotos_{datetime.now().strftime("%Y%m%d_%H%M%S")}'# name it according to the id 
    folder_path = os.path.join(path, folder_name)
    os.makedirs(folder_path)

    # Initialize MTCNN for face detection
    detector = MTCNN()

    capture_duration = 10 # Adjust the duration as needed
    start_time = time.time()
    face_detected = False

    while capture_count < 2:
        cap = cv2.VideoCapture(0)  # Try different indices if 0 doesn't work
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cap.set(3, 640)
        cap.set(4, 480)

        if not cap.isOpened():
            print(f"Error: Unable to access the camera. Try a different camera index.")
            break

        while True:
            success, img = cap.read()

            if not success:
                print("Error: Unable to capture an image.")
                break

            # Detect faces using MTCNN
            faces = detector.detect_faces(img)

            if faces:
                x, y, width, height = faces[0]['box']
                forehead_height = y
                if forehead_height > 50:  # Adjust the threshold as needed
                    cv2.rectangle(img, (x, y), (x+width, y+height), (0, 255, 0), 2)
                    face_detected = True
            else:
                face_detected = False

            if face_detected:
                # If face is detected, display the image with rectangle
                cv2.imshow("Capture Photos", img)
            else:
                # If no face is detected, display a message
                cv2.putText(img, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Capture Photos", img)

            if time.time() - start_time >= capture_duration and face_detected:
                # Capture and save a photo
                capture_count += 1
                photo_name = f'captured_photo_{capture_count}.jpg'
                photo_path = os.path.join(folder_path, photo_name)
                cv2.imwrite(photo_path, img)
                print(f'Captured photo: {photo_path}')
                
                # Display a message inside the window
                cv2.putText(img, f'Photo {capture_count} clicked!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Capture Photos", img)
                
                # Wait for 3 seconds
                cv2.waitKey(3000)

                if capture_count == 1:
                    time.sleep(3)  # Delay before capturing the second photo

                if capture_count == 2:
                    break  # Break out of the loop when two photos are captured

            key = cv2.waitKey(1)

            if key == ord('q'):
                break

        cap.release()  # Release the capture object
        cv2.destroyWindow("Capture Photos")  # Destroy the window

    return folder_path

if __name__ == "__main__":
    # Run the function to capture photos and get the folder path
    captured_folder_path = capture_photos()

    if captured_folder_path:
        print(f'Captured photos stored in: {captured_folder_path}')
