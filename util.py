import os
import numpy as np

from PIL import Image
from tqdm import tqdm


def max_min_dim(max_w, max_h, min_w, min_h, base_folder):
    """
    Find the smallest and the largest width and height for images in a folder
    """
    for img in tqdm(os.listdir(base_folder)):
        width, height = Image.open(base_folder + "/" + img).size
        if max_w < width:
            max_w = width
        if max_h < height:
            max_h = height

        if min_w > width:
            min_w = width
        if min_h > height:
            min_h = height

        return max_w, max_h, min_w, min_h


def current_resolution(base_folder, src_folders):
    """
    Find the smallest and the largest width and height for images in multiple folders
    """
    max_w = max_h = 0
    min_w = min_h = 10000

    for src in src_folders:
        path = base_folder + "/" + src
        max_w, max_h, min_w, min_h = max_min_dim(max_w, max_h, min_w, min_h, path)

    print(f"Max dimensions: {(max_w, max_h)}")
    print(f"Min dimensions: {(min_w, min_h)}")

    return max_w, max_h, min_w, min_h


def above_pixels_threshold(base_folder, threshold):
    for img in tqdm(sorted(os.listdir(base_folder))):
        path = base_folder + "/" + img
        width, height = Image.open(path).size
        largest_dim = max(width, height)
        if largest_dim > threshold:
            print(f"{img} above threshold: {width, height}")


def padding(img, target_dim, color = 'w'):
    """
    Pad the image with white color to get a square
    """
    if img.mode != "RGB":
        img = img.convert("RGB")

    if color == 'w':
        col_code = (255, 255, 255)
    else:
        col_code = (0, 0, 0)

    padded = Image.new(img.mode, (target_dim, target_dim), color=col_code)
    
    width, height = img.size
    delta_w = (target_dim - width)//2
    delta_h = (target_dim - height)//2
    padded.paste(img, (delta_w, delta_h))

    return padded


def crop(img_file, flexible, src_folder, dest_folder, target_width, target_height):
    """
    Simply crop an image to the desired size
    """
    img = Image.open(src_folder + "/" + img_file)
    if flexible:
        width, height = img.size
        img = img_resize(img, max(width, height) - 256) # This constant value of 256 IS NOT OK

    width, height = img.size

    assert width > target_width and height > target_height, \
    f"Expected width and heigth {(width, height)} larger than the target dimension {(target_width, target_height)}"

    delta_w = (width - target_width) // 2
    delta_h = (height - target_height) // 2

    left_upper = (delta_w, delta_h)
    right_lower = (width - delta_w, height - delta_h)
    cropping_square = tuple([*left_upper, *right_lower])

    cropped_img = img.crop(cropping_square)
    cropped_img.convert("RGB").save(dest_folder + "/" + img_file)


def img_resize(img_file, target_dim, pad=False, color=None):
    """
    Resize and pad the given PIL image
    """
    img_file.thumbnail((target_dim, target_dim),Image.LANCZOS)

    if pad:
        img_file = padding(img_file, target_dim, color)

    return img_file
    

def resize(src_folder, dest_folder, target_dim, pad = False, color = 'w'):
    """
    Resize image reducing resolution (number of pixels) mantaining aspect
    """
    os.makedirs(dest_folder, exist_ok=True)
    for img_path in tqdm(sorted(os.listdir(src_folder))):
        src_path = src_folder + "/" +  img_path
        dest_path = dest_folder + "/" + img_path

        img_file = Image.open(src_path)
        img_file = img_resize(img_file, target_dim, pad, color)

        img_file.convert("RGB").save(dest_path, "PNG")


def video_grid():
    """
    Script to concatenate and display videos in a grid.
    Can also make video from image
    """
    # Arguments
    video_length = 19
    scale_size = 512

    # Transform images into video
    for i, img in enumerate(os.listdir("out/ffhq")):
        command = "ffmpeg -loop 1 -i out/ffhq" + f"/{img} " + f"-pix_fmt yuv420p -t {video_length} out/ffhq_video/ffhq{i}.mp4"
        os.system(command)

    # Rescale and concatenate videos in a grid
    command = 'ffmpeg '
    for i, video in enumerate(sorted(os.listdir('out/ffhq_video'))):
        if i < 5:
            command += '-i out/ffhq_video/' + f'ffhq{i}.mp4 '

    command += '-i test2.mp4 '
    x = f"scale={scale_size}:{scale_size}:"
    command += f'-filter_complex "[0:v]{x}[v0];[1:v]{x}[v1];[2:v]{x}[v2];[v0][v1][v2]hstack=inputs=3[row1];[3:v]{x}[v3];[4:v]{x}[v4];[5:v]{x}[v5];[v3][v4][v5]hstack=inputs=3[row2];[row1][row2]vstack=inputs=2[v]" -map "[v]" output.mp4'
    os.system(command)