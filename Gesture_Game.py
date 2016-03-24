import cv2
import numpy as np

#Load the Images for the Game
fog = cv2.imread('Foggy.jpg')
clear = cv2.imread('fog-wallpaper-2.jpg')

#blank_image = np.zeros((768,,3), np.uint8)
#change_image = Fog

#Start the Video Capture from the WebCam(Any Video Device)
cap = cv2.VideoCapture(0) # 0 is the ID of the Webcam, enter -1 to have OpenCV list all the connected Video Devices 
cap.set(3,768) # Set the Resolution of the Video
cap.set(4,480)
while( cap.isOpened() ) :
    ret,img = cap.read() 
    rows,columns,dim = img.shape
	# Convert the Frame to Grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# Reduce Noise and Edge Effects by Applying a Guassian Blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
	# Thresholding : Otsu's Binarization method 
    ret,thresh1 = cv2.threshold(blur,20,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  
	# Find the Contours
    _, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(img.shape,np.uint8)

    max_area=0
   
    for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
    cnt=contours[ci]
    area = cv2.contourArea(cnt)
    hull = cv2.convexHull(cnt)
    prev_hull = cv2.convexHull(cnt)
    prev_cnt = cnt
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00
              
    centr=(cx,cy)
	# Draw the Contours in the Output Image Frame
    cv2.circle(img,centr,5,[0,0,255],2)       
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
    cv2.drawContours(drawing,[hull],0,(255,0,255),thickness=-1) 
    #pts = np.where(drawing == (0,255,0))
	# Check for the Pixels where the Value of BGR is (255,0,255). This is set by the drawContours function and defines the Area under the Contour
	
    if (area>34000 and area<=65000):
		for i in range(rows):
			for j in range(columns):
				b,g,r = drawing.item(i,j,0),drawing.item(i,j,1),drawing.item(i,j,2)
				if (b == 255 and g == 0 and r == 255):
					# Replace the Pixels under the Contour with the Corresponding Pixels of the Other Image
					p1,p2,p3 = clear.item(i,j,0),clear.item(i,j,1),clear.item(i,j,2)
					fog.itemset((i,j,0),p1)
					fog.itemset((i,j,1),p2)
					fog.itemset((i,j,2),p3)
    
	# Finding Convexity Defects
	# To find convexity defects use fallowing while finding convex hull
    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt,returnPoints = False)
	
    # Plotting defects 
    if(1):
               defects = cv2.convexityDefects(cnt,hull)
               mind=0
               maxd=0
               for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    dist = cv2.pointPolygonTest(cnt,centr,True)
                    cv2.line(img,start,end,[0,255,0],2)
                    cv2.circle(img,far,5,[0,0,255],-1)
               #print "i=",i,"area=",area,"hull",hull,"prev_hull",prev_hull
               print "Points=",area # This is the Area under the Contour  
               i=0
    #change_image[hull] = Clear[hull]
    #cv2.imshow('final_game',change_image)
	# Plot the Corresponding Images   
    cv2.imshow('output',drawing)
    cv2.imshow('input',img)
	# Show the Game Window
    cv2.imshow('game',fog)
                
    k = cv2.waitKey(10)
    if k == 27:
        break
		
cap.release()
cv2.destroyAllWindows()
