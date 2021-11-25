import pandas as pd
import numpy as np
import json

def load_instances(subset, root): 
    instances_file_path = root + "annotations/instances_" + subset + ".json"

    categories_dict = dict()
    box_images = dict()
    box_categories = dict()
    box_bboxes = dict()

    image_bboxes = dict()
    supercategory = dict()
    category_name = dict()

    with open(instances_file_path) as file:
        json_data = json.load(file)
        annotations = json_data["annotations"]
        categories = json_data["categories"]

    for category in categories:
        categories_dict[category["id"]] = category["supercategory"] + ":" + category["name"]

    for item in annotations:
        box_images[item["id"]] = item["image_id"]
        box_categories[item["id"]] = item["category_id"]
        box_bboxes[item["id"]] = item["bbox"]

    for b_cat in box_categories:
        image_id = box_images[b_cat]
        category_id = box_categories[b_cat]
        if image_id not in category_name:
            supercategory[image_id] = np.empty((0,1))
            category_name[image_id] = np.empty((0,1))
        supername, name = categories_dict[category_id].split(":")
        supercategory[image_id] = np.append(supercategory[image_id], supername) 
        category_name[image_id] = np.append(category_name[image_id], name)


    for b_box in box_bboxes:
        image_id = box_images[b_box]
        bbox = box_bboxes[b_box]
        if image_id not in image_bboxes:
            image_bboxes[image_id] = np.empty((0,4))
        image_bboxes[image_id] = np.append(image_bboxes[image_id], np.array(bbox))

    #df = pd.DataFrame({"super category": supercategory, "category": category_name, "bbox": image_bboxes})
    columns = supercategory, category_name, image_bboxes
    return columns