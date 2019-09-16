#coding:utf-8
 
# pip install lxml
import argparse
import sys
import os
import json
import xml.etree.ElementTree as ET
 
START_BOUNDING_BOX_ID = 1

#pascal class
PRE_DEFINE_CATEGORIES = {
    'aeroplane'   : 0,
    'bicycle'     : 1,
    'bird'        : 2,
    'boat'        : 3,
    'bottle'      : 4,
    'bus'         : 5,
    'car'         : 6,
    'cat'         : 7,
    'chair'       : 8,
    'cow'         : 9,
    'diningtable' : 10,
    'dog'         : 11,
    'horse'       : 12,
    'motorbike'   : 13,
    'person'      : 14,
    'pottedplant' : 15,
    'sheep'       : 16,
    'sofa'        : 17,
    'train'       : 18,
    'tvmonitor'   : 19
}
 
def get(root, name):
    vars = root.findall(name)
    return vars
 
 
def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars
 
 
def get_filename_as_int(filename):
    try:
        filename = os.path.splitext(filename)[0]
        return int(filename)
    except:
        raise NotImplementedError('Filename %s is supposed to be an integer.'%(filename))
 
 
def convert(xml_dir, json_file):
    xml_files = os.listdir(xml_dir)
    
    json_dict = {"images":[], "type": "instances", "annotations": [],
                 "categories": []}
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    num = 0
    for line in xml_files:
#         print("Processing %s"%(line))
        num +=1
        if num%50==0:
            print("processing ",num,"; file ",line)
        #print("processing ",num,"; file ",line)
        xml_f = os.path.join(xml_dir, line)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        ## The filename must be a number
        filename = line[:-4]
        image_id = get_filename_as_int(filename)
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        # image = {'file_name': filename, 'height': height, 'width': width,
        #          'id':image_id}
        image = {'file_name': (filename+'.jpg'), 'height': height, 'width': width,
                 'id':image_id}
        json_dict['images'].append(image)
        ## Cruuently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category == 'mtdown':
                print(category,',',line)
            if category == 'ebikedown':
                print(category,',',line)
            if category not in categories:
                print(category,',',line)
                new_id = len(categories)
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(get_and_check(bndbox, 'xmin', 1).text) - 1
            ymin = int(get_and_check(bndbox, 'ymin', 1).text) - 1
            xmax = int(get_and_check(bndbox, 'xmax', 1).text)
            ymax = int(get_and_check(bndbox, 'ymax', 1).text)
            #print(xmin,xmax,ymin,ymax)
            assert(xmax > xmin)
            assert(ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'area': o_width*o_height, 'iscrowd': 0, 'image_id':
                   image_id, 'bbox':[xmin, ymin, o_width, o_height],
                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                   'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1
 
    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()


parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-i', '--input', help='path of data', default='/home/syh/pascal_voc/')
args = parser.parse_args()

if __name__ == '__main__':

    base_dir = args.input

    folder_list= ["train","val","test"]

    for i in range(3):
        folder_name = folder_list[i]
        #xml_dir = base_dir + folder_name + "/"
        xml_dir = base_dir + folder_name + "/Annotations/"
        json_dir = base_dir + folder_name + "/instances_" + folder_name + ".json"
        
        print("deal: ",folder_name)
        print("xml dir: ",xml_dir)
        print("json file: ",json_dir)
        
        convert(xml_dir,json_dir)
