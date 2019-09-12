# coding utf-8
import os, shutil
import random
import numpy as np
 
def rename_data(xml_path, img_path):
    xmlFiles = os.listdir(xml_path)
    total = len(xmlFiles)
    cur = 0
    for xml in xmlFiles:
        cur += 1
        if cur % 500 == 1:
            print("Total/cur:", total, "/", cur)
        imgPath = img_path + xml[:-4] + ".jpg"
        
        outName = ("%08d" % (cur))
        
        outXMLPath = ("%s/%s.xml" % (xml_path,outName))
        outImgPath = ("%s/%s.jpg" % (img_path,outName))
        
        os.rename(xml_path+xml,outXMLPath)
        os.rename(imgPath,outImgPath)
        
    
    print("picker number:",cur)
    
 
if __name__ == '__main__':
    xml_path = "/path-to-voc-data/Annotations/"    
    img_path = "/path-to-voc-data/JPEGImages/"
    
    print(xml_path)
    print(img_path)
    
    rename_data(xml_path, img_path)
