import pandas as pd
import os.path
import cv2
from utils.support_functions import load_config
from utils.captions import load_objects
from utils.instances import load_instances

def merge_columns(df1, df2):
    df = pd.DataFrame({"caption1": df1[0], "caption2": df1[1], "caption3": df1[2], "caption4": df1[3], "caption5": df1[4], "super category": df2[0], "category": df2[1], "bbox": df2[2]})
    df = df.sort_index()
    return df

def draw_bboxes(image, bbox, category):
    points_x = list()
    points_y = list()
    points = list()
    categories = list()

    for i in category:
        categories.append(i)

    for i in range(0, len(bbox), 4):
        points_x.append(round(bbox[i]))
        points_y.append(round(bbox[i+1]))
        points_x.append(round(bbox[i]) + round(bbox[i+2]))
        points_y.append(round(bbox[i+1]) + round(bbox[i+3]))

    for i in range(0, len(points_x)):
        points.append((points_x[i], points_y[i]))
    
    for i in range(0, len(points), 2):
        cv2.rectangle(image, points[i], points[i+1], (50,50,250), 1)
        cv2.putText(image, categories[int(i/2)], (points[i][0], points[i][1] - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50,50,250), 1)

def pickle(df, filename):
    df.to_pickle(filename)

def unpickle(filename):
    config = load_config()
    root = config["root"]
    subset = config["subset"]
    edition = config["edition"]
    subsetEdition = subset + edition

    if os.path.isfile(root + filename):
        pass
    else:
        data = merge_columns(load_objects(subsetEdition, root + "img/"), load_instances(subsetEdition, root + "img/"))
        pickle(data, filename)

    return pd.read_pickle(root + filename)

