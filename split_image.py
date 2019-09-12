# -*- coding:utf-8 -*-

import os
import numpy as np
import shutil

def split_img(xml_dir,origin_img,img_dir):
    xml_files = os.listdir(xml_dir)
    for xml in xml_files: 
    	originimg_path = origin_img + xml[:-4] + ".jpg"
    	newimg_path = img_dir + xml[:-4] + ".jpg"
    	print(shutil.copy(originimg_path,newimg_path))

if __name__ == '__main__':
    folder_list= ["train","val","test"]

    base_dir = "/save_path/data/pascal_voc/"
    origin_img = base_dir + "fullimages/" 
    for i in range(3):
        folder_name = folder_list[i]
        xml_dir = base_dir + folder_name + "/Annotations/"
        if not os.path.exists(xml_dir):
        	os.makedirs(xml_dir)
        img_dir = base_dir + "/images/" + folder_name + "/"
        if not os.path.exists(img_dir):
        	os.makedirs(img_dir)
        print(img_dir)
        split_img(xml_dir,origin_img,img_dir)
