#!/usr/bin/python
# encoding:utf-8
from xml.dom.minidom import Document
from xml.etree.ElementTree import ElementTree, Element
from lxml import objectify
import os


def xml2xml_lableme(inputpath,outputpath):
    # 输入为输入输出路径Labelme
    xml = objectify.parse(open(inputpath))
    root = xml.getroot()
    imagename=0
    wsize = 0
    hsize =0
    label = []
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for tmp in root.getchildren():
      if tmp.tag == 'filename':
          imagename = tmp.pyval
      if tmp.tag == 'imagesize':
            imagesize =tmp
            for child in imagesize.getchildren():
                if child.tag =='nrows':
                    hsize = child.pyval
                if child.tag =='ncols':
                    wsize = child.pyval
      if tmp.tag == 'object':
          obj = tmp
          objection = True
          for child in obj.getchildren():
                if child.tag == 'name':
                    label.append(child.pyval)
                if child.tag == 'deleted':
                    if child.pyval == 1:
                        objection = False
                        del label[-1]
                if child.tag == 'polygon':
                    if objection == True:
                        a=[]
                        b=[]
                        for position in child.getchildren():
                            if position.tag == 'pt':
                                for location in position.getchildren():
                                    if location.tag == 'x':
                                        a.append(location.pyval)
                                    if location.tag == 'y':
                                        b.append(location.pyval)
                        xmin = min(a)
                        ymin = min(b)
                        xmax = max(a)
                        ymax = max(b)

                        if ((xmax - xmin) >= 20) & ((ymax - ymin) >= 20):
                            x1.append(max(xmin,0))
                            y1.append(max(ymin,0))
                            x2.append(min(xmax,wsize))
                            y2.append(min(ymax,hsize))
    if len(x1) != 0 :
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
        name_text = doc.createTextNode('zhouyizhe')
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

        f=open(outputpath +'/'+ imagename[:-4]+'.xml','w')
        f.write(doc.toprettyxml(indent=''))
        f.close()

def xml2xml_labelImage(inputpath,outputpath): # 输入为输入输出路�?    xml = objectify.parse(open(inputpath))
    root = xml.getroot()
    imagename=0
    wsize = 0
    hsize =0
    label = []
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    difficult =[]
    for tmp in root.getchildren():
        if tmp.tag == 'filename':
            print(tmp.pyval)
            imagename = tmp.pyval +'.jpg'


        if tmp.tag == 'size':
            imagesize =tmp
            for child in imagesize.getchildren():
                if child.tag =='height':
                    hsize = child.pyval
                if child.tag =='width':
                    wsize = child.pyval

        if tmp.tag == 'object':
            obj = tmp
            objection = True
            for child in obj.getchildren():
                # name=0
                difficult_tmp =0
                if child.tag == 'name':
                    if child.pyval == "ct":
                        name ="cp"
                        print("corrected to cp")
                    # elif child.pyval == "tco":
                    #     label.append("tc")
                    #     print "corrected tco "
                    elif child.pyval != 'cp' and child.pyval != 'ct' and child.pyval != 'cf'and child.pyval != 'ls'and child.pyval != 'os'and child.pyval !='rd'and child.pyval !='sz' and child.pyval !='so'and child.pyval !='tc'and child.pyval !='tco':
                        name = 'sz'
                        print("corrected to sz")
                    else:
                        name = child.pyval
                if child.tag == 'difficult':
                    difficult_tmp = child.pyval


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

                    if ((xmax - xmin) >= 20) & ((ymax - ymin) >= 20):
                            if len(x1)!=0:
                                if xmin!= x1[-1] and xmax!=x2[-1]:
                                    x1.append(max(xmin, 0))
                                    y1.append(max(ymin, 0))
                                    x2.append(min(xmax, wsize))
                                    y2.append(min(ymax, hsize))
                                    label.append(name)
                                    difficult.append(difficult_tmp)
                            else:
                                x1.append(max(xmin, 0))
                                y1.append(max(ymin, 0))
                                x2.append(min(xmax, wsize))
                                y2.append(min(ymax, hsize))
                                label.append(name)
                                difficult.append(difficult_tmp)



    if len(x1) != 0 :
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

        f=open(outputpath +'/'+ imagename[:-4]+'.xml','w')
        f.write(doc.toprettyxml(indent=''))
        f.close()

def changename_scientific_name(inputpath,outputpath):
    for alldir in os.listdir(inputpath):
        if alldir[-4:] != '.xml':
            continue
        file_path = os.path.join(inputpath, alldir)
        xml = objectify.parse(open(file_path, 'r', encoding='UTF-8'))
        root = xml.getroot()

        imagename = 0
        wsize = 0
        hsize = 0
        label = []
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        difficult1 = []
        for tmp in root.getchildren():
            if tmp.tag == 'filename':
                imagename = str(tmp.pyval)

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
                    # name = 'mycete'
                    # label.append(name)
                    if child.tag == 'name':
                        if child.pyval == 'so' or child.pyval =='sz':
                            name = 'sitophilus'
                            label.append(name)
                        elif child.pyval == 'cf' or child.pyval =='cp' or child.pyval =='ct'or child.pyval == 'cryptoleste':
                            name = 'cryptolestes'
                            label.append(name)
                            print('fhdfk')

                        elif child.pyval == 'ls':
                            name = 'lasioderma'
                            label.append(name)

                        elif child.pyval == 'os'or child.pyval =='osww':
                            name = 'oryzaephilus'
                            label.append(name)

                        elif child.pyval == 'rd':
                            name = 'rhizopertha'
                            label.append(name)

                        elif child.pyval=='tc' or child.pyval=='tco' or child.pyval =='Tenebrionidae':
                            name ='tribolium'
                            label.append(name)
                            print('change T-t')
                        else:
                            name = child.pyval
                            label.append(name)
                            print("do not need to correct",imagename)

                    if child.tag == 'difficult':
                        difficult1.append(child.pyval)

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
                            x1.append(max(xmin, 0))
                            y1.append(max(ymin, 0))
                            x2.append(min(xmax, wsize))
                            y2.append(min(ymax, hsize))

        # if len(label) == len(difficult1):
        #     print('ok')

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
                difficult_text = doc.createTextNode(str(difficult1[i]))
                # difficult_text = doc.createTextNode('0')
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

def revise_to_counting(inputpath,outputpath):
    for alldir in os.listdir(inputpath):
        if alldir[-4:] != '.xml':
            continue
        file_path = os.path.join(inputpath, alldir)
        xml = objectify.parse(open(file_path, 'r', encoding='UTF-8'))
        root = xml.getroot()

        imagename = 0
        wsize = 0
        hsize = 0
        label = []
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        difficult1 = []
        for tmp in root.getchildren():
            if tmp.tag == 'filename':
                imagename = str(tmp.pyval)

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
                    name = 'insect'
                    label.append(name)
                    # if child.tag == 'name':
                    #     if child.pyval == 'so' or child.pyval =='sz':
                    #         name = 'sitophilus'
                    #         label.append(name)
                    #     elif child.pyval == 'cf' or child.pyval =='cp' or child.pyval =='ct'or child.pyval == 'cryptoleste':
                    #         name = 'cryptolestes'
                    #         label.append(name)
                    #         # print('fhdfk')
                    #
                    #     elif child.pyval == 'ls':
                    #         name = 'lasioderma'
                    #         label.append(name)
                    #
                    #     elif child.pyval == 'os'or child.pyval =='osww':
                    #         name = 'oryzaephilus'
                    #         label.append(name)
                    #
                    #     elif child.pyval == 'rd':
                    #         name = 'rhizopertha'
                    #         label.append(name)
                    #
                    #     elif child.pyval=='tc' or child.pyval=='tco' or child.pyval =='Tenebrionidae':
                    #         name ='tribolium'
                    #         label.append(name)
                    #         # print('change T-t')
                    #     else:
                    #         name = child.pyval
                    #         label.append(name)
                    #         print("do not need to correct",imagename)

                    if child.tag == 'difficult':
                        difficult1.append(child.pyval)

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
                            x1.append(max(xmin, 0))
                            y1.append(max(ymin, 0))
                            x2.append(min(xmax, wsize))
                            y2.append(min(ymax, hsize))

        # if len(label) == len(difficult1):
        #     print('ok')

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
                difficult_text = doc.createTextNode(str(difficult1[i]))
                # difficult_text = doc.createTextNode('0')
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

def check_annotations(inputpath):
    imagename = []
    for alldir in os.listdir(inputpath):
        if alldir[-4:] != '.xml':
            continue
        file_path = os.path.join(inputpath, alldir)
        xml = objectify.parse(open(file_path, 'r', encoding='UTF-8'))
        root = xml.getroot()

        tmp_name=0
        for tmp in root.getchildren():
            if tmp.tag == 'filename':
                tmp_name = tmp.pyval
                # if tmp_name[:3]!='IMG' and tmp_name[16:19]=='001':
                #     imagename.append(tmp_name)
            if tmp.tag == 'object':
                obj = tmp
                # objection = True
                for child in obj.getchildren():
                    if child.tag == 'name':
                        # if child.pyval == 'tc' or child.pyval == 'tco' or child.pyval == 'Tenebrionidae':
                        if child.pyval == 'g1':
                            imagename.append(tmp_name)
                            print('erro',tmp_name)
                #         name ='tenebrionidae'
                #         label.append(name)
                #         # print('change T-t')
            #         if child.tag == 'bndbox':
            #             xmin=0
            #             ymin=0
            #             for coordinate in child.getchildren():
            #                 if coordinate.tag == 'xmin':
            #                     xmin = coordinate.pyval
            #                 if coordinate.tag == 'ymin':
            #                     ymin = coordinate.pyval
            #                 # if coordinate.tag == 'xmax':
            #                 #     xmax = coordinate.pyval
            #                 # if coordinate.tag == 'ymax':
            #                 #     ymax = coordinate.pyval
            #             if xmin <1 or ymin <1:
            #                 if tmp_name!=0:
            #                     imagename.append(tmp_name)
    return imagename



if __name__ == '__main__':
    inp="/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/Annotations/"
    out = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/Annotations_re/"    # inputpath ='/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/cropped_imgs/Annotations_6'
    changename_scientific_name(inp,out)
    
    # outputpath ='/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCmobile/VOC2007/cropped_imgs/Annotations'
    # revise_to_counting(inputpath,outputpath)
    #                 xml2xml_labelImage(xmlpath,outputpath)
    #
    # inp = '/media/ubuntu/CPBA_X64FRE/VOC2007/Annotations1'
    # out = '/media/ubuntu/CPBA_X64FRE/VOC2007/Annotations'
    # changename_scientific_name(inputpath=input, outputpath=outputpath)
    # out= '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCdevice2/VOC2007/Annotations'
    # inp = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOCdevice2/VOC2007/Annotations_10'
    # changename_scientific_name(inp,out)
    # path = '/media/ubuntu/LIJIANGTAO_/Annotations'
    # re=check_annotations(path)
    # print(re)\
    # out = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/RGBInsectpapers/VOC2007/Annotations_1'
    # inp = '/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/RGBInsectpapers/VOC2007/Annotations'
    # a = check_annotations(inp)
    # print(a)


