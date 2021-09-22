import os
import numpy as np

from PIL import Image
from util import resize

def main():
    target_dim = 512
    src_folder = "datasets/raw/modigliani"
    dest_folder = f"datasets/raw/resized-{target_dim}/modigliani"
    folders = ["pinterest-modigliani", "wikiart-modigliani"]

    try:
        os.makedirs(dest_folder)
    except:
        print("Removing destination folder...")
        os.system(f"rm -r {dest_folder}")
        os.makedirs(dest_folder)

    for folder in folders:
        resize(src_folder + "/" + folder, dest_folder, target_dim, pad = True)
        

main()