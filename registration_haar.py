import cv2
import os
from datetime import datetime
import time

def capture_photos():
    path = './ImageDataset'
    capture_count = 0

    # Create a new folder inside ImageDataset for the captured photos
    folder_name = f'CapturedPhotos_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    folder_path = os.path.join(path, folder_name)
    os.makedirs(folder_path)

    # Initialize Haarcascade for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    capture_duration = 7 # Adjust the duration as needed
    start_time = time.time()
    face_detected = False
    time.sleep(2)

    while capture_count < 2:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cap.set(3, 640)
        cap.set(4, 480)

        if not cap.isOpened():
            print(f"Error: Unable to access the camera.")
            break

        while True:
            c=0
            success, img = cap.read()

            if not success:
                print("Error: Unable to capture an image.")
                break

            # Convert the image to grayscale for Haarcascade
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Capture Photos", img)
            if(c==0):
                cv2.waitKey(1)
                c=1

            # Detect faces using Haarcascade
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(210, 210))

            if len(faces) > 0:
                x, y, width, height = faces[0]
                forehead_height = y
                if forehead_height > 70:  # Adjust the threshold as needed
                    cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)
                    face_detected = True
                else:
                    cv2.putText(img, "Please stay at Center.", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow("Capture Photos", img)
                    cv2.waitKey(3000)
                    face_detected=False

            else:
                face_detected = False

            if face_detected:
                # If face is detected, display the image with rectangle
                cv2.imshow("Capture Photos", img)
            else:
                # If no face is detected, display a message
                cv2.putText(img, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Capture Photos", img)

            # Check if the capture duration has elapsed
            if (time.time() - start_time >= capture_duration and face_detected):
                cv2.waitKey(100)
                if capture_count == 0:
                    
                    capture_count += 1
                    photo_name = f'captured_photo_{capture_count}.jpg'
                    photo_path = os.path.join(folder_path, photo_name)
                    cv2.imwrite(photo_path, img)
                    print(f'Captured photo: {photo_path}')

                    # Display a message inside the window
                    cv2.putText(img, f'Photo {capture_count} clicked!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)
                    cv2.imshow("Capture Photos", img)
                    cv2.waitKey(3)

                    # Wait for 3 seconds
        
                    start_time = time.time()  # Reset the start time for the second photo
                else:
                    # Capture and save the second photo
                    capture_count += 1
                    photo_name = f'captured_photo_{capture_count}.jpg'
                    photo_path = os.path.join(folder_path, photo_name)
                    cv2.imwrite(photo_path, img)
                    print(f'Captured photo: {photo_path}')

                    # Display a message inside the window
                    cv2.putText(img, f'Photo {capture_count} clicked!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)
                    cv2.imshow("Capture Photos", img)

                    # Wait for 3 seconds
                    cv2.waitKey(3)
                    break  # Break out of the loop when two photos are captured

            key = cv2.waitKey(1)

            if key == ord('q'):
                break
        if key == ord('q'):
                break

        cap.release()  # Release the capture object
        cv2.destroyWindow("Capture Photos")  # Destroy the window

    return folder_path

if __name__ == "__main__":
    # Run the function to capture photos and get the folder path
    captured_folder_path = capture_photos()

    
    os.startfile('encoding.exe')
    
