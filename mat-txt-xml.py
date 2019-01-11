#encoding:utf-8
#用于将.txt转换成.xml，制作成voc2007 要求格式

import matplotlib.pyplot as plt
import os
from xml.dom.minidom import Document
import scipy.io as sio
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
from lxml import objectify
import shutil

def get_name(imagename):

    name = imagename[:-4]
    return name
def txt2xml(txt_path , outputpath,imagepath):
    txt_file = open(txt_path, 'r')
    lines = txt_file.readlines()
    imagename = 0
    name = 0
    label = 0
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    lastname = 'begin'


    for line in lines:
    # 整行读取数据
       f_tmp, i_tmp, xmin_tmp, ymin_tmp, xmax_tmp, ymax_tmp = [i for i in line.split()]
       imagename = f_tmp
       imgpath =  os.path.join(imagepath,imagename)
       img = plt.imread(imgpath)
       imgshape = img.shape
       wsize =imgshape[1]
       hsize =imgshape[0]
       label = i_tmp
       x1 = str(max(int(xmin_tmp), 0))  # 判断是否越界
       y1 = str(max(int(ymin_tmp), 0))
       x2 = str(min(int(xmax_tmp), wsize))
       y2 = str(min(int(ymax_tmp), hsize))

       if (len(x1) != 0)&(lastname == imagename): #相同的图片
           # 修改xml
           object = doc.createElement('object')
           annotation.appendChild(object)

           name1 = doc.createElement('name')
           name1_text = doc.createTextNode(str(label))
           name1.appendChild(name1_text)
           object.appendChild(name1)

           pose = doc.createElement('pose')
           pose_text = doc.createTextNode('Unspecified')
           pose.appendChild(pose_text)
           object.appendChild(pose)

           truncated = doc.createElement('truncated')
           truncated_text = doc.createTextNode('0')
           truncated.appendChild(truncated_text)
           object.appendChild(truncated)

           difficult = doc.createElement('difficult')
           difficult_text = doc.createTextNode('0')
           difficult.appendChild(difficult_text)
           object.appendChild(difficult)

           bndbox = doc.createElement('bndbox')
           object.appendChild(bndbox)

           xmin = doc.createElement('xmin')
           xmin_text = doc.createTextNode(str(x1))
           xmin.appendChild(xmin_text)
           bndbox.appendChild(xmin)

           ymin = doc.createElement('ymin')
           ymin_text = doc.createTextNode(str(y1))
           ymin.appendChild(ymin_text)
           bndbox.appendChild(ymin)

           xmax = doc.createElement('xmax')
           xmax_text = doc.createTextNode(str(x2))
           xmax.appendChild(xmax_text)
           bndbox.appendChild(xmax)

           ymax = doc.createElement('ymax')
           ymax_text = doc.createTextNode(str(y2))
           ymax.appendChild(ymax_text)
           bndbox.appendChild(ymax)

       else :# 不同图片
           if lastname != 'begin' :
               # 保存上一次的xml
               tempname = lastname
               name = get_name(tempname)
               f = open(outputpath + '/' + name + '.xml', 'w')
               f.write(doc.toprettyxml(indent=''))
               f.close()

           # 新建新的xml
           doc = Document()
           annotation = doc.createElement('annotation')
           doc.appendChild(annotation)

           folder = doc.createElement('folder')
           folder_text = doc.createTextNode('VOC2007')
           folder.appendChild(folder_text)
           annotation.appendChild(folder)

           filename = doc.createElement('filename')
           filename_text = doc.createTextNode(imagename)
           filename.appendChild(filename_text)
           annotation.appendChild(filename)

           source = doc.createElement('source')
           annotation.appendChild(source)

           database = doc.createElement('database')
           database_text = doc.createTextNode('My Database')
           database.appendChild(database_text)
           source.appendChild(database)

           annotation1 = doc.createElement('annotation')
           annotation1_text = doc.createTextNode('VOC2007')
           annotation1.appendChild(annotation1_text)
           source.appendChild(annotation1)

           image = doc.createElement('image')
           image_text = doc.createTextNode('flickr')
           image.appendChild(image_text)
           source.appendChild(image)

           flickrid = doc.createElement('flickrid')
           flickrid_text = doc.createTextNode('NULL')
           flickrid.appendChild(flickrid_text)
           source.appendChild(flickrid)

           owner = doc.createElement('owner')
           annotation.appendChild(owner)

           flickrid = doc.createElement('flickrid')
           flickrid_text = doc.createTextNode('NULL')
           flickrid.appendChild(flickrid_text)
           owner.appendChild(flickrid)

           name = doc.createElement('name')
           name_text = doc.createTextNode('lijiangtao')
           name.appendChild(name_text)
           owner.appendChild(name)

           size = doc.createElement('size')
           annotation.appendChild(size)

           width = doc.createElement('width')
           width_text = doc.createTextNode(str(wsize))
           width.appendChild(width_text)
           size.appendChild(width)

           height = doc.createElement('height')
           height_text = doc.createTextNode(str(hsize))
           height.appendChild(height_text)
           size.appendChild(height)

           depth = doc.createElement('depth')
           depth_text = doc.createTextNode('3')
           depth.appendChild(depth_text)
           size.appendChild(depth)

           segmented = doc.createElement('segmented')
           segmented_text = doc.createTextNode('0')
           segmented.appendChild(segmented_text)
           annotation.appendChild(segmented)

           object = doc.createElement('object')
           annotation.appendChild(object)

           name1 = doc.createElement('name')
           name1_text = doc.createTextNode(str(label))
           name1.appendChild(name1_text)
           object.appendChild(name1)

           pose = doc.createElement('pose')
           pose_text = doc.createTextNode('Unspecified')
           pose.appendChild(pose_text)
           object.appendChild(pose)

           truncated = doc.createElement('truncated')
           truncated_text = doc.createTextNode('0')
           truncated.appendChild(truncated_text)
           object.appendChild(truncated)

           difficult = doc.createElement('difficult')
           difficult_text = doc.createTextNode('0')
           difficult.appendChild(difficult_text)
           object.appendChild(difficult)

           bndbox = doc.createElement('bndbox')
           object.appendChild(bndbox)

           xmin = doc.createElement('xmin')
           xmin_text = doc.createTextNode(str(x1))
           xmin.appendChild(xmin_text)
           bndbox.appendChild(xmin)

           ymin = doc.createElement('ymin')
           ymin_text = doc.createTextNode(str(y1))
           ymin.appendChild(ymin_text)
           bndbox.appendChild(ymin)

           xmax = doc.createElement('xmax')
           xmax_text = doc.createTextNode(str(x2))
           xmax.appendChild(xmax_text)
           bndbox.appendChild(xmax)

           ymax = doc.createElement('ymax')
           ymax_text = doc.createTextNode(str(y2))
           ymax.appendChild(ymax_text)
           bndbox.appendChild(ymax)

           lastname = imagename
       #
       tempname = lastname
       name = get_name(tempname)
       f = open(os.path.join(outputpath,name + '.xml'), 'w')
       f.write(doc.toprettyxml(indent=''))
       # f.close()

def read_xml_draw(xmlpath,imagepath,outputpath):

    xmls = os.listdir(xmlpath)
    # images = os.listdir(image_path)
    for xml in xmls:
        if xml[-3:] != "xml":
            continue
        imgname = get_name(xml)
        if os.path.exists(os.path.join(imagepath,imgname+'.BMP')):
            img = cv.imread(os.path.join(imagepath,imgname+'.BMP'))
        elif os.path.exists(os.path.join(imagepath,imgname+'.JPG')):
            img = cv.imread(os.path.join(imagepath, imgname + '.JPG'))
        else:
            img = cv.imread(os.path.join(imagepath, imgname + '.jpg'))

        # print type(tmp)
        xml = objectify.parse(open(os.path.join(xmlpath,xml)))
        root = xml.getroot()
        copy = img.copy()
        copy = cv.cvtColor(copy,cv.COLOR_BGR2RGB)
        x1=[]
        x2=[]
        y1=[]
        y2=[]
        label=[]
        for tmp in root.getchildren():
            if tmp.tag == 'object':
                obj = tmp
                for child in obj.getchildren():
                    if child.tag == 'bndbox':
                        x1.append(child.xmin.pyval)
                        y1.append(child.ymin.pyval)
                        x2.append(child.xmax.pyval)
                        y2.append(child.ymax.pyval)
                    if child.tag == 'name':
                        label.append(child.pyval)



                    continue
            continue
        if len(x1)!=0:
            for i in range(len(x1)):
                   copy = cv.rectangle(copy, (x1[i], y1[i]), (x2[i], y2[i]), (255, 0, 0), 3)
                   caption = "{}".format(label[i])
                   cv.putText(copy, caption, (x1[i], y1[i] - 10), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 3)


            save_path = os.path.join(outputpath, imgname + '.png')
        # plt.imshow(copy), plt.title('Result'), plt.show()
            plt.imsave(save_path, copy)

def mat2txt(path):
    insect = ['al', 'ls', 'cf', 'rd', 'tc', 'tco', 'os', 'ct', 'so', 'sz', 'cp']
    category = insect.index(os.path.split(path)[-1][0:2])
    label = insect[category]
    if os.path.split(path)[-1][0:3]== 'tco':
        label = insect[5]

    # 读取.mat文件中的bbox
    matpath = path
    mat = os.path.join(matpath, label + ".mat")
    data = sio.loadmat(mat)
    a = data[label][0]
    # a = data['to'][0]
    num = a.size
    # print(a[0][1])
    # print (a[0][0])
    # 写txt
    txtpath = path
    txt_path = os.path.join(txtpath, label + ".txt")
    f = open(txt_path, 'a')
    # files = os.listdir(os.path.join(path,'pics'))
    filenames=[]
    # files = os.listdir(path)
    # for i in range(len(files)):
    #     filename = files[i]
    #     # name=a[0][i][0]
    #     if filename[-3:]!='JPG':
    #         continue
    #     # print(filename)
    #     filenames.append(filename)

    for i in range(num):
        filepath = a[i][0][0]
        print(type(filepath))
        # print(a[2][0][0])
        filename = filepath[38:len(filepath)]
        for j in range(len(a[i][1])):

            tmp = a[i][1][j]
            bbox = []
            # 左上
            if (tmp[2] > 20) & (tmp[3] > 20):
                bbox.append(tmp[0])
                bbox.append(tmp[1])
                # 右下
                bbox.append(tmp[0] + tmp[2])
                bbox.append(tmp[1] + tmp[3])

                bbox = np.array(bbox)
                line = str(filename) + ' '+label + ' '+str(bbox)
                line = list(line)
                line.remove('[')
                line.remove(']')
                line = ''.join(line)
                print(line)
                # lines = []
                f.writelines(line)
                f.writelines("\n")
                # lines.append(line)
    return label

def txt2xml_for_mess(txt_path , outputpath,imagepath):
    txt_file = open(txt_path, 'r')
    lines = txt_file.readlines()
    imagename = 0
    name = 0
    label = 0
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    lastname = 'begin'


    for line in lines:
    # 整行读取数据
       f_tmp, num ,i_tmp, xmin_tmp, ymin_tmp, xmax_tmp, ymax_tmp = [i for i in line.split()]
       imagename = f_tmp+" "+num
       imgpath =  os.path.join(imagepath,imagename)
       img = plt.imread(imgpath)
       imgshape = img.shape
       wsize =imgshape[1]
       hsize =imgshape[0]
       label = i_tmp
       x1 = str(max(int(xmin_tmp), 0))  # 判断是否越界
       y1 = str(max(int(ymin_tmp), 0))
       x2 = str(min(int(xmax_tmp), wsize))
       y2 = str(min(int(ymax_tmp), hsize))

       if (len(x1) != 0)&(lastname == imagename): #相同的图片
           # 修改xml
           object = doc.createElement('object')
           annotation.appendChild(object)

           name1 = doc.createElement('name')
           name1_text = doc.createTextNode(str(label))
           name1.appendChild(name1_text)
           object.appendChild(name1)

           pose = doc.createElement('pose')
           pose_text = doc.createTextNode('Unspecified')
           pose.appendChild(pose_text)
           object.appendChild(pose)

           truncated = doc.createElement('truncated')
           truncated_text = doc.createTextNode('0')
           truncated.appendChild(truncated_text)
           object.appendChild(truncated)

           difficult = doc.createElement('difficult')
           difficult_text = doc.createTextNode('0')
           difficult.appendChild(difficult_text)
           object.appendChild(difficult)

           bndbox = doc.createElement('bndbox')
           object.appendChild(bndbox)

           xmin = doc.createElement('xmin')
           xmin_text = doc.createTextNode(str(x1))
           xmin.appendChild(xmin_text)
           bndbox.appendChild(xmin)

           ymin = doc.createElement('ymin')
           ymin_text = doc.createTextNode(str(y1))
           ymin.appendChild(ymin_text)
           bndbox.appendChild(ymin)

           xmax = doc.createElement('xmax')
           xmax_text = doc.createTextNode(str(x2))
           xmax.appendChild(xmax_text)
           bndbox.appendChild(xmax)

           ymax = doc.createElement('ymax')
           ymax_text = doc.createTextNode(str(y2))
           ymax.appendChild(ymax_text)
           bndbox.appendChild(ymax)

       else :# 不同图片
           if lastname != 'begin' :
               # 保存上一次的xml
               tempname = lastname
               name = get_name(tempname)
               f = open(outputpath + '/' + name + '.xml', 'w')
               f.write(doc.toprettyxml(indent=''))
               f.close()

           # 新建新的xml
           doc = Document()
           annotation = doc.createElement('annotation')
           doc.appendChild(annotation)

           folder = doc.createElement('folder')
           folder_text = doc.createTextNode('VOC2007')
           folder.appendChild(folder_text)
           annotation.appendChild(folder)

           filename = doc.createElement('filename')
           filename_text = doc.createTextNode(imagename)
           filename.appendChild(filename_text)
           annotation.appendChild(filename)

           source = doc.createElement('source')
           annotation.appendChild(source)

           database = doc.createElement('database')
           database_text = doc.createTextNode('My Database')
           database.appendChild(database_text)
           source.appendChild(database)

           annotation1 = doc.createElement('annotation')
           annotation1_text = doc.createTextNode('VOC2007')
           annotation1.appendChild(annotation1_text)
           source.appendChild(annotation1)

           image = doc.createElement('image')
           image_text = doc.createTextNode('flickr')
           image.appendChild(image_text)
           source.appendChild(image)

           flickrid = doc.createElement('flickrid')
           flickrid_text = doc.createTextNode('NULL')
           flickrid.appendChild(flickrid_text)
           source.appendChild(flickrid)

           owner = doc.createElement('owner')
           annotation.appendChild(owner)

           flickrid = doc.createElement('flickrid')
           flickrid_text = doc.createTextNode('NULL')
           flickrid.appendChild(flickrid_text)
           owner.appendChild(flickrid)

           name = doc.createElement('name')
           name_text = doc.createTextNode('lijiangtao')
           name.appendChild(name_text)
           owner.appendChild(name)

           size = doc.createElement('size')
           annotation.appendChild(size)

           width = doc.createElement('width')
           width_text = doc.createTextNode(str(wsize))
           width.appendChild(width_text)
           size.appendChild(width)

           height = doc.createElement('height')
           height_text = doc.createTextNode(str(hsize))
           height.appendChild(height_text)
           size.appendChild(height)

           depth = doc.createElement('depth')
           depth_text = doc.createTextNode('3')
           depth.appendChild(depth_text)
           size.appendChild(depth)

           segmented = doc.createElement('segmented')
           segmented_text = doc.createTextNode('0')
           segmented.appendChild(segmented_text)
           annotation.appendChild(segmented)

           object = doc.createElement('object')
           annotation.appendChild(object)

           name1 = doc.createElement('name')
           name1_text = doc.createTextNode(str(label))
           name1.appendChild(name1_text)
           object.appendChild(name1)

           pose = doc.createElement('pose')
           pose_text = doc.createTextNode('Unspecified')
           pose.appendChild(pose_text)
           object.appendChild(pose)

           truncated = doc.createElement('truncated')
           truncated_text = doc.createTextNode('0')
           truncated.appendChild(truncated_text)
           object.appendChild(truncated)

           difficult = doc.createElement('difficult')
           difficult_text = doc.createTextNode('0')
           difficult.appendChild(difficult_text)
           object.appendChild(difficult)

           bndbox = doc.createElement('bndbox')
           object.appendChild(bndbox)

           xmin = doc.createElement('xmin')
           xmin_text = doc.createTextNode(str(x1))
           xmin.appendChild(xmin_text)
           bndbox.appendChild(xmin)

           ymin = doc.createElement('ymin')
           ymin_text = doc.createTextNode(str(y1))
           ymin.appendChild(ymin_text)
           bndbox.appendChild(ymin)

           xmax = doc.createElement('xmax')
           xmax_text = doc.createTextNode(str(x2))
           xmax.appendChild(xmax_text)
           bndbox.appendChild(xmax)

           ymax = doc.createElement('ymax')
           ymax_text = doc.createTextNode(str(y2))
           ymax.appendChild(ymax_text)
           bndbox.appendChild(ymax)

           lastname = imagename
       #
       tempname = lastname
       name = get_name(tempname)
       f = open(os.path.join(outputpath,name + '.xml'), 'w')
       f.write(doc.toprettyxml(indent=''))
       # f.close()

if __name__ == '__main__':

    # dir_path = r"C:\Users\Public\Pictures\insect_imagaes_dataset\orignal_img_dataset\orignal_mobile\2016-11-hut\shouji_mi\test"
    # paths = os.listdir(dir_path)
    path ='/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/sticky_board/2017_07_04/dfkjfdk'


    xmlpath = path
    imagepath = path
    outputpath = path + "/show_gt"
    # if not os.path.exists(xmlpath):
    #     os.mkdir(xmlpath)
    #     # shutil.rmtree(xmlpath)

    if not os.path.exists(outputpath):
        os.mkdir(outputpath)


    # label = mat2txt(path)

    # txtpath = path + "/" + label + ".txt"
    # txtpath = path +'/tco.txt'
    # txt2xml_for_mess(txtpath, xmlpath, imagepath)
    read_xml_draw(xmlpath, imagepath, outputpath)


