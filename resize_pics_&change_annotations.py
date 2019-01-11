#!/usr/bin/python
# encoding:utf-8
from xml.dom.minidom import Document
from lxml import objectify
import os
import matplotlib.pyplot as plt
from skimage import transform,data
import cv2
from scipy import misc

def xml2xml_resized(inputpath,outputpath,set_scale_l,set_scale_s,imgpath,outimg): # 输入为输入输出路径

  for alldir in os.listdir(inputpath):
     file_path = os.path.join(inputpath, alldir)
     xml = objectify.parse(open(file_path))
     root = xml.getroot()
     imagename=0
     img_h=0
     img_w=0
     wsize = 0
     hsize =0
     label = []
     x1 = []
     y1 = []
     x2 = []
     y2 = []
     kl= 0.0   #resize 的比例
     ks = 0.0
     for tmp in root.getchildren():
        if tmp.tag == 'filename':
            imagename = tmp.pyval
            file_path = os.path.join(imgpath, imagename)
            img = plt.imread(file_path)
        if tmp.tag == 'size':
            imagesize =tmp
            for child in imagesize.getchildren():
                if child.tag =='height':
                    img_h = child.pyval
                if child.tag =='width':
                    img_w = child.pyval
            if img_h & img_w :
                if img_h>img_w:
                    # kl = float(set_scale_l) / float(img_h)
                    ks = float(set_scale_s) / float(img_w)
                    wsize = int(ks * img_w)
                    hsize = int(ks * img_h)
                else:
                    # kl = float(set_scale_l) / float(img_w)
                    ks = float(set_scale_s) / float(img_h)
                    wsize = int(ks * img_w)
                    hsize = int(ks * img_h)
                res = cv2.resize(img, (wsize, hsize))
                save_path = os.path.join(outimg, imagename)
                plt.imsave(save_path, res)
        if tmp.tag == 'object':
            obj = tmp
            objection = True
            for child in obj.getchildren():
                if child.tag == 'name':
                    label.append(child.pyval)

                if child.tag == 'bndbox':
                    for coordinate in child.getchildren():
                        if coordinate.tag == 'xmin':
                            if img_h > img_w:
                                x1.append(int(coordinate.pyval * ks))
                            else:
                                x1.append(int(coordinate.pyval * kl))
                        if coordinate.tag == 'ymin':
                            if img_h > img_w:
                                y1.append(int(coordinate.pyval * kl))
                            else:
                                y1.append(int(coordinate.pyval * ks))
                        if coordinate.tag == 'xmax':
                            if img_h > img_w:
                                x2.append(int(coordinate.pyval * ks))
                            else:
                                x2.append(int(coordinate.pyval * kl))
                        if coordinate.tag == 'ymax':
                            if img_h > img_w:
                                y2.append(int(coordinate.pyval * kl))
                            else:
                                y2.append(int(coordinate.pyval * ks))
     # if len(x1) != 0 :
     #    doc = Document()
     #    annotation = doc.createElement('annotation')
     #    doc.appendChild(annotation)
     #
     #    folder = doc.createElement('folder')
     #    folder_text = doc.createTextNode('VOC2007')
     #    folder.appendChild(folder_text)
     #    annotation.appendChild(folder)
     #
     #    filename = doc.createElement('filename')
     #    filename_text = doc.createTextNode(imagename)
     #    filename.appendChild(filename_text)
     #    annotation.appendChild(filename)
     #
     #    source = doc.createElement('source')
     #    annotation.appendChild(source)
     #
     #    database = doc.createElement('database')
     #    database_text = doc.createTextNode('My Database')
     #    database.appendChild(database_text)
     #    source.appendChild(database)
     #
     #    annotation1 = doc.createElement('annotation')
     #    annotation1_text = doc.createTextNode('VOC2007')
     #    annotation1.appendChild(annotation1_text)
     #    source.appendChild(annotation1)
     #
     #    image = doc.createElement('image')
     #    image_text = doc.createTextNode('flickr')
     #    image.appendChild(image_text)
     #    source.appendChild(image)
     #
     #    flickrid = doc.createElement('flickrid')
     #    flickrid_text = doc.createTextNode('NULL')
     #    flickrid.appendChild(flickrid_text)
     #    source.appendChild(flickrid)
     #
     #    owner = doc.createElement('owner')
     #    annotation.appendChild(owner)
     #
     #    flickrid = doc.createElement('flickrid')
     #    flickrid_text = doc.createTextNode('NULL')
     #    flickrid.appendChild(flickrid_text)
     #    owner.appendChild(flickrid)
     #
     #    name = doc.createElement('name')
     #    name_text = doc.createTextNode('lijiangtao')
     #    name.appendChild(name_text)
     #    owner.appendChild(name)
     #
     #    size = doc.createElement('size')
     #    annotation.appendChild(size)
     #
     #    width = doc.createElement('width')
     #    width_text = doc.createTextNode(str(wsize))
     #    width.appendChild(width_text)
     #    size.appendChild(width)
     #
     #    height = doc.createElement('height')
     #    height_text = doc.createTextNode(str(hsize))
     #    height.appendChild(height_text)
     #    size.appendChild(height)
     #
     #    depth = doc.createElement('depth')
     #    depth_text = doc.createTextNode('3')
     #    depth.appendChild(depth_text)
     #    size.appendChild(depth)
     #
     #    segmented = doc.createElement('segmented')
     #    segmented_text = doc.createTextNode('0')
     #    segmented.appendChild(segmented_text)
     #    annotation.appendChild(segmented)
     #
     #    for i in range(len(x1)):
     #        object = doc.createElement('object')
     #        annotation.appendChild(object)
     #
     #        name1 = doc.createElement('name')
     #        name1_text = doc.createTextNode(label[i].encode('utf-8'))
     #        name1.appendChild(name1_text)
     #        object.appendChild(name1)
     #
     #        pose = doc.createElement('pose')
     #        pose_text = doc.createTextNode('Unspecified')
     #        pose.appendChild(pose_text)
     #        object.appendChild(pose)
     #
     #        truncated = doc.createElement('truncated')
     #        truncated_text = doc.createTextNode('0')
     #        truncated.appendChild(truncated_text)
     #        object.appendChild(truncated)
     #
     #        difficult = doc.createElement('difficult')
     #        difficult_text = doc.createTextNode('0')
     #        difficult.appendChild(difficult_text)
     #        object.appendChild(difficult)
     #
     #        bndbox = doc.createElement('bndbox')
     #        object.appendChild(bndbox)
     #
     #        xmin = doc.createElement('xmin')
     #        xmin_text = doc.createTextNode(str(x1[i]))
     #        xmin.appendChild(xmin_text)
     #        bndbox.appendChild(xmin)
     #
     #        ymin = doc.createElement('ymin')
     #        ymin_text = doc.createTextNode(str(y1[i]))
     #        ymin.appendChild(ymin_text)
     #        bndbox.appendChild(ymin)
     #
     #        xmax = doc.createElement('xmax')
     #        xmax_text = doc.createTextNode(str(x2[i]))
     #        xmax.appendChild(xmax_text)
     #        bndbox.appendChild(xmax)
     #
     #        ymax = doc.createElement('ymax')
     #        ymax_text = doc.createTextNode(str(y2[i]))
     #        ymax.appendChild(ymax_text)
     #        bndbox.appendChild(ymax)
     #
     #    f=open(outputpath +'/'+ alldir,'w')
     #    f.write(doc.toprettyxml(indent=''))
     #    f.close()
     if len(x1) != 0:
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
         name_text = doc.createTextNode('ljt')
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

         for i in range(len(x1)):
             object = doc.createElement('object')
             annotation.appendChild(object)

             name1 = doc.createElement('name')
             name1_text = doc.createTextNode(str(label[i]))
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
             xmin_text = doc.createTextNode(str(x1[i]))
             xmin.appendChild(xmin_text)
             bndbox.appendChild(xmin)

             ymin = doc.createElement('ymin')
             ymin_text = doc.createTextNode(str(y1[i]))
             ymin.appendChild(ymin_text)
             bndbox.appendChild(ymin)

             xmax = doc.createElement('xmax')
             xmax_text = doc.createTextNode(str(x2[i]))
             xmax.appendChild(xmax_text)
             bndbox.appendChild(xmax)

             ymax = doc.createElement('ymax')
             ymax_text = doc.createTextNode(str(y2[i]))
             ymax.appendChild(ymax_text)
             bndbox.appendChild(ymax)

         f = open(outputpath + '/' + imagename[:-4] + '.xml', 'w')
         f.write(doc.toprettyxml(indent=''))
         f.close()
def xml2xml_resized_k(inputpath, outputpath, k, imgpath, outimg):  # 输入为输入输出路径

         for alldir in os.listdir(inputpath):
             file_path = os.path.join(inputpath, alldir)
             xml = objectify.parse(open(file_path))
             root = xml.getroot()
             imagename = 0
             img_h = 0
             img_w = 0
             label = []
             x1 = []
             y1 = []
             x2 = []
             y2 = []

             for tmp in root.getchildren():
                 if tmp.tag == 'filename':
                     imagename = tmp.pyval
                     file_path = os.path.join(imgpath, imagename)
                     img = plt.imread(file_path)
                 if tmp.tag == 'size':
                     imagesize = tmp
                     for child in imagesize.getchildren():
                         if child.tag == 'height':
                             img_h = child.pyval
                         if child.tag == 'width':
                             img_w = child.pyval
                         res = transform.resize(img, (int(k * img_w),int(k * img_h)))
                         save_path = os.path.join(outimg, imagename)
                         plt.imsave(save_path, res)
                 if tmp.tag == 'object':
                     obj = tmp
                     objection = True
                     for child in obj.getchildren():
                         if child.tag == 'name':
                             label.append(child.pyval)

                         if child.tag == 'bndbox':
                             for coordinate in child.getchildren():
                                 if coordinate.tag == 'xmin':
                                     x1.append(int(coordinate.pyval * k))
                                 if coordinate.tag == 'ymin':
                                     y1.append(int(coordinate.pyval * k))
                                 if coordinate.tag == 'xmax':
                                     x2.append(int(coordinate.pyval * k))
                                 if coordinate.tag == 'ymax':
                                     y2.append(int(coordinate.pyval * k))

             if len(x1) != 0:
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

                 for i in range(len(x1)):
                     object = doc.createElement('object')
                     annotation.appendChild(object)

                     name1 = doc.createElement('name')
                     name1_text = doc.createTextNode(label[i].encode('utf-8'))
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
                     xmin_text = doc.createTextNode(str(x1[i]))
                     xmin.appendChild(xmin_text)
                     bndbox.appendChild(xmin)

                     ymin = doc.createElement('ymin')
                     ymin_text = doc.createTextNode(str(y1[i]))
                     ymin.appendChild(ymin_text)
                     bndbox.appendChild(ymin)

                     xmax = doc.createElement('xmax')
                     xmax_text = doc.createTextNode(str(x2[i]))
                     xmax.appendChild(xmax_text)
                     bndbox.appendChild(xmax)

                     ymax = doc.createElement('ymax')
                     ymax_text = doc.createTextNode(str(y2[i]))
                     ymax.appendChild(ymax_text)
                     bndbox.appendChild(ymax)

                 f = open(outputpath + '/' + alldir, 'w')
                 f.write(doc.toprettyxml(indent=''))
                 f.close()





# def resize_image(imgpath,set_scale,out):
#     for img_file in os.listdir(imgpath):
#         file_path = os.path.join(imgpath, img_file)
#         img = plt.imread(file_path)
#         imgshape = img.shape
#         wsize = imgshape[1]
#         hsize = imgshape[0]
#         scale = max(wsize,hsize)
#         k = float(set_scale/scale)
#         w = int(wsize*k)
#         h = int(hsize*k)
#         # res = img.resize((w, h))
#         # res = cv.resize(img, (w, h))  # 直接resize
#         res = misc.imresize(img, k)
#         save_path = os.path.join(out, img_file)
#         plt.imsave(save_path, res)

if __name__ == '__main__':
    xmlinputpath = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/Annotations_6_o'
    xmloutputpath = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/Annotations'
    img_path ='/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/JPEGImages_o'
    out = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/JPEGImages'
    k=xml2xml_resized(xmlinputpath, xmloutputpath,set_scale_l=1400,set_scale_s=1000,imgpath=img_path,outimg=out)

