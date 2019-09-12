# -*- coding:utf-8 -*-

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

if __name__ == '__main__':
    folder_list= ["train","val","test"]
	
    base_dir = "/save-path/data/" 
    for i in range(3):
        folder_name = folder_list[i]
        xml_dir = base_dir + folder_name + "/Annotations/"
        if not os.path.exists(xml_dir):
        	os.makedirs(xml_dir)

    train_dir = base_dir + folder_list[0] + "/Annotations/"
    val_dir = base_dir + folder_list[1] + "/Annotations/"
    test_dir = base_dir + folder_list[2] + "/Annotations/"
    clc(train_dir)
    clc(test_dir)
    clc(val_dir)

    total = np.arange(1,10192+1)
    valList = random.sample(range(1, 10192+1), 500) #val random select
    print(sorted(valList))

    # move 500 val pics to splited folder
    for i in range(0,500):
    	xmlfile = ("%08d" % (valList[i]))
    	file_dir = base_dir + "/Annotations/"+'/'+ xmlfile +'.xml'
    	shutil.copy(file_dir,val_dir)

    # take away val ids from total ids
    total_val = [] # total ids minus val ids, ids left stay here
    for i in range(0,10192):
    	if total[i] not in valList:
    		total_val.append(total[i])

    testlist_temp = random.sample(range(0, 10192-500), 1000) #test random select
    print(sorted(testlist_temp))
    testList = []
    for k in range(0,1000):
    	testList.append(total_val[testlist_temp[k]])
    print(sorted(testList))

    # move 1000 test pics to splited folder
    for i in range(0,1000):
    	xmlfile = ("%08d" % (testList[i]))
    	file_dir = base_dir + "/Annotations/"+'/'+ xmlfile +'.xml'
    	shutil.copy(file_dir,test_dir)

    # take away test ids from total_val ids
    total_val_test = [] # total ids minus val&test ids, ids left stay here
    for i in range(0,10192-500):
    	if total_val[i] not in testList:
    		total_val_test.append(total_val[i])
    print(sorted(total_val_test))

    # move lest train pics to splited folder
    for i in range(0,10192-500-1000):
    	xmlfile = ("%08d" % (total_val_test[i]))
    	file_dir = base_dir + "/Annotations/"+'/'+ xmlfile +'.xml'
    	shutil.copy(file_dir,train_dir)
