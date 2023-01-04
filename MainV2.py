import cv2

# Initialize the Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(r'C:\Users\Addison\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\cv2\data\haarcascade_frontalface_default.xml')

# Calibrate the player height
init_height = 300
jump_offset = 25



# Start the video capture
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920/2)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    # Read a frame from the video
    ret, frame = video.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # Draw a line in the center of the frame
    height, width = frame.shape[:2]
    cv2.line(frame, (0, height//2), (width, height//2), (0, 255, 0), 2)

    # Write FPS on top right corner
    cv2.putText(frame, f"FPS: {int(video.get(cv2.CAP_PROP_FPS))}", (width-100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Iterate over the faces and draw a rectangle around them
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Calculate the center of the bounding box
        center_x = x + w // 2
        center_y = y + h // 2

        # Draw a circle at the center of the bounding box
        cv2.circle(frame, (center_x, center_y), 3, (0, 0, 255), -1)

        # Draw center line
        cv2.line(frame, (0, init_height), (1920, init_height), (255, 255, 255), 2)

        # If y coords for BB is greater than half of the webcam height, then emulate a spacebar press
        if center_y < (init_height + jump_offset):
            print("Spacebar Pressed")
        else:
            print("")


        # Print the position of the bounding box center
        # print(f"Bounding box center: ({center_x}, {center_y})")

    # Show the frame
    cv2.imshow('Frame', frame)

    # Check if the user pressed the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("Calibrated Height")
        init_height = center_y

# Release the video capture and destroy all windows
video.release()
cv2.destroyAllWindows()
