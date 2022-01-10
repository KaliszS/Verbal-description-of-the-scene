import pandas as pd

def fuzzy_reason_for_fam1d(fuzzyfied_coordinates):
    """ Function to get fuzzy descriptors for edges

        * return = pair of descriptors for each edge (x, y)
    """
    fuzzy1d = dict()
    for row in fuzzyfied_coordinates.iterrows():
        fuzzy1d[row[0]] = dict()
        for field in range(0, len(fuzzyfied_coordinates)):
            x1 = row[1][field][0][0]
            y1 = row[1][field][0][1]
            x2 = row[1][field][1][0]
            y2 = row[1][field][1][1]

            edge_x = estimate_fuzzy_positions(x1, x2, "x")
            edge_y = estimate_fuzzy_positions(y1, y2, "y")

            edge_x = get_maximum(edge_x)
            edge_y = get_maximum(edge_y)

            fuzzy1d[row[0]][field] = (edge_x, edge_y)
            
    return pd.DataFrame.from_dict(fuzzy1d, orient='index').sort_index()

def estimate_fuzzy_positions(p1, p2, coordinate):
    """
        * p1, p2 - x or y coordinates of corners
        * coordinate - "x" or "y" (information to get correct lingustic names for x or y axis)
    """
    fuzzy_descriptors = get_1d_fuzzy_descriptos()
    map_y2x = fuzzy_descriptors[0]
    map_1d = fuzzy_descriptors[1]
    fam1_matrix = fuzzy_descriptors[2]

    descriptors = dict()
    for d1 in p1:
        for d2 in p2:
            if coordinate == "y":
                d = fam1_matrix.loc[map_y2x[d1], map_y2x[d2]]
            else:
                d = fam1_matrix.loc[d1, d2]
            if d == "-":
                continue
            d = get_axis_direction(d, coordinate, map_1d)
            descriptors[d] = get_minimum(p1[d1], p2[d2])

    return descriptors

def get_1d_fuzzy_descriptos():
    """
        * return = tuple of maps to bind x-y edges and fam1 table
    """
    y_to_x_0d = {
        "fa": "fl",
        "na": "nl",
        "ca": "cl",
        "ea": "el",
        "ia": "il",
        "ib": "ir",
        "eb": "er",
        "cb": "cr",
        "nb": "nr",
        "fb": "fr",
    }

    x_to_y_1d = {
        "L": "A",
        "R": "B",
        "H": "V"
    }

    descriptors = {
        "fl": ["FA/L", "NE/L", "CL/L", "TO/L", "CR/L", "CR/L", "CR/L", "LO/H", "LO/H", "LO/H"],
        "nl": ["-", "NE/L", "CL/L", "TO/L", "CR/L", "CR/L", "CR/L", "LO/H", "LO/H", "LO/H"],
        "cl": ["-", "-", "CL/L", "TO/L", "CR/L", "CR/L", "CR/L", "LO/H", "LO/H", "LO/H"],
        "el": ["-", "-", "-", "TO/L", "IN/L", "IN/L", "SA/H", "CR/R", "CR/R", "CR/R"],
        "il": ["-", "-", "-", "-", "IN/L", "SH/H", "IN/R", "CR/R", "CR/R", "CR/R"],
        "ir": ["-", "-", "-", "-", "-", "IN/R", "IN/R", "CR/R", "CR/R", "CR/R"],
        "er": ["-", "-", "-", "-", "-", "-", "TO/R", "TO/R", "TO/R", "TO/R"],
        "cr": ["-", "-", "-", "-", "-", "-", "-", "CL/R", "CL/R", "CL/R"],
        "nr": ["-", "-", "-", "-", "-", "-", "-", "-", "NE/R", "NE/R"],
        "fr": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "FA/R"]
    }

    df = pd.DataFrame.from_dict(descriptors, orient='index', columns=["fl", "nl", "cl", "el", "il", "ir", "er", "cr", "nr", "fr"])

    return y_to_x_0d, x_to_y_1d, df

def get_axis_direction(d, coordinate, map):
    desc = d.split("/")[0]
    dir = d.split("/")[1]

    if coordinate == "y":
        dir = map[dir]

    return desc + "/" + dir

def get_minimum(d1, d2):
    if d1 < d2:
        return d1
    else:
        return d2

def get_maximum(edge):
    max_value = 0
    variable = ""
    for key in edge.keys():
        if edge[key] > max_value:
            max_value = edge[key]
            variable = key

    return {variable: max_value}
    