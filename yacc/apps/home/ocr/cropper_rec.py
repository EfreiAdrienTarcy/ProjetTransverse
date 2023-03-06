import cv2
import numpy as np
import os

def card_or_not(thresh,maxnbcard):  
    CARD_MAX_AREA = 2000000
    CARD_MIN_AREA = 100000
    MAX_CARD_NB = maxnbcard
    # Find contours and sort their indices by contour size
    cnts,hier = cv2.findContours(image=thresh,mode=cv2.RETR_TREE,method=cv2.CHAIN_APPROX_SIMPLE)
    index_sort = sorted(range(len(cnts)), key=lambda i : cv2.contourArea(cnts[i]),reverse=True)


    # Otherwise, initialize empty sorted contour and hierarchy lists
    cnts_sort = []
    hier_sort = []
    cnt_is_card = []

    # Fill empty lists with sorted contour and sorted hierarchy. Now,
    # the indices of the contour list still correspond with those of
    # the hierarchy list. The hierarchy array can be used to check if
    # the contours have parents or not.
    for i in index_sort:
        cnts_sort.append(cnts[i])
        hier_sort.append(hier[0][i])

    # Determine which of the contours are cards by applying the
    # following criteria: 1) Smaller area than the maximum card size,
    # 2), bigger area than the minimum card size, 3) have no parents,
    # and 4) have four corners
    size_list=[]
    contourlist=[]

    #determining avg contour size
    for i in range(len(cnts_sort)):
        contourlist.append(cv2.contourArea(cnts_sort[i]))
    size_avg=np.sum(contourlist)/MAX_CARD_NB



    for i in range(len(cnts_sort)):

        size_list.append((i,cv2.contourArea(cnts_sort[i])))
        size = cv2.contourArea(cnts_sort[i])
        peri = cv2.arcLength(cnts_sort[i],True)
        approx = cv2.approxPolyDP(cnts_sort[i],0.01*peri,True)

            
        if ((size > 0.7*size_avg) and (size < MAX_CARD_NB*size_avg) #(size < CARD_MAX_AREA) and (size > CARD_MIN_AREA) avant
            and (hier_sort[i][3] == -1 or hier_sort[i][2]==-1) and (len(approx) == 4)):

            cnt_is_card.append(i)
    return [cnts_sort[i] for i in cnt_is_card]

def flattener(image, pts, w, h):
    """Flattens an image of a card into a top-down 200x300 perspective.
    Returns the flattened, re-sized, grayed image.
    See www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/"""
    temp_rect = np.zeros((4,2), dtype = "float32")
    
    s = np.sum(pts, axis = 2)

    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]

    diff = np.diff(pts, axis = -1)
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]

    # Need to create an array listing points in order of
    # [top left, top right, bottom right, bottom left]
    # before doing the perspective transform

    if w <= 0.8*h: # If card is vertically oriented
        temp_rect[0] = tl
        temp_rect[1] = tr
        temp_rect[2] = br
        temp_rect[3] = bl

    if w >= 1.2*h: # If card is horizontally oriented
        temp_rect[0] = bl
        temp_rect[1] = tl
        temp_rect[2] = tr
        temp_rect[3] = br

    # If the card is 'diamond' oriented, a different algorithm
    # has to be used to identify which point is top left, top right
    # bottom left, and bottom right.
    
    if w > 0.8*h and w < 1.2*h: #If card is diamond oriented
        # If furthest left point is higher than furthest right point,
        # card is tilted to the left.
        if pts[1][0][1] <= pts[3][0][1]:
            # If card is titled to the left, approxPolyDP returns points
            # in this order: top right, top left, bottom left, bottom right
            temp_rect[0] = pts[1][0] # Top left
            temp_rect[1] = pts[0][0] # Top right
            temp_rect[2] = pts[3][0] # Bottom right
            temp_rect[3] = pts[2][0] # Bottom left

        # If furthest left point is lower than furthest right point,
        # card is tilted to the right
        if pts[1][0][1] > pts[3][0][1]:
            # If card is titled to the right, approxPolyDP returns points
            # in this order: top left, bottom left, bottom right, top right
            temp_rect[0] = pts[0][0] # Top left
            temp_rect[1] = pts[3][0] # Top right
            temp_rect[2] = pts[2][0] # Bottom right
            temp_rect[3] = pts[1][0] # Bottom left
            
        
    maxWidth = 600
    maxHeight = 1000

    # Create destination array, calculate perspective transform matrix,
    # and warp card image
    dst = np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0, maxHeight-1]], np.float32)
    M = cv2.getPerspectiveTransform(temp_rect,dst)
    warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    #warp = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)

        

    return warp

def contours_detailer(contour):
    # Find perimeter of card and use it to approximate corner points
    peri = cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,0.01*peri,True)
    pts = np.float32(approx)
    points = pts

    # Find width and height of card's bounding rectangle
    x,y,w,h = cv2.boundingRect(contour)
    width, height = w, h

    # Find center point of card by taking x and y average of the four corners.
    average = np.sum(pts, axis=0)/len(pts)
    cent_x = int(average[0][0])
    cent_y = int(average[0][1])
    center = [cent_x, cent_y]

    return pts,w,h,center



def crop(image):
    # read the image
   # image = cv2.imread(image)#avec contour.jpg
    image_inverted = np.invert(image)

    # convert the image to grayscale format
    img_gray = cv2.cvtColor(image_inverted, cv2.COLOR_BGR2GRAY)

    # apply binary thresholding
    ret, thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)

    contours=card_or_not(thresh,10)  

    images=[]
    # see the results
    for i,contour in enumerate(contours):

        pts,w,h,center=contours_detailer(contour)
        warp = flattener(image, pts, w, h)
        x=400
        y=710
        w=145
        h=40
        warp = warp[y:y+h,x:x+w]
        images.append(warp)
    return images


