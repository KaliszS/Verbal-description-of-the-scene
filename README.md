# What is needed to run application?

1. Spyder & Python 3.8+ (with cv2 installed)
2. COCO images datasets and annotations
    - https://cocodataset.org/#download

# Project structure
- <root_directory>
    - /img
        - /annotations
            - *.json
        - /train2014 (for example)
            - *.jpg
        - /val2014 (for example)
            - *.jpg
        - /src
        - /utils
        - main.py
        - *.pkl

# How to run application?

0. Enter your <root_directory> and pickle file name into /utils/config.json
1. Open and run main.py in Spyder
2. Navigation:
    - ESC to close application
    - q & a -> move forwad/backward by 1 picture
    - w & s -> move forwad/backward by 10 pictures
    - e & d -> move forwad/backward by 100 pictures
    - r & f -> move forwad/backward by 1000 pictures

First start of each dataset may be slower, because application needs to pickle data first.