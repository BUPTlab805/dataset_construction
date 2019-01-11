#!/usr/bin/python
# encoding:utf-8
from xml.dom.minidom import Document
from lxml import objectify
import os
import matplotlib.pyplot as plt
import numpy as np
#将大图剪切成小图，并修改其label，生成新的label annotations 文件

#命名生成的小图（一张原图剪切结果）
def getname (num_begin ,img_num):#img_nmu:生成新图像的数量
    name_long =8
    img_newname = []
    xml_newname = []
    for i in range(img_num):
        b = np.zeros(img_num).astype(np.str)
        c = str(i + num_begin)
        ze = name_long - len(c)
        b[i] = '0' * ze + c
        img_name =  b[i] + '.jpg'
        xml_name =  b[i] + '.xml'
        print(b[i])
        img_newname.append(img_name)
        xml_newname.append(xml_name)
    return img_newname, xml_newname

#计算图像剪切个数
def calculate_images(img_h,img_w,delta_w,delta_h):
    #计算图像剪切H
    h_index = img_h / delta_h
    tmp_h = img_h - h_index*delta_h
    if tmp_h < 500:
        h_index = h_index -1
        tmp_h = img_h - h_index*delta_h
    # 计算图像剪切W
    w_index = img_w / delta_w
    tmp_w = img_w - w_index * delta_w
    if tmp_w < 500:
        w_index = w_index - 1
        tmp_w = img_w - w_index * delta_w
    return h_index,w_index,tmp_h,tmp_w

#读取一个xml文件，剪切生成小图，并生成相应的xml文件
def read_xml(img_path, xmlpath,outputpath,delta_w,delta_h,num_begin):
    xml = objectify.parse(open(xmlpath))
    img =0
    root = xml.getroot()
    imagename = 0
    wsize = 0
    hsize = 0
    label = []

    x1 = []
    y1 = []
    x2 = []
    y2 = []

    img_newname = []
    xml_newname = []
    re_w = 0 # 余数
    re_h = 0 # 余数
    h_index = 0
    w_index = 0
    # 解析xml得到原始的label和BBox坐标
    for tmp in root.getchildren():
        if tmp.tag == 'filename':
            # imagename = tmp.pyval
            # img = plt.imread(os.path.join(img_path,imagename))
            img = plt.imread(img_path)
            hsize= img.shape[0]
            wsize = img.shape[1]
            h_index, w_index, re_h, re_w = calculate_images(hsize,wsize,delta_w,delta_h)
            print("number of new images:",int((w_index + 1) * (h_index + 1)))
            img_newname, xml_newname = getname(num_begin, img_num=int((w_index + 1) * (h_index + 1)))
            # 得到原始的label和BBox坐标
        if tmp.tag == 'object':
                obj = tmp
                for child in obj.getchildren():
                    if child.tag == 'name':
                        if child.pyval == 'so' or child.pyval == 'sz':
                            name = 'sitophilus'
                            label.append(name)

                        elif child.pyval == 'cf' or child.pyval == 'cp' or child.pyval == 'ct'or child.pyval == 'cryptoleste':
                            name = 'cryptolestes'
                            label.append(name)
                            # print('fhdfk')

                        elif child.pyval == 'ls':
                            name = 'lasioderma'
                            label.append(name)

                        elif child.pyval == 'os' or child.pyval == 'osww':
                            name = 'oryzaephilus'
                            label.append(name)

                        elif child.pyval == 'rd':
                            name = 'rhizopertha'
                            label.append(name)

                        elif child.pyval == 'tc' or child.pyval == 'tco' or child.pyval == 'Tenebrionidae':
                            name = 'tribolium'
                            label.append(name)
                            # print('change T-t')
                        else:
                            name = child.pyval
                            label.append(name)

                    if child.tag == 'bndbox':
                        for coordinate in child.getchildren():
                            if coordinate.tag == 'xmin':
                                x1.append(coordinate.pyval )
                            if coordinate.tag == 'ymin':
                                y1.append(coordinate.pyval)
                            if coordinate.tag == 'xmax':
                                x2.append(coordinate.pyval)
                            if coordinate.tag == 'ymax':
                                y2.append(coordinate.pyval)




    index = 0  # 计数一张图片生成了的小图的数量
    for x_i in range(int(w_index + 1)):
        tmp_ox = x_i * delta_w
        x_boundary = tmp_ox + delta_w
        if x_i == w_index:
            x_boundary = tmp_ox + re_w

        for y_i in range(int(h_index + 1)):
            tmp_oy = y_i * delta_h
            y_boundary = tmp_oy + delta_h
            if y_i == h_index:
                y_boundary = tmp_oy + re_h
            ss_img = img[tmp_oy:y_boundary, tmp_ox:x_boundary, :]
            s_img = ss_img.copy()  # 生成img
            tmp_path = os.path.join(outputpath, 'JPEGImages')
            save_path = os.path.join(tmp_path, img_newname[index])

            # 获取新的label 和 BBox坐标
            imagenewname = img_newname[index]
            new_label = []
            x_min = []
            y_min = []
            x_max = []
            y_max = []
            img_w = 0
            img_h = 0
            for j in range(len(x1)):
                # 最理想的情况：边界框不被切割线穿过
                if (x1[j] >= tmp_ox) & (y1[j] >= tmp_oy) & (x2[j] <= x_boundary) & (y2[j] <= y_boundary):
                    x_min.append(x1[j] - tmp_ox)
                    x_max.append(x2[j] - tmp_ox)
                    y_min.append(y1[j] - tmp_oy)
                    y_max.append(y2[j] - tmp_oy)
                # 边界框被横着的切割线穿过
                elif (x1[j] >= tmp_ox) & (y1[j] >= tmp_oy) & (x2[j] <= x_boundary) & (y2[j] > y_boundary) & (
                        y1[j] < y_boundary):
                    if (y2[j] - y_boundary) <= (y_boundary - y1[j]):
                        y_min.append(y1[j] - tmp_oy)
                        y_max.append(y_boundary - tmp_oy)
                        x_min.append(x1[j] - tmp_ox)
                        x_max.append(x2[j] - tmp_ox)

                elif (x1[j] >= tmp_ox) & (y1[j] < tmp_oy) & (x2[j] <= x_boundary) & (y2[j] <= y_boundary):
                    if (y2[j] - tmp_oy) > (tmp_oy - y1[j]):
                        y_min.append(1)
                        y_max.append(y2[j] - tmp_oy)
                        x_min.append(x1[j] - tmp_ox)
                        x_max.append(x2[j] - tmp_ox)

                # 边界框被竖着的切割线切割
                elif (x1[j] >= tmp_ox) & (y1[j] >= tmp_oy) & (x2[j] > x_boundary) & (y2[j] <= y_boundary) & (
                        x1[j] < x_boundary):
                    if (x2[j] - x_boundary) <= (x_boundary - x1[j]):
                        x_min.append(x1[j] - tmp_ox)
                        x_max.append(x_boundary - tmp_ox)
                        y_min.append(y1[j] - tmp_oy)
                        y_max.append(y2[j] - tmp_oy)

                elif (x1[j] <= tmp_ox) & (y1[j] >= tmp_oy) & (x2[j] <= x_boundary) & (y2[j] <= y_boundary):
                    if (x2[j] - tmp_ox) > (tmp_ox - x1[j]):
                        x_min.append(1)
                        x_max.append(x2[j] - tmp_ox)
                        y_min.append(y1[j] - tmp_oy)
                        y_max.append(y2[j] - tmp_oy)

                # 最不理想的情况，边界框被两条切割线穿过
                elif (x1[j] >= tmp_ox) & (y1[j] >= tmp_oy) & (x2[j] >= x_boundary) & (y2[j] >= y_boundary) & (
                        x1[j] < x_boundary) & (y1[j] < y_boundary):
                    if ((x2[j] - x_boundary) <= (x_boundary - x1[j])) & ((y2[j] - y_boundary) <= (y_boundary - y1[j])):
                        x_min.append(x1[j] - tmp_ox)
                        x_max.append(x_boundary - tmp_ox)
                        y_min.append(y1[j] - tmp_oy)
                        y_max.append(y_boundary - tmp_oy)

                elif (x1[j] < tmp_ox) & (y1[j] >= tmp_oy) & (x2[j] < x_boundary) & (y2[j] >= y_boundary) & (
                        y1[j] < y_boundary):
                    if ((x2[j] - tmp_ox) >= (tmp_ox - x1[j])) & ((y2[j] - y_boundary) <= (y_boundary - y1[j])):
                        x_min.append(1)
                        x_max.append(x2[j] - tmp_ox)
                        y_min.append(y1[j] - tmp_oy)
                        y_max.append(y_boundary - tmp_oy)

                elif (x1[j] >= tmp_ox) & (y1[j] < tmp_oy) & (x2[j] > x_boundary) & (y2[j] < y_boundary) & (
                        x1[j] < x_boundary):
                    if ((x2[j] - x_boundary) <= (x_boundary - x1[j])) & ((y2[j] - tmp_oy) >= (tmp_oy - y1[j])):
                        x_min.append(x1[j] - tmp_ox)
                        x_max.append(x_boundary - tmp_ox)
                        y_min.append(1)
                        y_max.append(y2[j] - tmp_oy)

                elif (x1[j] < tmp_ox) & (y1[j] < tmp_oy) & (x2[j] < x_boundary) & (y2[j] < y_boundary):
                    if ((x2[j] - tmp_ox) >= (tmp_ox - x1[j])) & ((y2[j] - tmp_oy) >= (tmp_oy - y1[j])):
                        x_min.append(1)
                        x_max.append(x2[j] - tmp_ox)
                        y_min.append(1)
                        y_max.append(y2[j] - tmp_oy)

                new_label.append(label[j])
                img_h = y_boundary - tmp_oy
                img_w = x_boundary - tmp_ox

            # 生成xml
            if (len(x_min) != 0):
                doc = Document()
                annotation = doc.createElement('annotation')
                doc.appendChild(annotation)

                folder = doc.createElement('folder')
                folder_text = doc.createTextNode('VOC2007')
                folder.appendChild(folder_text)
                annotation.appendChild(folder)

                filename = doc.createElement('filename')
                filename_text = doc.createTextNode(imagenewname)
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
                width_text = doc.createTextNode(str(img_w))
                width.appendChild(width_text)
                size.appendChild(width)

                height = doc.createElement('height')
                height_text = doc.createTextNode(str(img_h))
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

                for i in range(len(x_min)):
                    object = doc.createElement('object')
                    annotation.appendChild(object)

                    name1 = doc.createElement('name')
                    name1_text = doc.createTextNode(str(new_label[i]))
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
                    xmin_text = doc.createTextNode(str(x_min[i]))
                    xmin.appendChild(xmin_text)
                    bndbox.appendChild(xmin)

                    ymin = doc.createElement('ymin')
                    ymin_text = doc.createTextNode(str(y_min[i]))
                    ymin.appendChild(ymin_text)
                    bndbox.appendChild(ymin)

                    xmax = doc.createElement('xmax')
                    xmax_text = doc.createTextNode(str(x_max[i]))
                    xmax.appendChild(xmax_text)
                    bndbox.appendChild(xmax)

                    ymax = doc.createElement('ymax')
                    ymax_text = doc.createTextNode(str(y_max[i]))
                    ymax.appendChild(ymax_text)
                    bndbox.appendChild(ymax)

                # f = open(outputpath + '/Annotations/' + xml_newname[index], 'w')
                # f.write(doc.toprettyxml(indent=''))
                # f.close()
                # plt.imsave(save_path, s_img)
            index = 1 + index

    return index,img_newname

if __name__ == '__main__':
    num_begin =0
    path = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCdevice1/VOC2007/"
    xmls_path = path +'/Annotations'
    imgs_path = path + "/JPEGImages/"
    txts = ['/ImageSets/Main/train.txt','/ImageSets/Main/test.txt','/ImageSets/Main/val.txt']
    outputpath = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/'
    txtsavepath = outputpath +"/ImageSets/Main"
    txts_to_write=['train.txt','test.txt','val.txt']

    for i,txt in enumerate(txts):
        txt_path = path+txt
        txt_file = open(txt_path, 'r')
        txt_to_write_path = os.path.join(txtsavepath,txts_to_write[i])
        f = open(txt_to_write_path, 'a')
        lines = txt_file.readlines()
        for line in lines:
            name = line[:-1]
            xmlname = name + '.xml'
            imgname = name + '.jpg'
            xml_path = os.path.join(xmls_path, xmlname)
            img_path = os.path.join(imgs_path, imgname)
            num_end, new_imgnames = read_xml(img_path=img_path, xmlpath=xml_path, outputpath=outputpath, delta_w=1024, delta_h=1024, num_begin=num_begin)
            num_begin = num_end + num_begin
            print(num_begin, num_end)
            for new_imgname in new_imgnames:
                f.writelines(new_imgname[:-4]+'\r')




