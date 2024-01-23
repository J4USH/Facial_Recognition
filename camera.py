import cv2

def check_cameras():
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
    return cameras

print(check_cameras())