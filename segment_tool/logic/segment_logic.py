import cv2
import os
import numpy as np
from PIL import Image 
from django.core.files.base import ContentFile
from io import BytesIO

#temp 
import pdb

KERNEL_INT = 48
WIDTH_DILATION = 112 
IMG_KERNEL = (KERNEL_INT, KERNEL_INT)


class BoundingBox ():
    def __init__(self, x,y,w,h, label):
        self.x1= x
        self.y1= y
        self.x2= x+w
        self.y2= y+h
        self.w = w
        self.h = h
        self.label = label

    def __str__ (self):
        return ( str(self.label) + ' : '+ '('+str(self.x1) +', '+str(self.y1)+')'+'\t' + '('+str(self.x2) +', '+str(self.y2)+')')
        
        
def check_overlap (b1, b2):
    return (b1.x1 < b2.x2 and b1.x2 > b2.x1 and b1.y1 < b2.y2 and b1.y2 > b2.y1)

#boxes: [ [x,y,w,h]...]
def merge_bounding_boxes(boxes):
    #process so that box list always starts from top left to bottom right
    boxes = sorted(boxes, key=lambda x:(x.y1, x.x1))
    for i in boxes:
        print(i.label)
    for i in range(len(boxes)):
        j = i+1
        while j < len(boxes):
            if (check_overlap(boxes[i],boxes[j])):
#                print(boxes[i].label, boxes[j].label, sep='\t')
                boxes[i].x1 = min(boxes[i].x1, boxes[j].x1)
                boxes[i].y1 = min(boxes[i].y1, boxes[j].y1)
                boxes[i].x2 = max(boxes[i].x2, boxes[j].x2)
                boxes[i].y2 = max(boxes[i].y2, boxes[j].y2)
                del boxes[j]
                j=i+1
                continue
            j+= 1

    return boxes 

#source: https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
def get_bounding_boxes (img, img_kernel = IMG_KERNEL, width_dilation = WIDTH_DILATION) :
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #mat, can show
     
    # Performing OTSU threshold 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    # Specify structure shape and kernel size.  
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, img_kernel) 
    # Appplying dilation on the threshold image 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) #mat, can show 
    # Finding contours 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,  
                                                     cv2.CHAIN_APPROX_NONE)
    # Looping through the identified contours
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        boxes.append( BoundingBox(x,y,w,h,len(boxes)) )  

    #merge bounding boxes
    boxes = merge_bounding_boxes(boxes)
    boxes = sorted(boxes, key = lambda x:(  int(x.w/width_dilation), x.x1, x.y1))
       
    return boxes 

#pil image 
def resize_image (img, width, height): 
    if img.size[0] > width or img.size[1] > height:
        new_img = img.resize((width, height))
    return new_img

'''   
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))
    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)
    # return the resized image
    return resized
''' 

#returns PIL image 
def extract_jpg_regions (django_image, width, height, img_kernel = IMG_KERNEL, width_dilation = WIDTH_DILATION): 
    img = cv2.imdecode(np.fromstring(django_image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    boxes = get_bounding_boxes(img, img_kernel, width_dilation)
    index = 0
    for box in boxes:
        cv2.rectangle(img, (box.x1, box.y1), (box.x2, box.y2), (0,255,0), 2)
        cv2.putText(img, str(index), (box.x1, box.y1), cv2.FONT_HERSHEY_SIMPLEX, 10, (255,255,255))
    
    #convert to ContentFile
    #https://stackoverflow.com/questions/32945292/how-to-save-pillow-image-object-to-django-imagefield
    pil_img = Image.fromarray(img, 'RGB')
    #pil_img = resize_image(pil_img, width, height)
    buffer = BytesIO() 
    pil_img.save(fp=buffer, format='JPEG')     
    return os.path.basename(django_image.url), ContentFile(buffer.getvalue()) 

