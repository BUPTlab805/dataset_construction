#!/usr/bin/python
# encoding:utf-8
from matplotlib import pyplot as plt
import numpy as np
import scipy.io as sio
from sklearn.externals import joblib
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os


insect = ['ls', 'cf',  'rd' , 'tc', 'tco', 'os', 'ct','so', 'sz','cp']
category = 0
label = insect[category]
file_name = insect[category] + '.jpg'
num=0

# 读取image路径
path = r'D:\img-set\mobile\mobile_2017_7_4\mi'
pic_path = os.path.join(path, label)
files = os.listdir(pic_path)

# matlab文件名
# mat = r'D:\img-set\mobile\mobile_2017_7_4\mi\ct.mat'
mat=os.path.join(path, label+".mat")
data = sio.loadmat(mat)
file = data.keys()
a = data[file[0]][0]
# a = data[file[1]][0]#读取.mat时，key的顺序不一样（sz，so）

for i in range(len(a)):
    filename = files[i]
    path = os.path.join(pic_path, filename)
    print path
    # img = cv2.imread(path)
    img = plt.imread(path)
    for j in a[i][1]:
        tmp = j
        # 判断bbox是否正常
        if  (tmp[2] >20)&(tmp[3]>20):
            num = num+1
            ss_img = img[tmp[1]:tmp[1]+tmp[3], tmp[0]:tmp[0]+tmp[2], :]
            s_img = ss_img.copy()
            tmp_path=os.path.join(r"D:\img_set_single\moble\20170704mi",label)
            save_path = os.path.join(tmp_path,str(num) + file_name)
            plt.imsave(save_path, s_img)








