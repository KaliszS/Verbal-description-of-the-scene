import cv2
from utils.aggregate import draw_bboxes, unpickle
from utils.support_functions import load_config, create_filename, count_img_index
from src.relative_coordinates import transform_cooridnates
from src.fuzzification import fuzzify_relative_coordinates
from src.fam1d import fuzzy_reason_for_fam1d
from src.fam2d import fuzzy_reason_for_fam2d

config = load_config()

root = config["root"] + "img/"
subset = config["subset"]
edition = config["edition"]
subsetEdition = subset + edition
directory = root + subsetEdition + "/"

pickle_filename = config["pickle_filename"]
data = unpickle(pickle_filename)

order= 0

while(1):
    k = cv2.waitKey(0) & 0xFF
    
    if k == 27: # ESC
        break
    elif k == ord('q'):
        if order < len(data) - 1:
            order += 1
    elif k == ord('a'):
        if order > 0:
            order -= 1
    elif k == ord('w'):
        if order < len(data) - 1:
            order += 10
    elif k == ord('s'):
        if order > 0:
            order -= 10
    elif k == ord('e'):
        if order < len(data) - 1:
            order += 100
    elif k == ord('d'):
        if order > 0:
            order -= 100
    elif k == ord('r'):
        if order < len(data) - 1:
            order += 1000
    elif k == ord('f'):
        if order > 0:
            order -= 1000
    
    img_index = count_img_index(data, order)
    path = directory + create_filename(img_index, subsetEdition)
    image = cv2.imread(path)
    bbox = data.loc[img_index, "bbox"]
    category = data.loc[img_index, "category"]
    color = data.loc[img_index, "color"]
    size = data.loc[img_index, "size"]
    
    relative_coordinates = transform_cooridnates(bbox, size)
    fuzzification = fuzzify_relative_coordinates(relative_coordinates)
    fam1 = fuzzy_reason_for_fam1d(fuzzification)
    fam2 = fuzzy_reason_for_fam2d(fam1)
    
    draw_bboxes(image, bbox, category, color)
    cv2.imshow("Picture", image)
    
    print(f"========== Picture ID: {img_index} ==========")
    for cap in data.loc[img_index, :"caption5"]:
        print(cap)
    print("========================================")


cv2.destroyAllWindows() 
