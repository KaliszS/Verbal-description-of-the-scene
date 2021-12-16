import pandas as pd

def transform_cooridnates(bbox, size):
    """ Transform coordinates of objects into relative ones
        1 reference object = 1 row
        Every object in a row has coordinates transformed into a relative ones

        * return = DataFrame(
            indexes = ids of relative object,
            columns = ids of every objects,
            data = coordinates of every objects relative to every other objects
        )
    """
    bbox_entire_image = add_entire_image_coordinates(size)
    img_objects = load_bboxes(bbox)
    img_objects.append(bbox_entire_image)
    relatives_position_box = dict()

    for o in img_objects:
        X = list()
        Y = list()
        ref_object = o
        ref_id = ref_object[0]
        ref_x_coords = ref_object[1][0], ref_object[2][0]
        ref_y_coords = ref_object[1][1], ref_object[2][1]

        for o_inner in img_objects:
            if o_inner[0] == ref_id:
                continue
            else:
                x_1 = compute_realative_coordinates(ref_x_coords, o_inner[1][0])
                x_2 = compute_realative_coordinates(ref_x_coords, o_inner[2][0])
                X.append((x_1, x_2))
                
                y_1 = compute_realative_coordinates(ref_y_coords, o_inner[1][1])
                y_2 = compute_realative_coordinates(ref_y_coords, o_inner[2][1])
                Y.append((y_1, y_2))
        
        relatives_position_box[ref_id] = [((x[0], y[0]), (x[1], y[1])) for x, y in zip(X, Y)]
    
    return pd.DataFrame.from_dict(relatives_position_box, orient='index').sort_index()

def add_entire_image_coordinates(size):
    """ Add bbox coordinates of entire image with id = 0

        * size = (width, height)
        * return = (id, (x_1, y_1), (x_2, y_2))
    """
    return 0, (0, 0), (size[0], size[1])

def load_bboxes(bbox):
    """ Transform bbox into a list of objects

        * bbox = [x_1, y_1, r_x, r_y, ...]
            -> 4 elements per object
            -> x_2 = x_1 + r_x
            -> y_2 = y_1 + r_y

        * return = [(id, (x_1, y_1), (x_2, y_2)), (...), ...]
    """
    img_objects = list()
    for i in range(0, len(bbox), 4):
        id = int(i/4+1)
        img_objects.append(define_object_edges(id, bbox[i:i+4]))
    
    return img_objects

def define_object_edges(id, edges):
    """ Transform bbox of 1 object into its edge coordinates

        * return = (id, (x_1, y_1), (x_2, y_2))
    """
    edgeRight = round(edges[0]), round(edges[1])
    edgeLeft = round(edges[0] + edges[2]), round(edges[1] + edges[3])

    return id, edgeRight, edgeLeft

def compute_realative_coordinates(bbox_r, p):
    """
        * bbox_r = (x_1, x_2) or (y_1, y_2)
        * p = original x or y coordinate of transforming point

        * return = relative x or y coordinate of transformed p
    """
    P = 2*(p - bbox_r[0])/(bbox_r[1] - bbox_r[0]) - 1
    
    return P

