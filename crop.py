from util import crop
import argparse

"""
For info on how crop is done see util.crop and https://stackoverflow.com/questions/9983263/how-to-crop-an-image-using-pil
"""


def parse_arguments():
    parser = argparse.ArgumentParser(description="Crop parameters", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--file", type=str, 
        help="filename of the target image. Must be in the src_folder"
    )
    parser.add_argument("--width", type=int, default=512, 
        help="width of the cropped image"
    )
    parser.add_argument("--height", type=int, default=512, 
        help="height of the cropped image"
    )
    parser.add_argument("--src_folder", type=str, default="projections/images", 
        help="Folder with the target image"
    )
    parser.add_argument("--dest_folder", type=str, default="projections/tmp", 
        help="Folder to store the cropped image"
    )
    parser.add_argument("--flexible", type=bool, default=False, 
        help="Folder to store the cropped image"
    )

    return parser.parse_args()


args = parse_arguments()
crop(args.file, args.flexible, args.src_folder, args.dest_folder, args.width, args.height)