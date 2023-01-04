# Modules (OpenCV, Matplotlib)
import cv2 as cv                    #pip install opencv-python
# import matplotlib.pyplot as plt    #pip install -U matplotlib
from time import time

# Load Files
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

# // Settings
font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 1
thickness = 2
colour = (0,255,0)

# Main program
cap = cv.imread('Assets\Test\jw-5d147f249c2d87.14657341.jpeg')

classIndex, confidence, bbox = model.detect(cap, confThreshold= 0.55)
print(classIndex, confidence, bbox)

for classIndex, confidence, bbox in zip(classIndex.flatten(), confidence.flatten(), bbox):
            if (classIndex <= 80):
                if(lables[classIndex-1] == 'person'):
                    cv.rectangle(cap, bbox, (0,255,0), thickness)
                    cv.putText(cap, lables[classIndex-1], (bbox[0]+10, bbox[1]+40), font, font_scale, colour, thickness)

capR = cv.resize(cap, (960, 640))
cv.imshow("",capR)
cv.waitKey(0)