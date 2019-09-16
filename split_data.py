# -*- coding:utf-8 -*-
import argparse
import random
from random import randint
import os
import numpy as np
import shutil

def clc(dir):
    ls = os.listdir(dir)
    for i in ls:
        c_path = os.path.join(dir, i)
        os.remove(c_path)

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-i', '--input',help='path of data', default='/home/syh/pascal_voc/')
args = parser.parse_args()

if __name__ == '__main__':
    folder_list= ["train","val","test"]
	
    base_dir = os.path.join(args.input)
    for i in range(3):
        folder_name = folder_list[i]
        xml_dir = base_dir + folder_name + "/Annotations/"
        if not os.path.exists(xml_dir):
            # print(xml_dir)
            os.makedirs(xml_dir)

    train_dir = base_dir + folder_list[0] + "/Annotations/"
    val_dir = base_dir + folder_list[1] + "/Annotations/"
    test_dir = base_dir + folder_list[2] + "/Annotations/"
    clc(train_dir)
    clc(test_dir)
    clc(val_dir)

    num = len(os.listdir(os.path.join(base_dir,'Annotations')))
    scale = 4
    val_num = num // scale
    test_num = num // scale

    total = np.arange(1,num+1)
    valList = random.sample(range(1, num+1), val_num) #val random select
    # print(sorted(valList))

    # move val_num val pics to splited folder
    for i in range(0,val_num):
        xmlfile = ("%08d" % (valList[i]))
        file_dir = base_dir + "/Annotations/"+'/'+ xmlfile +'.xml'
        shutil.copy(file_dir,val_dir)

    # take away val ids from total ids
    total_val = [] # total ids minus val ids, ids left stay here
    for i in range(0,num):
        if total[i] not in valList:
            total_val.append(total[i])

    testlist_temp = random.sample(range(0, num-val_num), test_num) #test random select
    # print(sorted(testlist_temp))
    testList = []
    for k in range(0,test_num):
        testList.append(total_val[testlist_temp[k]])
    # print(sorted(testList))

    # move test_num test pics to splited folder
    for i in range(0,test_num):
        xmlfile = ("%08d" % (testList[i]))
        file_dir = base_dir + "/Annotations/"+'/'+ xmlfile +'.xml'
        shutil.copy(file_dir,test_dir)

    # take away test ids from total_val ids
    total_val_test = [] # total ids minus val&test ids, ids left stay here
    for i in range(0,num-val_num):
        if total_val[i] not in testList:
            total_val_test.append(total_val[i])
    # print(sorted(total_val_test))

    # move lest train pics to splited folder
    for i in range(0,num-val_num-test_num):
        xmlfile = ("%08d" % (total_val_test[i]))
        file_dir = base_dir + "/Annotations/"+'/'+ xmlfile +'.xml'
        shutil.copy(file_dir,train_dir)

    print('train:', len(os.listdir(train_dir)))
    print('val:', len(os.listdir(val_dir)))
    print('test:', len(os.listdir(test_dir)))

'''
python voc2coco/split_data.py -i /home/syh/cornernet-lite/data/voc/
'''