# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 12:19:05 2019

@author: LXL
"""

import cv2
import numpy as np

def compute_hist(img):
    M, N = img.shape
    hist = [0] * 256
    for i in range(M):
        for j in range(N):
            hist[img[i][j]] += 1
    for i in range(256):
        hist[i] /= (M * N)
    return hist, M * N

def cumulative(hist):
    cum_sum = [0] * 256
    cum_mean = [0] * 256
    for i in range(len(hist)):
         cum_sum[i] = hist[i] + cum_sum[i - 1]
         cum_mean[i] = cum_mean[i - 1] + hist[i] * i
    return cum_mean, cum_sum
         
def Ostu_method(img):
    hist, size = compute_hist(img)
    cum_mean, cum_sum = cumulative(hist)
    global_mean = cum_mean[255]
    epi = 1e-10
    max_sig = 0
    thr = 0
    for i in range(256):
        sigma = (global_mean * cum_sum[i] / size - cum_mean[i] / size)**2 / ((cum_sum[i] / size) * (1 - cum_sum[i] / size) + epi)
        if max_sig < sigma:
            max_sig = sigma
            thr = i
    return thr

def main():
  img = cv2.imread('1.jpg')
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
  cv2.imshow("segmented image", out)
  cv2.waitKey()
  
if __name__ == '__main__':
    main()
