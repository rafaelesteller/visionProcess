import cv2
import numpy as np
import math
from Utilities import norm
keys = ["found", "orientation", "centerPointX", "centerPointY"]
ort = "orientation"
cpY = "centerPointY"
cpX = "centerPointX"
found = "found"

def ProcessFrame(frame):
  out = {}
  out[ort] = -400
  out[cpX] = 0
  out[cpY] = 0
  out[found] = False
  pRed = frame[:, :, 2]
  frame = norm(frame)
  red = frame[:,:,2]
  debugFrame("red", red)
  (row, col, pages) = frame.shape
  maxArea = (row * col)/3
  minArea = 200
  red = cv2.medianBlur(red, ksize = 3)
  ret, thresh = cv2.threshold(red, 120, 255, cv2.THRESH_BINARY)
  debugFrame("threshOg", thresh)
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)
  res, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  possiblePoles = []
  for cont in contours:
    (center, (w, h), ang) = cv2.minAreaRect(cont)
    area = w * h
    aspectRatio = 0
    if w != 0:
      aspectRatio = h / w
    if aspectRatio < 1 and aspectRatio != 0:
    	aspectRatio = 1/aspectRatio
    
    
    if area > 1000 and aspectRatio > 3 and aspectRatio < 13:
      angp = abs(ang)
      angp = abs(angp - round((angp/90.0)) * 90)
      loc = (int(center[0]), int(center[1]))
      cv2.drawContours(frame, [cont], -1, (0,0, 0), 3)
      [vx,vy,x,y] = cv2.fitLine(cont, cv2.DIST_L2,0,0.01,0.01)
      if vx  > .01:
        lefty = int((-x*vy/vx) + y) 
        righty = int(((col-x)*vy/vx)+y) 
        cv2.line(frame,(col-1,righty),(0,lefty),(0,255,0),2)
      angm = math.degrees(math.atan2(vy,vx))
      angM = angm - round((angm/90.0)) * 90
      stringOut = "angP %.2f, asp %.2f" % (angM, aspectRatio)
      cv2.putText(frame, stringOut, loc, cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
      out[ort] = int(angM)
      out[cpY] = center[1]
      out[cpX] = center[0]
      out[found] = True
      
  	  
  debugFrame("out", frame)
  return out

def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
