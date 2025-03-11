#!/usr/bin/env python3
"""
Reads SURP dataset containing data of 21 subjects, each consisting of
* metadata in file meta.yaml
* time series data in file [object].pts with the following data columns:
-------------------------------------------
X Y Z Time[s] RX RY RZ RW FX FY FZ TX TY TZ
-------------------------------------------
X,Y,Z: position of the tracker w.r.t. calibration station
RX, RY, RZ, RW: Quaternion orientation (scalar-last convention) of the tracker w.r.t. calibration station
Time[s]: time in seconds
FX, FY, FZ: forces in FTS sensor frame
TX, TY, TZ: moments in FTS sensor frame

Translation in (x,y,z) from Vive tracker to sanding tool finishing disk center point: [0, 0, 0.2227]
"""


import os
import yaml
import numpy as np


# Adapt to dataset root path:
data_root_directory = "SURP"


def parse_pts_file(file_path):
    parsed_data = []
    
    with open(file_path, 'r') as file:
        # Skip the first line (header)
        next(file)
        
        for line in file:
            values = line.split()
            parsed_values = [float(val) for val in values]
            parsed_data.append(parsed_values)
    
    return np.array(parsed_data)


subjects = [f"{s:02d}" for s in range(1,22)] # from subject 01 to 21
workpieces = ["box", "sphere", "cylinder", "wooden_corners"]

for s in subjects:
    meta_file_path = os.path.join(data_root_directory, s, "meta.yaml")
    with open(meta_file_path, "r") as file:
        meta_data = yaml.safe_load(file)
        print(f"subject: {s}", meta_data)
    
    for w in workpieces:
        
        file_path = os.path.join(data_root_directory, s, w + ".pts")
        data = parse_pts_file(file_path)

        # do something with data here
        print(f"\tworkpiece: {w}, data shape: {data.shape}")
