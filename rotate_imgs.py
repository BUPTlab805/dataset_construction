import os
import cv2
import matplotlib.pyplot as plt
# def rotate(image)

inputpath = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/sticky_board/VOC2007/JPEGImages/1025/mmp'
imgs = os.listdir(inputpath)
out ='/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/sticky_board/VOC2007/JPEGImages/1025/mmp_re'
for img_n in imgs:
    img = cv2.imread(os.path.join(inputpath,img_n))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    (h,w)=img.shape[:2]
    print('h:',h,"w:",w)
    center =(w/2,h/2)

    M= cv2.getRotationMatrix2D(center,90,1.0)
    rotated = cv2.warpAffine(img,M,(w,h))
# cv2.imshow('shf',rotated)
# cv2.waitKey(0)
#     plt.imshow(rotated)
    #  plt.show()
    outpath =os.path.join(out,img_n)
    plt.imsave(outpath, rotated)