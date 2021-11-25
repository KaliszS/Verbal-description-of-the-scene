import json
import os

def create_filename(id, subset):
    config = load_config()
    subsetEdition = subset + "_"
    prefix = config["file_prefix"]
    length = config["file_id_length"]
    ext = config["file_extension"]
    filename = prefix + subsetEdition + str(id).zfill(length) + ext
    return filename

def count_img_index(df, order):
    return df.iloc[order:order+1, 0].index[0]

def load_config():
    with open(define_path("config.json")) as json_config:
        config = json.load(json_config)
    return config

def define_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)