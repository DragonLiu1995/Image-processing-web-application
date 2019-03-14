# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 00:50:33 2019

@author: LXL
"""
import numpy as np
import scipy.sparse
import cv2
from kmeans import kmeans
import scipy.stats
import time
class GMM(kmeans):
    def __init__(self, data, clusters):
        super().__init__(data, clusters)
        self.Sigma = []
        self.prior = []

    '''
    @params:
            X - M by N by 3
            clusters - How many clusters
            max_iter - Maximum iterations
    @return - a GMM params_list
    '''
    def train(self, max_iter=10):
        self.initialize_stat()
        iter_cur = 0
        while iter_cur < max_iter:
            MAP_prob = self.Estep()
            self.Mstep(MAP_prob)
            iter_cur += 1
        self.MAP_prob = self.Estep()

    def cluster(self):
         out = np.empty_like(self.data)
         idx = np.argmax(self.MAP_prob, axis=1)
         for i in range(self.M):
             for j in range(self.N):
                 out[i,j,:] = self.mu[idx[i * self.N + j]].astype(np.uint8)
         return out

    '''
     @params:
            X - M by N by 3
            clusters - How many clusters
    '''
    def initialize_stat(self):
        start = time.time()
        self.mu = self._kmeans_plus_init()
        size = self.M * self.N
        labels_dict = super().Estep(self.mu)
        for key, li in labels_dict.items():
            cur_cate = np.array(li)
            self.Sigma.append(np.cov(cur_cate, rowvar=False))
            self.prior.append(len(li) / size)
        end = time.time()
        print("time elapsed Init step: ", end - start, "s")

    def Estep(self):
        start = time.time()
        size = self.M * self.N
        MAP_prob = np.empty((size, self.clusters))
        data_reshape = np.reshape(self.data, (size, 3))
        for k in range(self.clusters):
            MAP_prob[:,k] = \
            self.prior[k] * scipy.stats.multivariate_normal.pdf(data_reshape,
                      self.mu[k], self.Sigma[k])
        sum_prob = np.sum(MAP_prob, axis=1, keepdims=True)
        MAP_prob = MAP_prob / sum_prob
        end = time.time()
        print("time elapsed E step: ", end - start, "s")
        return MAP_prob

    def Mstep(self, MAP_prob):
        start = time.time()
        prior = np.sum(MAP_prob, axis=0)
        self.prior = list(prior)
        size = self.M * self.N
        data_reshape = np.reshape(self.data, (size, 1, 3))
        prior_reshape = np.reshape(np.stack([prior] * size, axis=0), (size, -1, 1))
        MAP_reshape = np.stack([MAP_prob] * 3, axis=2)
        mu = np.sum(data_reshape * MAP_reshape / prior_reshape, axis=0)
        print(mu, "\n\n")
        self.mu = list(mu)
        mu_reshape = np.stack([mu] * size, axis=0)
        demean = data_reshape - mu_reshape
        Sigma = []
        for i in range(self.clusters):
            demean_i = demean[:,i,:]
            MAP_i = scipy.sparse.csr_matrix(
                      scipy.sparse.diags(list(MAP_prob[:,i]))
                    )
            cov = np.dot(demean_i.T, MAP_i.dot(demean_i)) / self.prior[i]
            Sigma.append(cov)
        self.Sigma = Sigma
        end = time.time()
        print("time elapsed M step: ", end - start, "s")

'''
img = cv2.imread('1.jpg')
print(img.shape)
model = GMM(img, 12)
model.train()
out = model.cluster()
cv2.imshow("segmented image using GMM", out)
cv2.waitKey()
'''
