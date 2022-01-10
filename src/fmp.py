import pandas as pd

def generate_predicates(bbox, fam2):
    areas = count_size(bbox)
    predicates = []
    for object in areas:
        variables = fam2.loc[object[0]]
        variables.drop([object[0]])
        print(variables)
        most_important_variable = count_saliency(variables)
        print(most_important_variable)

def count_size(bbox):
    areas = {}

    for i in range(0, len(bbox), 4):
        id = int(i/4+1)
        size = bbox[i+2] * bbox[i+3]
        areas[id] = size

    sorted_areas = sorted(areas.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_areas

def count_saliency(variables):
    saliency = get_saliency()
    variable = variables[0][0].split("/")[0]
    for v in variables:
        v = v[0].split("/")[0]
        if saliency[v] > saliency[variable]:
            variable = v

    return variable

def get_saliency():
    saliency = {
        "FA": 0.6,
        "NE": 0.7,
        "CL": 0.8,
        "TO": 0.9,
        "CR": 0.9,
        "IN": 0.8,
        "LG": 0.3,
        "SP": 0.9,
        "SA": 1
    }

    return saliency