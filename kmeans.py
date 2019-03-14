# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 07:09:47 2019

@author: LXL
"""
import numpy as np
import cv2
import random

class kmeans:
    def __init__(self, data, clusters):
        self.data = data
        self.M, self.N, _ = data.shape
        self.clusters = clusters
        self.mu = []

    def _kmeans_plus_init(self):
        mu = []
        size = self.M * self.N
        idx = random.randint(0, size)
        mu.append(self.data[idx // self.N][idx % self.N])
        self.data_reshape = self.data.reshape((self.M * self.N, 1, 3))
        k = 1
        while k < self.clusters:
            prob = self._calc_dist_from_mean(mu)
            idx = np.random.choice(size, p=prob)
            mu.append(self.data[idx // self.N][idx % self.N])
            k += 1
        return mu

    def train(self, maxiter = 10):
        mu= self._kmeans_plus_init()
        labels_dict = self.Estep(mu)
        for iter_times in range(maxiter):
            prev_dict = labels_dict
            mu = self.Mstep(labels_dict)
            labels_dict = self.Estep(mu)
            print(mu)
            if (self._equals(prev_dict, labels_dict)):
                break
        self.mu = mu

    def cluster(self):
        out = np.zeros_like(self.data)
        for i in range(self.M):
            for j in range(self.N):
                dist_min = float("inf")
                arg_min = 0
                for k in range(len(self.mu)):
                    dist = np.linalg.norm(self.data[i][j]- self.mu[k])
                    if (dist_min > dist):
                        dist_min = dist
                        arg_min = k
                out[i][j] = self.mu[arg_min]
        return out

    def Estep(self, mu):
        labels_dict = dict(zip(range(self.clusters), [None] * self.clusters))
        for i in range(self.M):
            for j in range(self.N):
              dist_min = float("inf")
              label = 0
              for k in range(self.clusters):
                dist = np.linalg.norm(self.data[i][j] - mu[k])
                if dist < dist_min:
                    dist_min = dist
                    label = k
              if labels_dict[label] == None:
                  labels_dict[label] = []
              labels_dict[label].append(self.data[i][j])
        return labels_dict

    def Mstep(self, labels_dict):
        mu = []
        for _, li in labels_dict.items():
            length = len(li)
            sum_all = np.zeros((3,))
            for val in li:
                sum_all += val
            mu.append(sum_all / length)
        return mu

    def _calc_dist_from_mean(self, mu):
        k = len(mu)
        mu = np.array(mu)
        dist = np.linalg.norm(self.data_reshape - np.reshape(mu, (1,k,3)), axis = 2) ** 2
        dist_min = list(np.amin(dist, axis=1))
        total = sum(dist_min)
        prob = [p / total for p in dist_min]
        return prob

    def _equals(self, prev, cur):
        for key, val_li in prev.items():
            if not len(val_li) == len(cur[key]):
                return False
            idx = 0
            for val in val_li:
                if (not np.all(cur[key][idx] == val)):
                    return False
                idx += 1
        return True


'''
img = cv2.imread('1.jpg')
print(img.shape)
model = kmeans(img, clusters=20)

mu = model._kmeans_plus_init()
out = model.cluster()
out.astype(np.uint8)
cv2.imshow("segmented image", out)
cv2.waitKey()

model.train()

out = model.cluster()
out.astype(np.uint8)
cv2.imshow("segmented image", out)
cv2.waitKey()
'''
