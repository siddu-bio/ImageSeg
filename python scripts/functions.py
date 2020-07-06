import numpy as np
import cv2 as cv
import tifffile as tf 


#part 1: import image 

def open_image(img_name):
    img_name: str
    image_array = tf.imread(img_name)
    return image_array

def display_image(source):
    cv.resize(source)
    
    exit


#part 2: active contour identification

#2-1 

#2-2

#2-3 define local area

#part 3: energy minimization segmentation

#3-1

#####################################

#driver program

source: str = input()

source_data = open_image(source)

cv.imshow("test",source_data)
cv.waitKey(0)

#display_image(source)

