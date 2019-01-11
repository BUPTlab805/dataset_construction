#encoding:utf-8
import scipy.io as sio
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

insect = ['al','ls', 'cf', 'cf_z', 'rd' , 'tc', 'tco', 'os_z', 'os_s','so', 'sz']
category = 10
label = insect[category]
file_name = insect[category] + '.jpg'
num=0
#读取文件名
path = r'D:\img-set\mobile\2016-11-hn\shouji_mi\train'
pic_path = r"D:\img-set\mobile\2016-11-hn\shouji_mi\train\sz2016_8zhengzhou"
files = os.listdir(pic_path)
# print files

# matlab文件名
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
            tmp_path=os.path.join(r"D:\img_set_single\moble\201611hnmitrain",label)
            save_path = os.path.join(tmp_path,str(num) + file_name)
            plt.imsave(save_path, s_img)
