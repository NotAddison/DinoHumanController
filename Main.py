# Made By Addison Chua (https://github.com/NotAddison)
# SideNote : V2 uses an estimated center dot from the coordinates of the Bondary Boxes (BBox) to determine the number of people on each side (left & right)

# Modules (OpenCV, time (FPS))
import cv2 as cv 
from time import time
import pyautogui

# --- ⚙ OpenCV Settings ⚙ ---
threshold = 0.55        # Main threshold for obj detection [aka, sensitivity]
toMirror = True         # Mirrors the projected frames (Use True if you're using a webcam & Left and right are mirrored)
center_offset = 100     # Offset for center dot (Note To Self: Need to fix for better accuracy) [100 if close : 200 if far]

font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
thickness = 2
bbox_color = (255,169,0)
text_colour = (0,255,0)

header = False;                 # Display Header Toggle
header_scale = 1                # Header Font Scale
header_thickness = 2            # Header Font Thickness
header_color = (255,255,255)    # Header Font Color

debug = True;                  # Show debugging stats
debug_fontSc          le  = 0.5          # Show debugging stats
debug_thickness = 1;            # Thickness of debugging text
debug_Colour = (77, 40, 225)    # Colour of debugging text

# Jump Offset
jump_offset = 25
inital_height = 0

# Load Dependency Files
config = r'Assets\Dependencies\coco-config.pbtxt'
frozen_model = r'Assets\Dependencies\frozen_inference_graph.pb'

# Read Pretrained Model
model = cv.dnn_DetectionModel(frozen_model, config)

# Model Setup
model.setInputSize(320, 320)
model.setInputScale(1.0/ 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

# Labels
lables = open('coco-labels.txt', 'r').read().rstrip('\n').split('\n')
print(f">> Loaded {len(lables)} classes...")


# // -- OpenCV Read Video (frames) --
# VideoCapture(0)       : 0 = Default Camera
# VideoCapture(1)       : 1 = External Camera
# VideoCapture(addr)    : addr = Path to Video File
video = cv.VideoCapture(0)

## Checks if camera opened successfully
if not video.isOpened():
    video = cv.VideoCapture(0)
if not video.isOpened():
    raise IOError("Cannot Open Video")

## Webcam Settings
video.set(cv.CAP_PROP_FRAME_WIDTH, 500)
video.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# Main Function
looptime = time() # Time Bookmark
while True:
    count = 0
    left_count = 0
    right_count = 0
    ret,frame = video.read()

    if(toMirror):
        frame = cv.flip(frame, 1)

    roi_left = frame[0:1280, 0:640]
    classIndex, confidence, bbox = model.detect(frame, threshold)


    # print(classIndex)
    if(len(classIndex) != 0):
        for classIndex, confidence, bbox in zip(classIndex.flatten(), confidence.flatten(), bbox):
            if (classIndex <= 80):
                if(lables[classIndex-1] == 'person'):                                                               # Filter so it displays only People
                    count +=1
                    cv.rectangle(frame, bbox, bbox_color, thickness)                                                # Draw Bounding Box
                    cv.putText(frame, lables[classIndex-1], (bbox[0], bbox[1]), font, font_scale, text_colour, 1)   # Draw Labels

                    # Bbox Tracking postiton (Using center point of Bbox)
                    # 0-> left top corner, 1-> left bottom corner, 2-> right bottom corner, 3-> right top corner

                    width = bbox[2] - bbox[1]   # Right Bottom - Left Bottom
                    height  = bbox[3] - bbox[0] # Right Top - Left Top
                    width_center_coord = int((bbox[0]+ (width/2)) + center_offset)

                    if height > (inital_height + jump_offset):
                        print("JUMPED")
                        pyautogui.press('space') # Emulate Keyboard Press
                    else:
                        print("\n")
                    
                    frame = cv.circle(frame, (width_center_coord, bbox[1]), 3, (255,255,255), thickness)

                    if (width_center_coord > 640):
                        right_count += 1
                    else:
                        left_count += 1

    # FPS Calculation & output
    fps = (1/(time() - looptime))
    looptime = time()

    # Display OpenCV Video Result
    frame = cv.line(frame,(640,0),(640,1000),(255,255,255),7)   # Draw Center Line
    
    if(header):                                                                                                                     # Toggle Headers
        frame = cv.putText(frame, 'Header_1', (220,60), font, header_scale, header_color, header_thickness, cv.LINE_AA)             # Display Left Header
        frame = cv.putText(frame, 'Header_2', (920,60), font, header_scale, header_color, header_thickness, cv.LINE_AA)             # Display Right Header
        
    if(debug):                                                                                                                      # Toggle Debug
        frame = cv.putText(frame, 'Human Detection Demo', (20,610), font, font_scale, debug_Colour, 1, cv.LINE_AA)                  # Display Project Name
        frame = cv.putText(frame, 'Human Detection Demo', (20,610), font, font_scale, debug_Colour, 1, cv.LINE_AA)                  # Display Project Name (Duplicated for opacity bold)
        frame = cv.putText(frame, f'FPS: {fps}', (20,640), font, debug_fontScale, debug_Colour, 1, cv.LINE_AA)                      # Display FPS Count
        frame = cv.putText(frame, f'Left Count: {left_count}', (20,670), font, debug_fontScale, debug_Colour, 1, cv.LINE_AA)        # Display Left Count
        frame = cv.putText(frame, f'Right Count: {right_count}', (20,700), font, debug_fontScale, debug_Colour, 1, cv.LINE_AA)      # Display Right Count
        frame = cv.putText(frame, f'Timer: Xs', (1130,700), font, debug_fontScale, debug_Colour, 1, cv.LINE_AA)                     # Display Timer
    cv.imshow(f'Human Detection [Demo]', frame)
    
    
    # Exit on 'ESC' Key
    if cv.waitKey(1) == 27: 
        break 

    # Calibrate Height
    if cv.waitKey(1) == ord('k'):
        inital_height = height
        print("Calibrated Height")
       
video.release()
cv.destroyAllWindows()