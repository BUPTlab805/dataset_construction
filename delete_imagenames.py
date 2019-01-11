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

def create_test_txt(savepath,list):
    ftest_S = open(os.path.join(savepath, 'train.txt'), 'w')
    for line in list[0]:
        name = line + '\r'
        # print("small_list",name)
        ftest_S.write(name)
    ftest_S.close()
    ftest_M = open(os.path.join(savepath, 'trainval.txt'), 'w')
    for line in list[1]:
        name = line + '\r'
        # print("medium_list", name)
        ftest_M.write(name)
    ftest_M.close()
    ftest_B = open(os.path.join(savepath, 'test.txt'), 'w')
    for line in list[2]:
        name = line + '\r'
        # print("big_list", name)
        ftest_B.write(name)
    ftest_B.close()
    ftest_ES = open(os.path.join(savepath, 'val.txt'), 'w')
    for line in list[3]:
        name = line + '\r'
        # print("small_extremely_list", name)
        ftest_ES.write(name)
    ftest_ES.close()

path = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007---/"
Anno_path = path + 'Annotations/'
# jpeg_path = path + 'JPEGImages'
txts = [ 'train','trainval','test','val']
txt_dir = path + "ImageSets/Main0/"
save_path = path + "ImageSets/Main/"
# Annotations = os.listdir(Anno_path)

train_lines=[]
trainval_lines=[]
test_lines=[]
val_lines=[]
new_lines = [train_lines,trainval_lines,test_lines,val_lines]
for idx,txt in enumerate(txts):
    txtpath = txt_dir+txt+'.txt'
    txt_file = open(txtpath, 'r')
    lines = txt_file.readlines()
    print(txtpath)
    for line in lines:
        xml_path = Anno_path + line[:-1] + ".xml"
        # print(xml_path)
        if os.path.exists(xml_path):
            print(xml_path)
            new_lines[idx].append(line[:-1])
            print('matched')
        else:
            print("empty_____________")
            continue
create_test_txt(save_path,new_lines)



