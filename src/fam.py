def compute_realative_coordinates(bbox_r, p):
    P = 2*(p - bbox[0])/(bbox_r[1] - bbox[0]) - 1
    
    return P
    

def transform_cooridnates(bbox):
    p1 = bbox[0], bbox[1]
    p2 = bbox[0] + bbox[2], bbox[1] + bbox[3]
    
    pass


