import cv2
import pyautogui

video = cv2.VideoCapture(0)

# Set video size
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920/2)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
video.set(cv2.CAP_PROP_FPS, 30)

# Init Tracker
tracker = cv2.legacy.TrackerMOSSE_create()
success, img = video.read()

# Calibrate tracker
calibrated = False
def CalibrateTracking():
    global calibrated
    bbox = cv2.selectROI("Tracking", img, False)
    tracker.init(img, bbox)
    calibrated = True
    return bbox

# Rerun (Hotfix lol)
def rerun():
    # Free resources
    video.release()
    cv2.destroyAllWindows()

    # Rerun the program
    import ROITracking
    ROITracking

# Draw box around object
def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Draw circle at y axis
    cv2.circle(img, (x + int(w / 2), y), 5, (0, 255, 0), -1)
    return y


inital_height = 900
jump_offset = 50


while True:
    timer = cv2.getTickCount()
    success, img = video.read()
    success, bbox = tracker.update(img)
    # print(f"Tracker Success: {success}")

    # Set video to greyscale
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('r'):
        if calibrated:
            rerun()
        else:
            print("Calibrating...")
            print("Press C after calibration")
            bbox = CalibrateTracking()

    if success:
        yaxis = drawBox(img, bbox)
        ypos = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT) - yaxis)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Calibrate Inital Height
            cv2.line(img, (0, yaxis - jump_offset), (1920, yaxis - jump_offset), (0, 255, 0), 2)
            inital_height = ypos
            
        # Detect for junp 
        if ypos > jump_offset + inital_height:
            print("Jump Detected")
            pyautogui.press('space')

        print(f"Y Axis: {ypos} | Inital Height: {inital_height} | Offset: {inital_height + jump_offset}")
        
    else:
        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img, f"FPS: {int(fps)}", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Tracking", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video.release()
        cv2.destroyAllWindows()
        break