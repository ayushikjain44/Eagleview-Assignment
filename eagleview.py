# -*- coding: utf-8 -*-
"""eagleview.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rDE6ezmldyyAEvzp7D13hXkgTaijMHs7
"""

cd /content/drive/MyDrive/assignment_place/ayushi/eagleview

from google.colab import drive
drive.mount('/content/drive')

ls

!tar -xzvf "/content/drive/MyDrive/assignment_place/ayushi/eagleview/trainval.tar.gz" -C "/content/drive/MyDrive/assignment_place/ayushi/eagleview"

cp -r /content/drive/MyDrive/assignment_place/ayushi/eagleview/trainval/images /content/drive/MyDrive/assignment_place/ayushi/eagleview/training/

def convert_bbox_coco2yolo(img_width, img_height, bbox):
    """
    Convert bounding box from COCO  format to YOLO format

    Parameters
    ----------
    img_width : int
        width of image
    img_height : int
        height of image
    bbox : list[int]
        bounding box annotation in COCO format: 
        [top left x position, top left y position, width, height]

    Returns
    -------
    list[float]
        bounding box annotation in YOLO format: 
        [x_center_rel, y_center_rel, width_rel, height_rel]
    """
    
    # YOLO bounding box format: [x_center, y_center, width, height]
    # (float values relative to width and height of image)
    x_tl, y_tl, w, h = bbox

    dw = 1.0 / img_width
    dh = 1.0 / img_height

    x_center = x_tl + w / 2.0
    y_center = y_tl + h / 2.0

    x = x_center * dw
    y = y_center * dh
    w = w * dw
    h = h * dh

    return [x, y, w, h]

import os
import json
from tqdm import tqdm
import shutil

def make_folders(path="output"):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path


def convert_yolo(output_path, json_file):

    path = make_folders(output_path)

    with open(json_file) as f:
        json_data = json.load(f)

    # write _darknet.labels, which holds names of all classes (one class per line)
    label_file = os.path.join(output_path, "_yoloformat.labels")
    with open(label_file, "w") as f:
        for category in tqdm(json_data["categories"], desc="Categories"):
            category_name = category["name"]
            f.write(f"{category_name}\n")

    for image in tqdm(json_data["images"], desc="Annotation txt for each iamge"):
        img_id = image["id"]
        img_name = image["file_name"]
        img_width = image["width"]
        img_height = image["height"]

        anno_in_image = [anno for anno in json_data["annotations"] if anno["image_id"] == img_id]
        anno_txt = os.path.join(output_path, img_name.split(".")[0] + ".txt")
        with open(anno_txt, "w") as f:
            for anno in anno_in_image:
                category = int(anno["category_id"]) -1
                bbox_COCO = anno["bbox"]
                x, y, w, h = convert_bbox_coco2yolo(img_width, img_height, bbox_COCO)
                f.write(f"{category} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

    print("Converting COCO Json to YOLO txt finished!")

if __name__ == '__main__':
    convert_yolo('/content/drive/MyDrive/assignment_place/ayushi/eagleview/bbox-annotations','/content/drive/MyDrive/assignment_place/ayushi/eagleview/trainval/annotations/bbox-annotations.json')

pwd

# Commented out IPython magic to ensure Python compatibility.
#!git clone https://github.com/ultralytics/yolov5  # clone
#%cd yolov5
# %pip install -qr requirements.txt  # install

# import torch
# from yolov5 import utils
# display = utils.notebook_init()  # checks

pwd

# Commented out IPython magic to ensure Python compatibility.
# %cd yolov5

!python train.py --img 640 --batch 16 --epochs 50 --data dataset.yaml --weights yolov5s.pt --cache

