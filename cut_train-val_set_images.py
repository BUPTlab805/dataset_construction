#encoding:utf-8
#根据划分的训练集和测试集剪切图片
from lxml import objectify
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt

#根据txt文件中的名称，读取xml文件，
def cutimages_txt(txtpath,xmlpath,imagepath,outputpath):
    num = 0
    txt_file = open(txtpath, 'r')
    lines = txt_file.readlines()
    for line in lines:
        name = line[:-1]
        xmlname = name + '.xml'
        imgname = name + '.jpg'
        xml_path = os.path.join(xmlpath,xmlname)
        img_path = os.path.join(imagepath,imgname)
        if not os.path.exists(img_path):
            imgname = name +'.BMP'
            img_path = os.path.join(imagepath,imgname)
        img = plt.imread(img_path)
        xml = objectify.parse(open(xml_path))
        root = xml.getroot()
        for tmp in root.getchildren():
            if tmp.tag == 'object':
                obj = tmp
                for child in obj.getchildren():
                    if child.tag =='name':
                        label = child.pyval
                        if os.path.exists(os.path.join(outputpath,label)):
                            save_file_path = os.path.join(outputpath,label)
                        else :
                            os.mkdir(os.path.join(outputpath,label))
                            save_file_path = os.path.join(outputpath, label)

                    if child.tag == 'bndbox':
                        x1 = child.xmin.pyval
                        y1 = child.ymin.pyval
                        x2 = child.xmax.pyval
                        y2 = child.ymax.pyval
                        if ((x2 - x1) >= 1) & ((y2 - y1) >= 1):
                            num = num + 1
                            ss_img = img[y1:y2, x1:x2, :]
                            s_img = ss_img.copy()
                            if not os.path.exists(save_file_path):
                                os.mkdir(save_file_path)
                            save_path = os.path.join(save_file_path, 'testval_mobile'+str(num) + label+'.jpg')
                            plt.imsave(save_path, s_img)
                            print (num)
                    continue
            continue

def cutimages(beginnum,xmlpath,imagepath,outputpath):
    num = beginnum
    xmls = os.listdir(xmlpath)
    for xml in xmls:
        xml_path = os.path.join(xmlpath, xml)
        imgname= xml[:-4]+'.jpg'
        img_path = os.path.join(imagepath, imgname)
        img = plt.imread(img_path)
        xml = objectify.parse(open(xml_path))
        root = xml.getroot()
        for tmp in root.getchildren():
            if tmp.tag == 'object':
                obj = tmp
                for child in obj.getchildren():
                    if child.tag == 'name':
                        label = child.pyval
                        if os.path.exists(os.path.join(outputpath, label)):
                            save_file_path = os.path.join(outputpath, label)
                        else:
                            os.mkdir(os.path.join(outputpath, label))
                            save_file_path = os.path.join(outputpath, label)

                    if child.tag == 'bndbox':
                        x1 = child.xmin.pyval
                        y1 = child.ymin.pyval
                        x2 = child.xmax.pyval
                        y2 = child.ymax.pyval
                        if ((x2 - x1) >= 1) & ((y2 - y1) >= 1):
                            num = num + 1
                            ss_img = img[y1:y2, x1:x2, :]
                            s_img = ss_img.copy()
                            if not os.path.exists(save_file_path):
                                os.mkdir(save_file_path)
                            save_path = os.path.join(save_file_path, str(num) + label + '.png')
                            plt.imsave(save_path, s_img)
                            print(num)
                    continue
            continue

if __name__ == '__main__':
    txtpath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/ImageSets/Main/testval.txt"
    xmlpath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/Annotations/"
    imagepath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/JPEGImages/"
    outputpath = "/home/ubuntu/lijiangtao/keras_classification/data/single_insect_images/Test"
    if os.path.exists(outputpath)==0:
        os.mkdir(outputpath)
    cutimages_txt(txtpath, xmlpath, imagepath, outputpath)

