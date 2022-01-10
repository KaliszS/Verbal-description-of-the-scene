import pandas as pd

def fuzzify_relative_coordinates(relative_positions):
    """ Function to fuzzify relative coordinates (separatively for x and y axis)

        * relative_positions - relative positions of points
        * each row is a row of relative positions dataframe
        * each field is a number of column in relative positions dataframe
        * each corner is a point (x, y)

        * return = set of descriptors for each coordinate ((x, y), (x', y'))
    """
    fuzzy0d = dict()
    for row in relative_positions.iterrows():
        fuzzy0d[row[0]] = dict()
        for field in range(0, len(relative_positions)):
            frame = tuple()
            for corner in row[1][field]:
                x_fuzz = estimate_fuzzy_position(corner[0], "x")
                y_fuzz = estimate_fuzzy_position(corner[1], "y")
                x_fuzz = get_non_zero_sets(x_fuzz)
                y_fuzz = get_non_zero_sets(y_fuzz)
                frame = *frame, (x_fuzz, y_fuzz)
            fuzzy0d[row[0]][field] = frame

    return pd.DataFrame.from_dict(fuzzy0d, orient='index').sort_index()

def estimate_fuzzy_position(point, coordinate):
    """
        * point - x or y coordinate of point
        * coordinate - "x" or "y" (information to get correct lingustic names for x or y axis)

        * return = dict of size 10 (counts trapezoidal function for each linguistic value)
            * sum of all trapezoidal functions = 1
    """
    fuzzy_dict = dict()
    parameters_matrix = get_fuzzy_parameters()
    for set in parameters_matrix:
        params = parameters_matrix[set]
        matrix_row = compute_trapezoidal_function(point, params[0], params[1], params[2], params[3])
        linguistic_set = set.split("/")
        linguistic_value = linguistic_set[0] if coordinate == "x" else linguistic_set[1]
        fuzzy_dict[linguistic_value] = matrix_row

    return fuzzy_dict

def get_fuzzy_parameters():
    """
        * m - margin
        * T1, T2 - zones thresholds
        * Inf, InfMinus - a way to represent infinities
    """
    m = 0.2
    T1 = 2
    T2 = 4
    Inf = 100
    InfMinus = -100

    parameters_matrix = {
        "fl/fa": (InfMinus, InfMinus, -T2-m, -T2+m),
        "nl/na": (-T2-m, -T2+m, -T1-m, -T1+m),
        "cl/ca": (-T1-m, -T1+m, -1-2*m, -1),
        "el/ea": (-1-2*m, -1, -1, -1+2*m),
        "il/ia": (-1, -1+2*m, -m, m),
        "ir/ib": (-m, m, 1-2*m, 1),
        "er/eb": (1-2*m, 1, 1, 1+2*m),
        "cr/cb": (1, 1+2*m, T1-m, T1+m),
        "nr/nb": (T1-m, T1+m, T2-m, T2+m),
        "fr/fb": (T2-m, T2+m, Inf, Inf)
    }

    return parameters_matrix

def compute_trapezoidal_function(p, a, b, c, d):
    """
        * p - x or y coordinate of point
        * a, b, c, d - trapezoidal function parameters
    """
    if p < a:
        return 0
    elif p < b:
        return (p - a) / (b - a)
    elif p < c:
        return 1
    elif p < d:
        return (d - p) / (d - c)
    else: # p >= d
        return 0

def get_non_zero_sets(f):
    """
        * f - fuzzy array of point coordinate (x or y)
        * return - list of non-zero sets (rounded to 2 decimal places)
    """
    non_zero_sets = dict()
    for variable in f:
        if f[variable] != 0:
            non_zero_sets[variable] = round(f[variable], 2)

    return non_zero_sets