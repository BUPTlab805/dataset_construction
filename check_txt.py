import os
test_txtpath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/ImageSets/Main/test.txt"
trainval_txtpath = "/home/ubuntu/lijiangtao/ImageDataset/insect_img_dataset/pascal_imgset/VOC2007/ImageSets/Main/trainval.txt"
test_file = open(test_txtpath, 'r')
test_lines = test_file.readlines()
trainval_file = open(trainval_txtpath, 'r')
trainval_lines = trainval_file.readlines()


def findSameNum(num1, num2):
    same=[]
    i = j = 0
    while i <= len(num1)-1 and j <= len(num2)-1:
        if num1[i] == num2[j]:
            same.append(num1[i])
            # return True
        if num1[i] != num2[j]:
            i += 1
        else:
            j += 1
    return same
def findsame(num1,num2):
    same=[]
    for i in num1:
        for j in num2:
            if i==j:
                print ("wrong")
                same.append(i)
    return same
            
same = findSameNum(num1=test_lines,num2=trainval_lines)
same = findsame(test_lines,trainval_lines)
print(same)