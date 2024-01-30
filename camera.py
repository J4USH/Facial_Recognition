import cv2

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Stop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()