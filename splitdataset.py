#encoding:utf-8
from math import log
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import shutil #复制文件
import re  #正则表达式模�?
import random


#计算给定数据集的香农�?
def calcShannonEnt(dataset):
    numEntries = len(dataset)
    labelCounts = {}
    for featVec in dataset :
        currentlabel = featVec[-1]
        if currentlabel not in labelCounts.keys():
            labelCounts[currentlabel] = 0
        labelCounts[currentlabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob* log(prob,2)
    return shannonEnt

#按照给定特征划分数据
def SplitDataSet (dataset , axis ,value):
    retDataSet = []
    for featVec in dataset :
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

#选择最好的数据集划分方�?
def choosebestfeaturetosplit(dataset):
    numFeatures = len(dataset[0])-1
    baseEntropy = calcShannonEnt(dataset)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataset]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = SplitDataSet(dataset,i,value)
            prob = len(subDataSet)/float(len(dataset))
            newEntropy += prob*calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature#

#随机采样划分数据集_每种虫子分别采样
def spilt_train_test(xmlfilepath,txtsavepath,trainval_percent,train_percent,label ):
    xmlfile = os.listdir(xmlfilepath)
    numofxml = len(xmlfile)

    list = range(numofxml)
    num_trainval = int(numofxml * trainval_percent)
    num_train = int(num_trainval * train_percent)
    trainval = random.sample(list, num_trainval)
    train = random.sample(trainval , num_train)

    ftrainval = open(os.path.join(txtsavepath,'trainval/'+label+'trainval.txt'), 'w')
    ftest = open(os.path.join(txtsavepath,'test/'+label+'test.txt'), 'w')
    ftrain = open(os.path.join(txtsavepath,'train/'+label+'train.txt'), 'w')
    fval = open(os.path.join(txtsavepath ,'val/'+label+'val.txt'), 'w')

    for i in list :
        name = xmlfile[i][:-4]+'\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train :
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

# 合并txt
def combine_txt(outputpath,txtspath,fname,insectlist):
    save_path = os.path.join(outputpath, fname+'.txt')
    txts_path = os.path.join(txtspath, fname)
    f = open(save_path, 'a')
    for label in insectlist:
        txtpath = os.path.join(txts_path, label + fname+'.txt')
        print(txtpath)
        txt_file = open(txtpath, 'r')
        lines = txt_file.readlines()
        f.writelines(lines)
    f.close()



# 直接划分数据�?
def spiltdatset(xmlfilepath,txtsavepath,trainval_percent,train_percent):
    xmlfile = os.listdir(xmlfilepath)
    numofxml = len(xmlfile)

    list_index= list(range(numofxml))
    np.random.shuffle(list_index)

    num_trainval = int(numofxml * trainval_percent)
    num_train = int(num_trainval * train_percent)
    trainval = random.sample(list_index, num_trainval)

    train = random.sample(trainval , num_train)


    ftrainval = open(os.path.join(txtsavepath,'trainval.txt'), 'w')
    ftest = open(os.path.join(txtsavepath,'test.txt'), 'w')
    ftrain = open(os.path.join(txtsavepath,'train.txt'), 'w')
    fval = open(os.path.join(txtsavepath ,'val.txt'), 'w')

    for i in list_index :
        name = xmlfile[i][:-4]+'\r'
        if i in trainval:
            ftrainval.write(name)
            if i in train :
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()


def spilit_dataset_imgs(path,trainval_percent,outputpath):
    labels = os.listdir(path)
    for label in labels:
        if len(label)>13 or label == 'labels.txt':
            continue
        imgdir= os.path.join(path,label)
        imgs = os.listdir(imgdir)
        numofimg = len(imgs)
        list_index = list(range(numofimg))
        np.random.shuffle(list_index)

        outdir_train = outputpath +'/train'
        outdir_test = outputpath +'/test'

        num_trainval = int(numofimg * trainval_percent)
        trainval = random.sample(list_index, num_trainval)

        for i in list_index:

            if i in trainval:
                outpath = os.path.join(outdir_train,label)
                if not os.path.exists(outpath):
                    os.mkdir(outpath)
                shutil.copyfile(os.path.join(imgdir, imgs[i]),os.path.join(outpath,imgs[i]))

            else:

                outpath = os.path.join(outdir_test, label)
                if not os.path.exists(outpath):
                    os.mkdir(outpath)
                shutil.copyfile(os.path.join(imgdir, imgs[i]), os.path.join(outpath, imgs[i]))


def calculate_img_num(path):
    labels = os.listdir(path)
    num =0
    for label in labels:
        imgdir= os.path.join(path,label)
        imgs = os.listdir(imgdir)
        num = num +len(imgs)
    return num




if __name__ == '__main__':
    # path= '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/cropped_img_dataset/mobile_smallview_for_app'
    # outp = '/home/ubuntu/lijiangtao/keras_classification/data/insetmobile_small_view'
    #
    # spilit_dataset_imgs(path,0.5,outp)
    xml_path = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCdevice2/VOC2007/Annotations/'
    txtsavepath = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCdevice2/VOC2007/ImageSets/Main/'
    trainval_percent = float(2/3)
    train_percent = float(2/3)
    spiltdatset(xml_path, txtsavepath, trainval_percent, train_percent)
    # 按虫种划分数�?
    # insect = ['ls', 'rd', 'tc', 'os', 'ct', 'so', 'sz', 'cp']
    #
    # # xml_path = r'D:\img-set\mobile\mobile_2017_7_4\mi\Annotations'
    # # txtsavepath = r"D:\img-set\mobile\mobile_2017_7_4\mi\txt_splitdataset"
    # xml_path =r'D:\img-set\mobile\mobile_2017_7_4\huawei\Annotations'
    # txtsavepath = r'D:\img-set\mobile\mobile_2017_7_4\huawei\txt_splitdataset'
    # trainval_percent = 0.5
    # train_percent = 0.8
    # for label in insect:
    #     xmlfile_path = os.path.join(xml_path, label)
    #     spilt_train_test(xmlfile_path, txtsavepath, trainval_percent, train_percent,label)
    # # 合并txt文件
    # insectlist = ['ls', 'rd', 'tc', 'os', 'ct', 'sz']
    # txtspath = r"D:\img-set\mobile\mobile_2017_7_4\mi\txt_splitdataset"
    # outputpath = r"D:\img-set\mobile\mobile_2017_7_4\mi"
    # fname = "trainval"
    # fname = "test"
    # fname = "train"
    # fname = "val"








