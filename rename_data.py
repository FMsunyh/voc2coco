# coding utf-8
import argparse
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


parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-i', '--input',help='path of data', default='/home/syh/pascal_voc/')
args = parser.parse_args()
 
if __name__ == '__main__':
    xml_path = os.path.join(args.input, 'Annotations/' )
    img_path = os.path.join(args.input, 'JPEGImages/' )
    
    print(xml_path)
    print(img_path)
    
    rename_data(xml_path, img_path)

'''
this script will rewrite the origin data.
'''

'''
python voc2coco/rename_data.py -i /home/syh/cornernet-lite/data/voc/
'''