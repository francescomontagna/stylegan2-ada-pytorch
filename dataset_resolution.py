"""
Script for custom resizing of the dataset.
Differently from dataset_tools, it allows resizing using thumbnail, keeping all the image content.
It also allows padding rather than cropping to get squared images
"""

import os
import numpy as np

from PIL import Image
from util import resize


def main():
    target_dim = 256
    src_folder = "datasets/raw/modigliani-highres-squared"
    dest_folder = f"datasets/raw/modigliani-highres-{target_dim}"

    try:
        os.makedirs(dest_folder)
    except:
        print("Removing destination folder...")
        os.system(f"rm -r {dest_folder}")
        os.makedirs(dest_folder)

    resize(src_folder, dest_folder, target_dim, pad = False)
        

main()