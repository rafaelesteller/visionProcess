import numpy as np
import cv2
import math

keys = ["test1", "test2"]

def ProcessFrame(frame):
  out = {}
  out["test1"] = 1
  out["test2"] = 2
  orig = np.copy(frame)
  #frame = frame[:,:,2]
  for i in range(0, 5):
    frame = cv2.GaussianBlur(frame, (7,7), 0)
  m = cv2.mean(frame)
  index = 0
  count = 0
  for val in m:
    if m[index] < val:
       index = count
    count = count + 1
    
  while ( m[index] > 8):
    sub = np.ones((np.shape(frame))) * m[0:3]
    sub = sub.astype(np.uint8)
    frame = cv2.subtract(frame, sub)
    m = cv2.mean(frame)
  green = frame[:, :, index]
  cv2.imshow(str(index), green)
  ret, thresh = cv2.threshold(green, 12, 255, cv2.THRESH_BINARY)
  cv2.imshow("orThresh", thresh)
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh, kernel)
  thresh = cv2.dilate(thresh, kernel)
  '''
  thresh = cv2.erode(thresh, kernel, iterations = 2)
  thresh = cv2.dilate(thresh,kernel, iterations = 1)
  thresh = cv2.dilate(thresh, kernel,iterations = 1) 
  '''
  cv2.imshow("thresh", thresh)
  
  res, contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for cont in contours:
    cont = cont.astype(np.float32)
    if len(cont) < 5:
      continue
    (center, (w, h), ang) = cv2.fitEllipse(cont)
    area = w * h
    angP = abs(abs(ang) - round((abs(ang)/90.0)) * 90)
    if h != 0 and w != 0:
      aspectRatio = w/h
      if aspectRatio < 1.0:
        aspectRatio = 1/aspectRatio
    else:
      aspectRatio = 10
    loc = (int(center[0]), int(center[1]))
    stringOut = "%d %d %d" % (angP, area, aspectRatio)
    box = cv2.boxPoints((center, (w,h), ang)) 
    box = np.int0(box)
    if area > 150 and area <7000 and aspectRatio < 1.7 and angP < 30:
      cv2.drawContours(orig, [box], -2, (0, 0, 255), 3)
    else:
      cv2.drawContours(orig, [box], -2, (0, 255, 0), 3)
      
    cv2.putText(orig, stringOut, loc, cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
  
  cv2.imshow("pro", orig)
  return out




