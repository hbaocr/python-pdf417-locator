import numpy as np
import random as rng
import matplotlib.pyplot as plt
import cv2



def getOpenCVVersion():
    ver=cv2.__version__
    print(cv2.__version__)
    return ver

def displayImgs(img_arr,titles=[]):
    l=len(img_arr)
    lt=len(titles)
    for i in range(0,l):
        plt.subplot(l,1,i+1)
        plt.imshow(img_arr[i],cmap='gray')
        if (lt-1)>=i:
            plt.title(titles[i])

    
def filterByArea(contours,thr):
    pdf417=[]
    for c in contours:
        if cv2.contourArea(c)>thr:
            pdf417.append(c)
    return pdf417


#https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/

def crop_rect2(img_src, rect,reserved=1.2):
    # I wanted to show an area slightly larger than my min rectangle set this to one if you don't 
    mult=reserved
    img = img_src.copy()
    
    # get the parameter of the small rectangle
    center, size, angle = rect[0], rect[1], rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    newzise=(int(size[0]*mult),int(size[1]*mult))
    rect1 = (center,newzise,angle)
    box = cv2.boxPoints(rect1)
    box = np.int0(box)
    # get width and height of the detected rectangle
    width = int(newzise[0])
    height = int(newzise[1])
    
    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened: 
    # in the top-left, top-right, bottom-right, and bottom-left order
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")
    


    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    # directly warp the rotated rectangle to get the straightened rectangle
    img_crop = cv2.warpPerspective(img, M, (width, height))
    return img_crop

def preProcessingImg(img):
    imagem = cv2.bitwise_not(img)
    kernel=np.zeros((5,1),np.uint8)
    rr=cv2.morphologyEx(imagem,cv2.MORPH_CLOSE,kernel,5)
    rr1=cv2.bitwise_not(rr)
    return rr1
    

def locatePDF417(gray):
    kernel = np.ones((21,21),np.uint8)
    op = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)
    #op = cv2.dilate(gray,kernel)
    thr_value,thr_img = cv2.threshold(op,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    img1 = cv2.morphologyEx(thr_img,cv2.MORPH_OPEN,kernel)
    # for opencv 3.x
    #modified_image, contours, hierarchy = cv2.findContours(img1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #opencv 4.x
    contours, hierarchy = cv2.findContours(img1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
   
    area_thr = gray.shape[0]*gray.shape[1]/36
    cnts=filterByArea(contours,area_thr)
    #print("Number of Contours is: " + str(len(cnts))+"/"+str(len(contours)))
    img_out=[]
    for c in cnts:
        rect=cv2.minAreaRect(c)
        margin_percent=1.2
        img_child=crop_rect2(gray,rect,margin_percent)
        (h,w)=img_child.shape[:2]
        
        if(h>w):
            img_child=cv2.rotate(img_child,cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        img_child=preProcessingImg(img_child)
        img_out.append(img_child)

    return img_out

########################################################################
img = cv2.imread('/Volumes/Data/AnacondaWorkspace/t4.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
child=locatePDF417(gray)
child.append(img)
displayImgs(child)

cv2.imwrite('c1.jpg',child[0])


