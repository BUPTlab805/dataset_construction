#!/usr/bin/python
# encoding:utf-8

import cv2
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.mlab as mlab
import numpy as np
from lxml import objectify
import os
import math
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn import cluster

def get_data(xmlpath):
    bbox=[]
    xmls = os.listdir(xmlpath)
    for xml in xmls:
        xmlfile_path = os.path.join(xmlpath, xml)
        xml = objectify.parse(open(xmlfile_path))
        root = xml.getroot()
        xmin = []
        ymin = []
        xmax = []
        ymax = []
        for tmp in root.getchildren():
           if tmp.tag == 'object':
                obj = tmp
                for child in obj.getchildren():
                    if child.tag == 'bndbox':
                        for coordinate in child.getchildren():
                            if coordinate.tag == 'xmin':
                                xmin.append(coordinate.pyval)
                            if coordinate.tag == 'ymin':
                                ymin.append(coordinate.pyval)
                            if coordinate.tag == 'xmax':
                                xmax.append(coordinate.pyval)
                            if coordinate.tag == 'ymax':
                                ymax.append(coordinate.pyval)
        if len(xmin) != 0:
            for i in range(len(xmin)):
                w_i = abs(xmax[i] - xmin[i])
                h_i = abs(ymax[i] - ymin[i])
                if h_i!=0:
                    ratio= w_i/h_i
                    bbox.append((w_i,h_i,ratio))

    bbox= np.array(bbox)

    return bbox



if __name__ == '__main__':
    xmlpath= "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/RGBInsectpapers/VOC2007/Annotations/"
    data = get_data(xmlpath)
    # data = np.random.rand(100,2)
    estimator = KMeans(n_clusters=5)
    res= estimator.fit_predict(data)
    label_pred = estimator.labels_
    centroids = estimator.cluster_centers_
    intertia = estimator.inertia_

    print(res)
    print(label_pred)
    print(centroids)
    print(intertia)

    for i in range(len(data)):
        if int(label_pred[i])==0:
            plt.scatter(data[i][0],data[i][1],color='red')
        if int(label_pred[i])==1:
            plt.scatter(data[i][0],data[i][1],color='black')
        if int(label_pred[i])==2:
            plt.scatter(data[i][0],data[i][1],color='blue')
        if int(label_pred[i])==3:
            plt.scatter(data[i][0],data[i][1],color='green')
        if int(label_pred[i])==4:
            plt.scatter(data[i][0],data[i][1],color='yellow')
    plt.show()
