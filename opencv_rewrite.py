import cv2 as cv
import numpy as np 
import tifffile as tf
import pandas as pd
#import seaborn as sns


sourcelist = [
    "Ng.il6. drg ipl. 405 nf200, 488 cgrp mRNA, 568 arc mRNA, 647 P2X3 mRNA. Image 1 20x 20uspixel.tif",
    "Ng.il6. drgCL. 405 nf200, 488 cgrp mRNA, 568 arc mRNA, 647 P2X3 mRNA. Image 1 20x 20uspixel.tif",
    "Ng.il6. drgCL. 405 nf200, 488 cgrp mRNA, 568 arc mRNA, 647 P2X3 mRNA. Image 2 20x 20uspixel.tif"
    ]

#helper function for processing multilayer tiff files
def img_open(src_img,layers):
    original_image = tf.imread(src_img)
    layer_list = []
    for i in range(layers):
        layer_list.append(original_image[i])
    return layer_list
        
#helper function for displaying previews of processed images
def image_show(img,wkyes):
    out = cv.resize(img, (1100,1100))
    cv.imshow(None,out)
    if wkyes == True:
        cv.waitKey()

#helper function to categorize contours by area
def area(c,minarea,maxarea):
    area = cv.contourArea(c)
    if area > minarea and area < maxarea:
        return True
    else:
        return False

#helper function for colocalization of an image
def pearsons(img2,img1):
    #img1 numbers
    img1_average = np.mean(img1)

    #img2 numbers
    img2_average = np.mean(img2)

    #final calc
    pearson_num = np.sum(np.multiply((img1-img1_average),(img2-img2_average)))
    pearson_denom = np.sqrt(
            np.multiply(
                np.sum(np.square(img1-img1_average)),np.sum(np.square(img2-img2_average))
                )
            )
    pcc = pearson_num/pearson_denom
    return pcc

#main function kwargs for tissue types
def segment(source_image_name,channels,marker_layer):

    layers = img_open(source_image_name,channels)
    contour_layer = layers[marker_layer]
    blank = np.zeros_like(contour_layer)
    blank_temp = blank.copy()
    contour = cv.normalize(contour_layer,None,alpha=0,beta=65535,norm_type=cv.NORM_MINMAX)
    ret,threshold = cv.threshold(contour,1000,65535,cv.THRESH_BINARY)
    thresh =  threshold.copy().astype(np.uint8)
    canny = cv.Canny(thresh,50,255)
    contours,hierarchy = cv.findContours(canny,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cConts = []
    retryConts = []
    for contour in contours:
        if area(contour,100,160000) == True:
            cConts.append(contour)
        else:
            retryConts.append(contour)
    cols = ["area","NF200 & CGRP","NF200 & ARC","NF200 & P2X3","CGRP & ARC", "CGRP and P2X3", "ARC and P2X3"]
    data = []
    for i,contour in enumerate(cConts):
        render_image = cv.normalize(contour_layer,None,alpha=0,beta=65535,norm_type=cv.NORM_MINMAX)
        color = [65535,65535,65535]
        cv.drawContours(render_image,cConts,i,color,1)
        cv.drawContours(blank_temp,cConts,i,color,cv.FILLED)
        image_show(render_image,False)
        key = cv.waitKey(0)
        pcc_data = []
        if key == ord("y"):
            cont_area = cv.contourArea(contour)
            micron_area = (0.8045**2)*cont_area
            pcc_data.append(micron_area)
            mask = blank_temp.copy()
            c1 = layers[0].copy()
            c2 = layers[1].copy()
            c3 = layers[2].copy()
            c4 = layers[3].copy()
            channel1 = cv.bitwise_and(c1,mask)
            #image_show(channel1,True)
            ret,channel1 = cv.threshold(channel1,1000,65535,cv.THRESH_TOZERO)
            #image_show(channel1,True)
            channel2 = cv.bitwise_and(c2,mask)
            ret,channel2 = cv.threshold(channel2,1000,65535,cv.THRESH_TOZERO)
            #image_show(channel2,True)
            channel3 = cv.bitwise_and(c3,mask)
            ret,channel3 = cv.threshold(channel3,1000,65535,cv.THRESH_TOZERO)
            #image_show(channel3,True)
            channel4 = cv.bitwise_and(c4,mask)
            ret,channel4 = cv.threshold(channel4,1000,65535,cv.THRESH_TOZERO)
            #image_show(channel4,True)
            blank_temp = blank.copy()
            c1c2 = pearsons(channel1,channel2)
            pcc_data.append(c1c2)
            c1c3 = pearsons(channel1,channel3)
            pcc_data.append(c1c3)
            c1c4 = pearsons(channel1,channel4)
            pcc_data.append(c1c4)
            c2c3 = pearsons(channel2,channel3)
            pcc_data.append(c2c3)
            c2c4 = pearsons(channel2,channel4)
            pcc_data.append(c2c4)
            c3c4 = pearsons(channel3,channel4)
            pcc_data.append(c3c4)
            pcc_data = np.nan_to_num(pcc_data)
            data.append(pcc_data)
        else:
            continue
        cv.destroyAllWindows()
    df = pd.DataFrame(data,columns = cols)
    filename = source_image_name + "_coloc.xlsx"
    df.to_excel(filename)

for file in sourcelist:
    segment(file,4,1)