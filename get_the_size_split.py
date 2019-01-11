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


def _get_mode(arr):  # 求众�?
    mode = []
    arr_appear = dict((a, arr.count(a)) for a in arr)
    if max(arr_appear.values()) == 1:
        return
    else:
        for k, v in arr_appear.items():
            if v == max(arr_appear.values()):
                mode.append(k)
                # mode = k
    return mode

def _get_average_(arr):
    tmp=0
    for i in arr:
        tmp+= i
    if len(arr)!=0:
        return tmp/len(arr)
    else:
        print('erros,len(arr)=0')

def _get_instance_scale(xmlpath):
    xml = objectify.parse(open(xmlpath))
    root = xml.getroot()
    xmin = []
    ymin = []
    xmax = []
    ymax = []
    scale = []
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
                area = w_i * h_i
                if area < 0.000:
                    print("erros")
                    # area = -1.0* area
                scale.append(math.sqrt(area))
    scale = np.array(scale)
    scale_avg = _get_average_(scale)
    return scale_avg


def instance_per_images_from_txt(txtpath,xml_path):
    # 计算划分后的数据集，统计图像个数和instances个数
    bbox_num =[]
    txt_file = open(txtpath, 'r')
    lines = txt_file.readlines()
    for line in lines:
        name = line[:-1]
        xmlname = name + '.xml'
        xmlfile_path = os.path.join(xml_path,xmlname)
        xml = objectify.parse(open(xmlfile_path))
        num=0
        root = xml.getroot()
        for tmp in root.getchildren():
            if tmp.tag == 'object':
                num = num +1
            continue
        bbox_num.append(num)

    bbox_num = np.array(bbox_num)
    total_img =len(bbox_num)
    sum = bbox_num.sum()
    return total_img,sum


def get_the_xmlname_for_different_scale_insect_from_txt(txtpath,xmlspath):
    txt_file = open(txtpath, 'r')
    lines = txt_file.readlines()
    small_list=[]
    medium_list =[]
    big_list=[]
    extremely_small=[]
    for line in lines:
        name = line[:-1]
        xmlname = name + '.xml'
        xml_path = os.path.join(xmlspath, xmlname)
        object_scale_avg = _get_instance_scale(xml_path)
        # print(object_scale_avg)
        # if object_scale_avg <64 and object_scale_avg > 32:
        #     extremely_small.append(name)
        # if object_scale_avg < 80:
            # small_list.append(name)
        # elif object_scale_avg >= 140:
            # big_list.append(name)
        # else:
            # medium_list.append(name)
        if object_scale_avg < 32:
            small_list.append(name)
        elif object_scale_avg >= 64:
            big_list.append(name)
        else:
            medium_list.append(name)

    lists = [small_list, medium_list, big_list]
    return lists


# def get_the_xmlname_for_different_scale_insect(xmlspath):
#     small_list=[]
#     medium_list =[]
#     big_list=[]
#     extremely_small=[]
#     xmls = os.listdir(xmlspath)
#
#     for xml in xmls:
#         xml_path = os.path.join(xmlspath, xml)
#         name = xml[:-4]
#         object_scale_avg = _get_instance_scale(xml_path)
#         print(object_scale_avg)
#         # if object_scale_avg <64 and object_scale_avg > 32:
#         #     extremely_small.append(name)
#         if object_scale_avg < 80.0:
#             small_list.append(name)
#         elif object_scale_avg >= 140.0:
#             big_list.append(name)
#         else:
#             medium_list.append(name)
#
#     lists = [small_list, medium_list, big_list]
#     return lists

def create_test_txt(savepath,list):
    # ftest_S = open(os.path.join(savepath, 'test_small.txt'), 'w')
    ftest_S = open(os.path.join(savepath, 'test_small_32.txt'), 'w')
    for line in list[0]:
        name = line + '\r'
        # print("small_list",name)
        ftest_S.write(name)
    ftest_S.close()
    # ftest_M = open(os.path.join(savepath, 'test_medium.txt'), 'w')
    ftest_M = open(os.path.join(savepath, 'test_small_32-64.txt'), 'w')
    for line in list[1]:
        name = line + '\r'
        # print("medium_list", name)
        ftest_M.write(name)
    ftest_M.close()
    # ftest_B = open(os.path.join(savepath, 'test_big.txt'), 'w')
    ftest_B = open(os.path.join(savepath, 'test_small_64.txt'), 'w')
    for line in list[2]:
        name = line + '\r'
        # print("big_list", name)
        ftest_B.write(name)
    ftest_B.close()
    


if __name__ == '__main__':
    savepath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/ImageSets/Main"
    #txtspath =  ['test_small.txt','test_medium.txt','test_big.txt']
    txtpath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/ImageSets/Main/test_small.txt"
    xmlspath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/Annotations/"
    lists = get_the_xmlname_for_different_scale_insect_from_txt(xmlspath=xmlspath,txtpath=txtpath)
    create_test_txt(savepath=savepath,list=lists)
    # for txt in txtspath:
        # path = os.path.join(savepath,txt)
        # image_number,instance_number = instance_per_images_from_txt(txtpath=path,xml_path=xmlspath)
        # print(image_number,instance_number)
    # sp = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/sticky_board/2017_10_25/"
    # xp = sp+"/Annotations/"
    # tp = sp+"/imgname_list.txt"
    # lists, extremely_small = get_the_xmlname_for_different_scale_insect_from_txt(txtpath=tp,xmlspath=xp)
    # print("s:", len(lists[0]))
    # print("m:", len(lists[1]))
    # print("b:", len(lists[2]))






