from EM import GMM
from kmeans import kmeans
from Ostu import Ostu_method
import cv2
import numpy as np

def segment_with_kmeans(clusters, img):
    print(img.shape)
    model = kmeans(img, clusters)
    model.train()
    out = model.cluster()
    out.astype(np.uint8)
    cv2.imwrite('k.jpg', out)
    return out

def segment_with_GMM(clusters, img):
    print(img.shape)
    model = GMM(img, clusters)
    model.train()
    out = model.cluster()
    cv2.imwrite('g.jpg', out)
    return out

def segment_with_Ostu(img):
  print(img.shape)
  thr = [Ostu_method(img[:,:,0]), Ostu_method(img[:,:,1]), Ostu_method(img[:,:,2])]
  out = np.zeros_like(img, dtype = np.uint8)
  for ch in range(3):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j, ch] <= thr[ch]:
                  out[i, j, ch] = 0
            else:
                  out[i, j, ch] = 255
  out = cv2.medianBlur(out, 15)
  cv2.imwrite('o.jpg', out)
  return out
