#encoding:utf-8
import os
import numpy as np
from xml.dom.minidom import Document
from lxml import objectify


def rename_xml_filename(xmlpath,imgname,outputpath):#修改xml文件名称和图片名称
    xml = objectify.parse(open(xmlpath))
    root = xml.getroot()
    wsize = 0
    hsize = 0
    label = []
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    difficult = []
    for tmp in root.getchildren():
        if tmp.tag == 'size':
            imagesize = tmp
            for child in imagesize.getchildren():
                if child.tag == 'height':
                    hsize = child.pyval
                if child.tag == 'width':
                    wsize = child.pyval
        if tmp.tag == 'object':
            obj = tmp
            objection = True
            for child in obj.getchildren():
                if child.tag == 'name':
                    name = child.pyval
                    label.append(name)
                if child.tag == 'difficult':
                    difficult_tmp = child.pyval
                    difficult.append(difficult_tmp)
                if child.tag == 'bndbox':
                    for coordinate in child.getchildren():
                        if coordinate.tag == 'xmin':
                            xmin = coordinate.pyval
                        if coordinate.tag == 'ymin':
                            ymin = coordinate.pyval
                        if coordinate.tag == 'xmax':
                            xmax = coordinate.pyval
                        if coordinate.tag == 'ymax':
                            ymax = coordinate.pyval
                    if ((xmax - xmin) >= 1) & ((ymax - ymin) >= 1):
                            # if x1[-1]!=xmin and x2[-1]!=xmax and y1[-1]!=ymin and y2[-1]!=ymax:
                            x1.append(max(xmin, 0))
                            y1.append(max(ymin, 0))
                            x2.append(min(xmax, wsize))
                            y2.append(min(ymax, hsize))


    if len(x1) != 0:
        doc = Document()
        annotation = doc.createElement('annotation')
        doc.appendChild(annotation)

        folder = doc.createElement('folder')
        folder_text = doc.createTextNode('VOC2007')
        folder.appendChild(folder_text)
        annotation.appendChild(folder)

        filename = doc.createElement('filename')
        filename_text = doc.createTextNode(imgname)
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

        f = open(outputpath + '/' + imgname[:-4]+'.xml', 'w')
        f.write(doc.toprettyxml(indent=''))
        f.close()

if __name__ == '__main__':

    imgdire ='/home/ubuntu/lijiangtao/keras_classification/data/insect_high_defination/test'
    species = os.listdir(imgdire)
    name_long = 4
    num_begin = 0
    newimgs = []

    for label in species:

        imgs = os.listdir(os.path.join(imgdire,label))
        for i in range(len(imgs)):
            img_path = os.path.join(os.path.join(imgdire,label), imgs[i])
            print(img_path)
            b = np.zeros(len(imgs)).astype(np.str)
            c = str(i + num_begin)
            ze = name_long - len(c)
            b[i] = '0' * ze + c
            tmpname = '3'+label+b[i] + '.bmp'
            newname = os.path.join(os.path.join(imgdire,label), tmpname)
            print(newname)
            os.rename(img_path, newname)
            # newimgs.append(newname)
    # print(newimgs)






