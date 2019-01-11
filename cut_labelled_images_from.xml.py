#encoding:utf-8
from lxml import objectify
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
def get_name(xmlname):
    f_tmp = list(xmlname)
    f_tmp.remove('.')
    f_tmp.remove('x')
    f_tmp.remove('m')
    f_tmp.remove('l')
    f_tmp = ''.join(f_tmp)
    name = f_tmp
    return name

def read_xml_cut(label,xmlpath,imagepath,outputpath):
    num = 0
    newimage = label + '.jpg'
    xml_path = os.path.join(xmlpath,label)
    image_path = os.path.join(imagepath,label)
    output_path = os.path.join(outputpath,label)
    xmls = os.listdir(xml_path)
    # images = os.listdir(image_path)
    for xmlname in xmls:
        imgname = get_name(xmlname)
        img = plt.imread(os.path.join(image_path,imgname+'.jpg'))
        xml = objectify.parse(open(os.path.join(xml_path,xmlname)))
        root = xml.getroot()
        for tmp in root.getchildren():
            if tmp.tag == 'object':
                obj = tmp
                for child in obj.getchildren():
                    if child.tag == 'bndbox':
                        x1=child.xmin.pyval
                        y1=child.ymin.pyval
                        x2=child.xmax.pyval
                        y2=child.ymax.pyval
                        if ((x2 - x1) >= 20) & ((y2 - y1) >= 20):
                            num = num + 1
                            ss_img = img[y1:y2, x1:x2, :]
                            s_img = ss_img.copy()
                            save_path = os.path.join(output_path, str(num) + newimage)
                            plt.imsave(save_path, s_img)

                    continue
            continue
    print (num)

#批处理剪切下来的图片，生成train.txt和val.txt
def generate_txt(path,txtname):#path:剪切下来的图片的路径
    txtpath = os.path.join(path, txtname + ".txt")
    f = open(txtpath, 'a')
    files = os.listdir(os.path.join(path,txtname))
    for label in files:
        class_num = label2num(label)
        imgs = os.listdir(os.path.join(os.path.join(path,txtname),label))
        for img in imgs:
            line = label+ "/"+img +" "+ class_num
            f.writelines(line)
            f.writelines("\n")
    f.close()

def label2num(label):
    if label == "ct":
        num = '0'
    elif label == 'ls':
        num ='1'
    elif label == 'os':
        num = '2'
    elif label == 'rd':
        num ='3'
    elif label == 'sz':
        num ='4'
    elif label == 'tc':
        num ='5'
    return num

if __name__ == '__main__':
    # huawei
    # insect = ['ls', 'cf', 'rd', 'tc',  'os', 'ct', 'so', 'sz', 'cp']# tco 没有，是因为当时用MATLAB标注的
    # xmlpath = r'D:\img-set\mobile\mobile_2017_7_4\huawei\voc2007'#xml文件地址
    # imagepath = r'D:\img-set\mobile\mobile_2017_7_4\huawei'#image文件地址
    # outputpath =r'D:\img_set_single\moble\20170704hua' #输出的地址
    # # # for label in insect:
    # # #     read_xml_cut(label, xmlpath, imagepath, outputpath)
    # read_xml_cut("sz", xmlpath, imagepath, outputpath)

    # insect = ['ls', 'cf', 'rd', 'tc', 'os', 'ct', 'so', 'sz', 'cp','tco']
    # xmlpath = r'D:\img-set\mobile\mobile_2017_7_4\mi\Annotations'  # xml文件地址
    # imagepath = r'D:\img-set\mobile\mobile_2017_7_4\mi'  # image文件地址
    # outputpath = r'D:\img_set_single\moble\20170704mi'  # 输出的地址
    # # # for label in insect:
    # # #     read_xml_cut(label, xmlpath, imagepath, outputpath)
    # read_xml_cut("tco", xmlpath, imagepath, outputpath)
    path = r"D:\img_set_single\moble\20170919_insect_6"
    txtname = 'train'
    # generate_txt(path, txtname)
    # txtname = 'val'
    generate_txt(path, txtname)












