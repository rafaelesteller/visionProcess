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
  m = cv2.mean(frame)
  sub = np.ones((np.shape(frame))) * m[0:3]
  sub = sub.astype(np.uint8)
  frame = cv2.subtract(frame, sub)
  
  f = np.copy(frame)
  f = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
  cv2.imshow("gray", f)
  
  Z = frame.reshape((-1, 3))
  Z = np.float32(Z)
  criteria = ( cv2.TERM_CRITERIA_MAX_ITER, 1, 10.0)
  
  
  K = 10
  ret,label,center=cv2.kmeans(Z,K,None,criteria,1,cv2.KMEANS_PP_CENTERS)
  
  #ret, label, center = cv2.kmeans(Z, K, None, criteria, 1, cv2.KMEANS_USE_INITIAL_LABELS)
  
  center = np.uint8(center)
  res = center[label.flatten()]
  res2 = res.reshape((frame.shape))
  
  
  
  print center
  print "\n"
  print "\n"
  
  cv2.imshow("kmean", res2)
  """
  
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
  
  cv2.imshow("pro", orig) """
  return out




