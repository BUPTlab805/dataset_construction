#!/usr/bin/python
# encoding:utf-8

import cv2
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
from matplotlib import pyplot as plt
import pandas as pd
#import matplotlib.mlab as mlab
import numpy as np
from lxml import objectify
import os
import math


def get_color_3d_BGR(img):
    b = img[:,:,0]# BGR中的B�?
    g = img[:,:,1]# BGR中的g�?
    r = img[:,:,2]# BGR中的r�?
    m_b = b.mean()
    m_g = g.mean()
    m_r = r.mean()
    # print (m_r, m_g, m_b)
    return m_r, m_g, m_b




class Image_Statistics():

    def calculate_image_mean_RGB(self,file_path):
        files = os.listdir(file_path)
        num = 0
        r = 0.0
        g = 0.0
        b = 0.0
        for img_name in files:
            num = num + 1
            img_path = os.path.join(file_path, img_name)
            img = cv2.imread(img_path)
            tmp_r,tmp_g,tmp_b = get_color_3d_BGR(img)
            r = tmp_r + r
            g = tmp_g + g
            b = tmp_b + b
        r = r / num
        g = g / num
        b = b / num
        return r,g,b


    def instance_per_images(self,xml_path):# 统计大图中的bbox个数
        bbox_num =[]
        total_img =0

        xml_files = os.listdir(xml_path)
        for xml_file in xml_files:
            xmlfile_path = os.path.join(xml_path,xml_file)
            xml = objectify.parse(open(xmlfile_path))
            num=0
            root = xml.getroot()
            for tmp in root.getchildren():
                if tmp.tag == 'object':
                    num = num +1
                continue
            bbox_num.append(num)
            # number = number+1
        bbox_num = np.array(bbox_num)
        total_img =len(bbox_num)
        sum = bbox_num.sum()
        return bbox_num,total_img,sum

    def instance_size(self, xmlpath):
        insect_size = []
        scale=[]
        img_h=[]
        img_w=[]
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
                if tmp.tag == 'size':
                    imgsize = tmp
                    for child in imgsize.getchildren():
                        if child.tag == 'height':
                            h = child.pyval
                            img_h.append(h)
                        if child.tag == 'width':
                            w = child.pyval
                            img_w.append(w)

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
            if h * w != 0 and len(xmin) != 0:
                for i in range(len(xmin)):
                    w_i = abs(xmax[i] - xmin[i])
                    h_i = abs(ymax[i] - ymin[i])
                    area = w_i * h_i
                    if area < 0.000:
                        print("erros")
                        # area = -1.0* area
                    insect_size.append(100.0*float(area) / float(h * w))
                    scale.append(max(w_i,h_i))
        # print(insect_size)
        return insect_size,scale,img_w,img_h

    def get_mode(self,arr):# 求众�?
        mode=[]
        arr_appear = dict((a,arr.count(a)) for a in arr)
        if max (arr_appear.values())==1:
            return
        else:
            for k,v in arr_appear.items():
                if v == max(arr_appear.values()):
                    mode.append(k)
        return mode

    def get_average_(self,arr):
        tmp=0
        for i in arr:
            tmp+= i
        if len(arr)!=0:
            return tmp/len(arr)
        else:
            print('erros,len(arr)=0')

    def get_var(self,arr,mean):
        tmp=0
        for i in arr:
            tmp += (i-mean)*(i-mean)
        if len(arr) != 0:
            var=tmp / len(arr)
            std = math.sqrt(var)
            return std
        else:
            print('erros,len(arr)=0')

    def calculate_scale_distribute_of_each_species_6(self,xmlpath):
        # s=np.zeros((8,4))
        s= np.zeros((6,4))#6 species
        scale_group = [1,64,128,256]
        label =[]
        xmin=[]
        xmax=[]
        ymin=[]
        ymax=[]
        xmls = os.listdir(xmlpath)

        #获取label和bbox
        for xml in xmls:
            xmlfile_path = os.path.join(xmlpath, xml)
            xml = objectify.parse(open(xmlfile_path))
            root = xml.getroot()
            for tmp in root.getchildren():
                if tmp.tag == 'object':
                    obj = tmp
                    for child in obj.getchildren():
                        if child.tag == 'name':
                            label.append(child.pyval)
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
        print (len(label),len(xmin))
        #统计
        for i in range(len(label)):
            # scale=(xmax[i]+ymax[i]-xmin[i]-ymin[i])/2
            scale= max(xmax[i]-xmin[i],ymax[i]-ymin[i])
            if label[i] == "sz" or label[i]=="so" or label[i] == 'sitophilus':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[0,0]=s[0,0]+1
                elif (scale > scale_group[1]) & (scale <=scale_group[2]):
                    s[0,1]=s[0,1] + 1
                elif (scale > scale_group[2]) & (scale <=scale_group[3]):
                    s[0,2]=s[0,2] + 1
                else:
                    s[0, 3] = s[0, 3] + 1

            elif label[i] == "os" or label[i] == 'oryzaephilus':
                if (scale >=scale_group[0]) & (scale <= scale_group[1]):
                    s[1,0]=s[1,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[1,1]=s[1,1] +1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[1, 2] = s[1, 2] + 1
                else:
                    s[1, 3] = s[1, 3] + 1
            elif label[i] == "ls" or label[i] == 'lasioderma':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[2,0]=s[2,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[2,1]=s[2,1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[2,2]=s[2,2] + 1
                else:
                    s[2, 3] = s[2, 3] + 1
            elif label[i] == "tc" or label[i]=='tco' or label[i] == 'tenebrionidae'or label[i] =='tribolium':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[3,0] = s[3,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[3,1] = s[3,1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[3, 2] = s[3, 2] + 1
                else:
                    s[3, 3] = s[3, 3] + 1
            elif label[i] == "ct" or  label[i]=='cp' or  label[i]=='cf' or label[i] == 'cryptoleste'or label[i] == 'cryptolestes':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[4,0] = s[4,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[4,1] = s[4,1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[4,2] = s[4,2] + 1
                else:
                    s[4, 3] = s[4, 3] + 1
            elif label[i] == "rd" or label[i] == 'rhizopertha':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[5,0]=s[5,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[5,1]=s[5,1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[5,2]=s[5,2] + 1
                else:
                    s[5, 3] = s[5, 3] + 1
        # 显示统计结果
        each_species = s.sum(axis=1)
        print (each_species , type(each_species))
        num_of_each_species = dict(Sz=each_species[0],Os=each_species[1],Ls=each_species[2],Tc=each_species[3],Ct=each_species[4],Rd=each_species[5] )
        df = pd.DataFrame(s , index=['S.','O.','L.','T.','C.','R.'],columns=pd.Index(['1-64','64-128','128-256','256-']))
        print (df)
        df.plot(kind='bar',alpha = 0.5)
        plt.show()
        # df.plot(kind="barh")

        # return num_of_each_species

    def calculate_scale_distribute_of_each_species_10(self,xmlpath):
        s=np.zeros((10,4))
        scale_group = [1,64,128,256]
        label =[]
        xmin=[]
        xmax=[]
        ymin=[]
        ymax=[]
        xmls = os.listdir(xmlpath)
        #获取label和bbox
        for xml in xmls:
            xmlfile_path = os.path.join(xmlpath, xml)
            xml = objectify.parse(open(xmlfile_path))
            root = xml.getroot()
            for tmp in root.getchildren():
                if tmp.tag == 'object':
                    obj = tmp
                    for child in obj.getchildren():
                        if child.tag == 'name':
                            label.append(child.pyval)
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
        print (len(label),len(xmin))
        #统计
        for i in range(len(label)):
            # scale=(xmax[i]+ymax[i]-xmin[i]-ymin[i])/2
            scale= max(xmax[i]-xmin[i],ymax[i]-ymin[i])
            if label[i] == "sz"or label[i]=="SZ":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[0,0]=s[0,0]+1
                elif (scale > scale_group[1]) & (scale <=scale_group[2]):
                    s[0,1]=s[0,1] + 1
                elif (scale > scale_group[2]) & (scale <=scale_group[3]):
                    s[0,2]=s[0,2] + 1
                else:
                    s[0, 3] = s[0, 3] + 1

            elif label[i] == "so" or label[i] =="SO":
                # print("djfk")
                if (scale >=scale_group[0]) & (scale <= scale_group[1]):
                    s[1,0]=s[1,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[1,1]=s[1,1] +1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[1, 2] = s[1, 2] + 1
                else:
                    s[1, 3] = s[1, 3] + 1
            elif label[i] == "ls"or label[i] == "LS":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[2,0]=s[2,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[2,1]=s[2,1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[2,2]=s[2,2] + 1
                else:
                    s[2, 3] = s[2, 3] + 1
            elif label[i] == "os"or label[i] == "OS" or label[i] == "osww":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[3,0] = s[3,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[3,1] = s[3,1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[3, 2] = s[3, 2] + 1
                else:
                    s[3, 3] = s[3, 3] + 1
            elif label[i] == "ct"or label[i] == "CT":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[4,0] = s[4,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[4,1] = s[4,1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[4,2] = s[4,2] + 1
                else:
                    s[4, 3] = s[4, 3] + 1
            elif label[i] == "cp"or label[i] == "CP":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[5,0]=s[5,0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[5,1]=s[5,1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[5,2]=s[5,2] + 1
                else:
                    s[5, 3] = s[5, 3] + 1
            elif label[i] == "cf"or label[i] == "CF":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[6, 0] = s[6, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[6, 1] = s[6, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[6, 2] = s[6, 2] + 1
                else:
                    s[6, 3] = s[6, 3] + 1
            elif label[i] == "rd"or label[i] == "RD":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[7, 0] = s[7, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[7, 1] = s[7, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[7, 2] = s[7, 2] + 1
                else:
                    s[7, 3] = s[7, 3] + 1
            elif label[i] == "tc"or label[i] == "TC":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[8, 0] = s[8, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[8, 1] = s[8, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[8, 2] = s[8, 2] + 1
                else:
                    s[8, 3] = s[8, 3] + 1
            elif label[i] == "tco"or label[i] == "TCO":
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[9, 0] = s[9, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[9, 1] = s[9, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[9, 2] = s[9, 2] + 1
                else:
                    s[9, 3] = s[9, 3] + 1

        # 显示统计结果
        each_species = s.sum(axis=1)
        each_scale_group = s.sum(axis=0)
        print(each_scale_group)
        # print (each_species , type(each_species))
        num_of_each_species = dict(Sz=each_species[0],So=each_species[1],Ls=each_species[2],Os=each_species[3],Ct=each_species[4],Cp=each_species[5],Cf = each_species[6],Rd = each_species[7],Tc=each_species[8],Tco=each_species[9] )
        df = pd.DataFrame(s , index=['Sz','So','Ls','Os','Ct','Cp','Cf','Rd','Tc','Tco'],columns=pd.Index(['1-32 pixels','32-96 pixels','96-224 pixels','224- pixels']))
        # df = pd.DataFrame(s , index=['Sitophilus zeamais','Sitophilus oryzae','Lasioderma serricorne','Oryzaephilus surinamesnsis','Cryptolestes turcicus','Cryptolestes pusillus','Cryptolestes ferrugineus','Rhizopertha dominica','Tribolium confusum','Tribolium confusum Jac.du Val.z'],columns=pd.Index(['1-64 pixels','64-128 pixels','128-256 pixels','256- pixels']))
        print(each_species)
        # print (num_of_each_species)
        df.plot(kind='bar', alpha =0.5)
        plt.xlabel('Species');plt.ylabel('Number of instances');plt.title('Distribution of instance size')
        plt.show()
        # df.plot(kind="barh")
        s=np.zeros((10,1))
        for i in range(len(each_species)):
            s[i,0]= each_species[i]
        return s, each_scale_group

    def calculate_scale_distribute(self,xmlpath):
        s = np.zeros((1, 5))
        scale_group = [1, 32, 64, 128, 256]
        label = []
        xmin = []
        xmax = []
        ymin = []
        ymax = []
        xmls = os.listdir(xmlpath)
        scales=[]
        # 获取label和bbox
        for xml in xmls:
            xmlfile_path = os.path.join(xmlpath, xml)
            xml = objectify.parse(open(xmlfile_path))
            root = xml.getroot()
            for tmp in root.getchildren():
                if tmp.tag == 'object':
                    obj = tmp
                    for child in obj.getchildren():
                        if child.tag == 'name':
                            label.append(child.pyval)
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
        print(len(label), len(xmin))
        # 统计
        for i in range(len(label)):
            # scale=(xmax[i]+ymax[i]-xmin[i]-ymin[i])/2
            scale = max(xmax[i] - xmin[i], ymax[i] - ymin[i])
            scales.append(scale)
            if label[i]:
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[0, 0] = s[0, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[0, 1] = s[0, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[0, 2] = s[0, 2] + 1
                elif (scale > scale_group[3]) & (scale <= scale_group[4]):
                    s[0, 3] = s[0, 3] + 1
                else:
                    s[0, 4] = s[0, 4] + 1

        # 显示统计结果
        df = pd.DataFrame(s, index=['Insect'], columns=pd.Index(['1-32', '32-64', '64-128', '128-256', '256-']))
        print(df)
        df.plot(kind='bar',alpha =0.5)
        plt.show()
        # df.plot(kind="barh")

        # return scales

    def calculate_scale_distribute_of_each_species_6_read_text(self, xmlpath,txtpath):
        # s=np.zeros((8,4))
        s = np.zeros((6, 4))  # 6 species
        # scale_group = [1, 64, 128, 256]
        scale_group = [1, 16, 32, 64]
        label = []
        xmin = []
        xmax = []
        ymin = []
        ymax = []
        xmls = os.listdir(xmlpath)
        txt_file = open(txtpath, 'r')
        lines = txt_file.readlines()
        # 获取label和bbox
        for xml in lines:
            xmlname = xml[:-1]+'.xml'
            xmlfile_path = os.path.join(xmlpath, xmlname)
            xml = objectify.parse(open(xmlfile_path))
            root = xml.getroot()
            for tmp in root.getchildren():
                if tmp.tag == 'object':
                    obj = tmp
                    for child in obj.getchildren():
                        if child.tag == 'name':
                            label.append(child.pyval)
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
        print(len(label), len(xmin))
        # 统计
        for i in range(len(label)):
            # scale=(xmax[i]+ymax[i]-xmin[i]-ymin[i])/2
            scale = max(xmax[i] - xmin[i], ymax[i] - ymin[i])
            if label[i] == "sz" or label[i] == "so" or label[i] == 'sitophilus':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[0, 0] = s[0, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[0, 1] = s[0, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[0, 2] = s[0, 2] + 1
                else:
                    s[0, 3] = s[0, 3] + 1

            elif label[i] == "os" or label[i] == 'oryzaephilus':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[1, 0] = s[1, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[1, 1] = s[1, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[1, 2] = s[1, 2] + 1
                else:
                    s[1, 3] = s[1, 3] + 1
            elif label[i] == "ls" or label[i] == 'lasioderma':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[2, 0] = s[2, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[2, 1] = s[2, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[2, 2] = s[2, 2] + 1
                else:
                    s[2, 3] = s[2, 3] + 1
            elif label[i] == "tc" or label[i] == 'tco' or label[i] == 'tenebrionidae' or label[i] =='tribolium':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[3, 0] = s[3, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[3, 1] = s[3, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[3, 2] = s[3, 2] + 1
                else:
                    s[3, 3] = s[3, 3] + 1
            elif label[i] == "ct" or label[i] == 'cp' or label[i] == 'cf' or label[i] == 'cryptolestes'or label[i] == 'cryptoleste':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[4, 0] = s[4, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[4, 1] = s[4, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[4, 2] = s[4, 2] + 1
                else:
                    s[4, 3] = s[4, 3] + 1
            elif label[i] == "rd" or label[i] == 'rhizopertha':
                if (scale >= scale_group[0]) & (scale <= scale_group[1]):
                    s[5, 0] = s[5, 0] + 1
                elif (scale > scale_group[1]) & (scale <= scale_group[2]):
                    s[5, 1] = s[5, 1] + 1
                elif (scale > scale_group[2]) & (scale <= scale_group[3]):
                    s[5, 2] = s[5, 2] + 1
                else:
                    s[5, 3] = s[5, 3] + 1
        # 显示统计结果
        each_species = s.sum(axis=1)
        print(each_species, type(each_species))
        num_of_each_species = dict(Sz=each_species[0], Os=each_species[1], Ls=each_species[2], Tc=each_species[3],
                                   Ct=each_species[4], Rd=each_species[5])
        df = pd.DataFrame(s, index=['S.', 'O.', 'L.', 'T.', 'C.', 'R.'],
                          # columns=pd.Index(['1-64', '64-128', '128-256', '256-']))
                          columns=pd.Index(['1-16', '16-32', '32-64', '64-']))
        print(df)
        df.plot(kind='bar', alpha=0.5)
        plt.show()
        # df.plot(kind="barh")

        # return num_of_each_species












if __name__ == '__main__':
    a = Image_Statistics()
    # a.calculate_scale_distribute(p)
    xmlpath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/Annotations/"
    txtpath1 = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/ImageSets/Main/train.txt"
    txtpath2 = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/ImageSets/Main/test.txt"
    txtpath3 = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/ImageSets/Main/val.txt"    
    # a.calculate_scale_distribute_of_each_species_6(xmlpath)
    # txtpath1 = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/RGBInsectpapers/VOC2007/ImageSets/Main/trainval.txt"
    # txtpath2 = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/RGBInsectpapers/VOC2007/ImageSets/Main/test.txt"
    #a.calculate_scale_distribute_of_each_species_6_read_text(xmlpath, txtpath1)
    a.calculate_scale_distribute_of_each_species_6_read_text(xmlpath, txtpath2)
    #a.calculate_scale_distribute_of_each_species_6_read_text(xmlpath, txtpath3)
    # instances per category
    # fp1 = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCdevice1/VOC2007/Annotations_10/"
    # fp2 = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCdevice2/VOC2007/Annotations_10/"
    # fp3 = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/Annotations_10/"
    # tmp1,g1= a.calculate_scale_distribute_of_each_species_10(fp1)
    # tmp2,g2 = a.calculate_scale_distribute_of_each_species_10(fp2)
    # tmp3,g3 = a.calculate_scale_distribute_of_each_species_10(fp3)
    # a,b,scales=a.instance_per_images(fp3)
    # print(a,b,scales)
    # print(a.mean())
    # tmp= np.append(tmp1,tmp2,axis=1)
    # tmp = np.append(tmp,tmp3,axis=1)
    # print (tmp)
    # df = pd.DataFrame(tmp , index=['Sz','So','Ls','Os','Ct','Cp','Cf','Rd','Tc','Tco'],columns=pd.Index(['Subset1','Subset2','Subset3']))
    #
    # print(df)
    # df.plot(kind='bar', stacked=True, alpha=0.5,)
    # plt.xlabel('Species');plt.ylabel('Number of Instances')
    # plt.title('Instances per Category')
    # plt.show()

    # instances per images

    # bbnum1, img_num1= a.instance_per_images(fp1)
    # bbnum2, img_num2 = a.instance_per_images(fp2)
    # bbnumv, img_numv = a.instance_per_images(fpvoc)
    # bbnum3, img_num3 = a.instance_per_images(fp3)
    # a1 = a.get_average_(bbnum1)
    # a2 = a.get_average_(bbnum2)
    # a3 = a.get_average_(bbnum3)

    # s = pd.DataFrame({'sudset1':bbnum1,'subset2':bbnum2,'voc2010':bbnumv},columns=['subset1','subset2','voc2010'])
    # plt.figure();s.plot.hist()
    # sv= pd.Series(bbnumv)
    # s1= pd.Series(bbnum1)
    # s2= pd.Series(bbnum2)
    # s3 = pd.Series(bbnum3)

    # print(s)
    # s.div(float(img_num))
    # s.value_counts().plot(kind='hist')
    # s1.plot(kind='hist',bins =50, color = 'y');plt.xlabel('Number of instances');plt.ylabel('Number of images');plt.title('intances per image')
    # s2.plot(kind='hist',bins= 50);plt.xlabel('Number of instances');plt.ylabel('Number of images');plt.title('intances per image')
    # s3.plot(kind='hist', bins=50,color = 'b');plt.xlabel('Number of instances');plt.ylabel('Number of images');plt.title('intances per image')
    # sv.plot(kind='hist',bins= 50,color ='k');plt.xlabel('Number of instances');plt.ylabel('Number of images');plt.title('intances per image')
    #
    #
    # plt.show()
    #
    # instances size
    # percent_of_imageSize1,scale,w,h= a.instance_size(path)
    # scale_avg= a.get_average_(scale)
    # print(scale_avg)
    # percent_of_imageSize2,scale,w,h = a.instance_size(fp2)
    # percent_of_imageSizev,scale,w,h = a.instance_size(fpvoc)
    # percent_of_imageSize3,scale,w,h = a.instance_size(paper_path)
    # mean_w = a.get_average_(w)
    # mean_h = a.get_average_(h)
    # print(mean_w,mean_h)
    # 计算众数\均值、方�?
    # mode = a.get_mode(scale)
    # mean = a.get_average_(scale)
    # var = a.get_var(scale,mean)
    # print(mode,mean,var)
    # # #print(percent_of_imageSize)
    # # s1 = pd.Series(percent_of_imageSize1)
    # # s2 = pd.Series(percent_of_imageSize2)
    # # sv = pd.Series(percent_of_imageSizev)
    # s3 = pd.Series(percent_of_imageSize3)
    # #
    # #
    # # # s1.plot(kind ='hist',bins= 100,color= 'y',xlim=[0,1],xticks=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    # #
    # # # s2.plot(kind='hist', bins=2000, xlim=[0,1],xticks=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    # s3.plot(kind='hist', bins=100, color = 'b',xlim=[0, 0.2])
    # # #
    # # sv.plot(kind='hist', bins=100, color='k')
    # plt.xlabel('Instance size');plt.ylabel('Number of instances');plt.title('Percent of instance size')
    # plt.show()


















