import cv2
import os
from datetime import datetime
from mtcnn import MTCNN
import time

class PhotoCapture:
    def __init__(self, path='ImageDataset'):
        self.path = path
        self.detector = MTCNN()

    def capture_photos(self, capture_duration=10):
        capture_count = 0
        folder_name = f'CapturedPhotos_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        folder_path = os.path.join(self.path, folder_name)
        os.makedirs(folder_path)

        start_time = time.time()
        face_detected = False

        while capture_count < 2:
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                print(f"Error: Unable to access the camera. Try a different camera index.")
                break

            while True:
                success, img = cap.read()

                if not success:
                    print("Error: Unable to capture an image.")
                    break

                faces = self.detector.detect_faces(img)

                if faces:
                    x, y, width, height = faces[0]['box']
                    forehead_height = y
                    if forehead_height > 50:
                        cv2.rectangle(img, (x, y), (x+width, y+height), (0, 255, 0), 2)
                        face_detected = True
                else:
                    face_detected = False

                if face_detected:
                    cv2.imshow("Capture Photos", img)
                else:
                    cv2.putText(img, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow("Capture Photos", img)

                if time.time() - start_time >= capture_duration and face_detected:
                    capture_count += 1
                    photo_name = f'captured_photo_{capture_count}.jpg'
                    photo_path = os.path.join(folder_path, photo_name)
                    cv2.imwrite(photo_path, img)
                    print(f'Captured photo: {photo_path}')

                    cv2.putText(img, f'Photo {capture_count} clicked!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Capture Photos", img)

                    cv2.waitKey(3000)

                    if capture_count == 1:
                        time.sleep(3)

                    if capture_count == 2:
                        break

                key = cv2.waitKey(1)

                if key == ord('q'):
                    break

            cap.release()
            cv2.destroyWindow("Capture Photos")

        return folder_path

if __name__ == "__main__":
    photo_capture = PhotoCapture()
    captured_folder_path = photo_capture.capture_photos()

    if captured_folder_path:
        print(f'Captured photos stored in: {captured_folder_path}')