#coding:utf-8
 
# pip install lxml
import argparse
import sys
import os
import json
import xml.etree.ElementTree as ET
 
START_BOUNDING_BOX_ID = 1

# #pascal class
# PRE_DEFINE_CATEGORIES = {
#     'aeroplane'   : 0,
#     'bicycle'     : 1,
#     'bird'        : 2,
#     'boat'        : 3,
#     'bottle'      : 4,
#     'bus'         : 5,
#     'car'         : 6,
#     'cat'         : 7,
#     'chair'       : 8,
#     'cow'         : 9,
#     'diningtable' : 10,
#     'dog'         : 11,
#     'horse'       : 12,
#     'motorbike'   : 13,
#     'person'      : 14,
#     'pottedplant' : 15,
#     'sheep'       : 16,
#     'sofa'        : 17,
#     'train'       : 18,
#     'tvmonitor'   : 19
# }

#pascal class
PRE_DEFINE_CATEGORIES = {"bej-bejnnbbt-dz-xcnnjrsnnw-46g": 28, "ch-chgzt-dz-sjw-45g": 45, "ch-chgzt-dz-ygw-45g": 44, "df-dfhfb-dz-nyw-168g": 19, "df-dfqkl-dz-shnnqkl-43g": 10, "glg-glgbcbg-hz-hjqklw-48g": 35, "glg-glgbqbg-hz-cmw-55g": 16, "glg-glgbqbg-hz-nnw-60g": 1, "glg-glgbqbg-hz-qklw-60g": 32, "glg-glgllbqbg-hz-lmw-45g": 24, "hly-hlydhp-hz-yw-138g": 12, "hly-hlyqklp-hz-qklw-204g": 46, "hly-hlyqtqkldg-hz-zzqklw-168g": 0, "hly-hlytlmsp-hz-yw-138g": 5, "hly-hlyytdst-dz-fqjw-70g": 40, "hly-hlyytdst-dz-ljnpw-70g": 26, "hn-hnwssgnyl-gz-yw-250ml": 9, "hy-hybfbgz-hz-xcw-200ml": 47, "kbk-kbksp-dz-fqw-60g": 31, "kbk-kbksp-dz-skw-60g": 6, "lj-ljlzkxt-pz-bhw-64g": 42, "mn-mnssr-hz-cmw-250ml": 2, "mn-mnssr-hz-yw-250ml": 22, "mn-zgl-hz-ygw-250ml": 36, "mz-mzxxb-pz-nnw-50g": 30, "mz-mzxxb-pz-qklw-50g": 39, "mzy-mzyglc-pz-czw-450ml": 11, "mzy-mzyglny-pz-blw-450ml": 43, "mzy-mzyglny-pz-mgw-450ml": 4, "nfsq-nfsqjjydyl-pz-nmw-550ml": 20, "nfsq-nfsqsrc-pz-nmw-445ml": 14, "pp-ppfsmb-dz-nxw-400g": 27, "pp-ppfsmb-dz-xcw-400g": 15, "qdpj-qdpj-gz-yw-330ml": 13, "wwsp-wznn-gz-yw-145ml": 23, "xhpj-xhqspj-gz-yw-330ml": 41, "yd-ydwtkxt-hz-rdsgw-32g": 3, "yd-ydwtkxt-pz-blbhw-56g": 18, "yd-ydwtkxt-pz-qsxgw-56g": 33, "yd-ydwtkxt-pz-xcbhw-56g": 37, "yd-ydwtkxt-pz-xnmgw-56g": 8, "yl-ylgldnn-hz-heiguw-250ml": 29, "yl-ylgldnn-hz-hongguw-250ml": 25, "yl-ylqqxetcznn-hz-jgx-125ml": 21, "yl-ylqqxetcznn-hz-qcx-125ml": 17, "yl-ylysr-hz-cmw-250ml": 34, "yl-ylysr-hz-yw-250ml": 38, "ys-zzyspyz-hz-yw-245ml": 7}
 
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
