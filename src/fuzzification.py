import pandas as pd

def fuzzify_relative_coordinates(relative_positions):
    """
    row - wiersz po wierszy, field - potrzebuję numeru kolumny, a kolumn jest tyle co wierszy
    edge - to punkty, np (0,0)

    """
    fuzzy = dict()
    for row in relative_positions.iterrows():
        fuzzy[row[0]] = dict()
        for field in range(0, len(relative_positions)):
            frame = tuple()
            for edge in row[1][field]:
                x_fuzz = estimate_fuzzy_position(edge[0], "x")
                y_fuzz = estimate_fuzzy_position(edge[1], "y")
                frame = *frame, (x_fuzz, y_fuzz)
            fuzzy[row[0]][field] = frame

    return pd.DataFrame.from_dict(fuzzy, orient='index').sort_index()

def estimate_fuzzy_position(point, coordinate):
    """

    """
    fuzzy_list = list()
    parameters_matrix = get_fuzzy_parameters()
    for set in parameters_matrix:
        params = parameters_matrix[set]
        matrix_row = compute_trapezoidal_function(point, params[0], params[1], params[2], params[3])
        fuzzy_list.append(matrix_row)

    return fuzzy_list

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

def get_fuzzy_descriptors():
    f = "far"
    n = "near"
    c = "close"
    e = "edge"
    i = "inside"

    l = "left"
    r = "right"
    a = "above"
    b = "below"

    zones = {"f": f, "n": n, "c": c, "e": e, "i": i}
    ling_values = {"l": l, "r": r, "a": a, "b": b}


    pass
