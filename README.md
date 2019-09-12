# voc2coco
Tansform pascal voc data to coco data format.

## Run

1. rename data
```bash
python rename_data.py
```

2. split data to train,valid,test
```bash
python split_data.py
```

3.split image
```bash
python split_image.py
```

4.tranform xml to json
```bash
python xml2json.py
```

* NOTE THAT *
modify the data path of yourself.
