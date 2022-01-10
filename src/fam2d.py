import pandas as pd

def fuzzy_reason_for_fam2d(fam1):
    fuzzy2d = dict()
    for row in fam1.iterrows():
        fuzzy2d[row[0]] = dict()
        for field in range(0, len(fam1)):
            x = row[1][field][0]
            y = row[1][field][1]

            descriptor2d = estimate_fuzzy_positions(x, y)
            
            fuzzy2d[row[0]][field] = descriptor2d

    return pd.DataFrame.from_dict(fuzzy2d, orient='index').sort_index()

def estimate_fuzzy_positions(x, y):
    fuzzy_descriptors = get_2d_fuzzy_descriptos()
    d = fuzzy_descriptors.loc[y, x]

    return d.values[0]

def get_2d_fuzzy_descriptos():
    descriptors = {
        "FA/A": ["FA/LA", "FA/LA", "FA/LA", "FA/AB", "FA/AB", "FA/AB", "FA/AB", "FA/AB", "FA/AB", "FA/AB", "FA/AB", "FA/AB", "FA/RA", "FA/RA", "FA/RA"],
        "NE/A": ["FA/LA", "NE/LA", "NE/LA", "NE/LA", "NE/AB", "NE/AB", "NE/AB", "NE/AB", "NE/AB", "NE/AB", "NE/AB", "NE/RA", "NE/RA", "NE/RA", "FA/RA"],
        "CL/A": ["FA/LA", "NE/LA", "CL/LA", "CL/LA", "CL/AB", "CL/AB", "CL/AB", "CL/AB", "CL/AB", "CL/AB", "CL/AB", "CL/RA", "CL/RA", "NE/RA", "FA/RA"],
        "TO/A": ["FA/LE", "NE/LA", "CL/LA", "TO/LA", "TO/LA", "TO/AB", "TO/AB", "TO/AB", "TO/AB", "TO/AB", "TO/RA", "TO/RA", "CL/RA", "NE/RA", "FA/RI"],
        "CR/A": ["FA/LE", "NE/LE", "CL/LE", "TO/LA", "CR/LA", "CR/AB", "CR/AB", "CR/AB", "CR/AB", "CR/AB", "CR/RA", "TO/RA", "CL/RI", "NE/RI", "FA/RI"],
        "IN/A": ["FA/LE", "NE/LE", "CL/LE", "TO/LE", "CR/LE", "IN/LA", "IN/AB", "IN/AB", "SP/AB", "IN/RA", "CR/RI", "TO/RI", "CL/RI", "NE/RI", "FA/RI"],
        "SH/V": ["FA/LE", "NE/LE", "CL/LE", "TO/LE", "CR/LE", "IN/LE", "IN/CE", "SP/HO", "SP/HO", "IN/RI", "CR/RI", "TO/RI", "CL/RI", "NE/RI", "FA/RI"],
        "SA/V": ["FA/LE", "NE/LE", "CL/LE", "TO/LE", "CR/LE", "IN/LE", "SP/VE", "SA/CE", "LG/HO", "IN/RI", "CR/RI", "TO/RI", "CL/RI", "NE/RI", "FA/RI"],
        "LO/V": ["FA/LE", "NE/LE", "CL/LE", "TO/LE", "CR/LE", "SP/LE", "SP/VE", "LG/VE", "LG/CE", "SP/RI", "CR/RI", "TO/RI", "CL/RI", "NE/RI", "FA/RI"],
        "IN/B": ["FA/LE", "NE/LE", "CL/LE", "TO/LE", "CR/LE", "IN/LB", "IN/BE", "IN/BE", "SP/BE", "IN/RB", "CR/RI", "TO/RI", "CL/RI", "NE/RI", "FA/RI"],
        "CR/B": ["FA/LE", "NE/LE", "CL/LE", "TO/LB", "CR/LB", "CR/BE", "CR/BE", "CR/BE", "CR/BE", "CR/BE", "CR/RB", "TO/RB", "CL/RI", "NE/RI", "FA/RI"],
        "TO/B": ["FA/LE", "NE/LB", "CL/LB", "TO/LB", "TO/LB", "TO/BE", "TO/BE", "TO/BE", "TO/BE", "TO/BE", "TO/RB", "TO/RB", "CL/RB", "NE/RB", "FA/RI"],
        "CL/B": ["FA/LB", "NE/LB", "CL/LB", "CL/LB", "CL/BE", "CL/BE", "CL/BE", "CL/BE", "CL/BE", "CL/BE", "CL/BE", "CL/RB", "CL/RB", "NE/RB", "FA/RB"],
        "NE/B": ["FA/LB", "NE/LB", "NE/LB", "NL/LB", "NE/BE", "NE/BE", "NE/BE", "NE/BE", "NE/BE", "NE/BE", "NE/BE", "NE/RB", "NE/RB", "NE/RB", "FA/RB"],
        "FA/B": ["FA/LB", "FA/LB", "FA/LB", "FA/BE", "FA/BE", "FA/BE", "FA/BE", "FA/BE", "FA/BE", "FA/BE", "FA/BE", "FA/BE", "FA/RB", "FA/RB", "FA/RB"]
    }

    df = pd.DataFrame.from_dict(descriptors, orient='index', columns=["FA/L", "NE/L", "CL/L", "TO/L", "CR/L", "IN/L", "SH/H", "SA/H", "LO/H", "IN/R", "CR/R", "TO/R", "CL/R", "NE/R", "FA/R"])

    return df