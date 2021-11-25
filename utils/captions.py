import pandas as pd
import json

def load_objects(subset, root): 
    captions_file_path = root + "annotations/captions_" + subset + ".json"

    img_index_counter = dict() 
    captions_ids = dict()
    captions = dict()

    caption1 = dict()
    caption2 = dict()
    caption3 = dict()
    caption4 = dict()
    caption5 = dict()
    captionsList = [caption1, caption2, caption3, caption4, caption5]

    with open(captions_file_path) as file:
        json_data = json.load(file)
        annotations = json_data["annotations"]

    for item in annotations:
        if img_index_counter is not None and item["image_id"] not in img_index_counter:
            img_index_counter[item["image_id"]] = 1

        captions_ids[item["id"]] = item["image_id"]
        captions[item["id"]] = item["caption"]
    
    for cap in captions:
        for i in range(len(captionsList)):
            if img_index_counter[captions_ids[cap]] == i+1:
                captionsList[i][captions_ids[cap]] = captions[cap]
        
        img_index_counter[captions_ids[cap]] += 1

    #df = pd.DataFrame({"caption1": caption1, "caption2": caption2, "caption3": caption3, "caption4": caption4, "caption5": caption5})
    columns = caption1, caption2, caption3, caption4, caption5
    return columns