from deepface import DeepFace
import cv2 as cv 

img = cv.imread('assets/button_1.png')

preds = DeepFace.analyze(img)
