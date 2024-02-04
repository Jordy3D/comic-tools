import os
import re
from PIL import Image

try:
    import helper as hp
except ImportError:
    import modules.helper as hp

def load_all_images(path):
    files = os.listdir(path)
    images = []
    for file in files:
        ext = os.path.splitext(file)[1]
        if ext in hp.valid_exts:
            images.append(file)
    return images

def get_dimensions(path, image):
    # get the width of the image in pixels
    check_image = Image.open(f"{path}/{image}")
    width, height = check_image.size
    return width, height

def generate_name(pattern="<SERIES> - cXXX (v<VOLUME>) - p<PAGE>", series="", volume="", page=""):
    series = str(series)
    volume = str(volume).zfill(2)
    page = str(page).zfill(3)

    # print(f"Generating name:    {pattern}")
    print(f"Series:             {series}")
    print(f"Volume:             {volume}")
    print(f"Page:               {page}")

    pattern = re.sub(r"<SERIES>", series, pattern)
    pattern = re.sub(r"<VOLUME>", volume, pattern)
    pattern = re.sub(r"<PAGE>", page, pattern)
    
    return pattern


def rename_file(path, name):
    os.rename(path, name)

def rename_files(path, pattern="<SERIES> - cXXX (v<VOLUME>) - p<PAGE>", series="", volume="", start=0):
    images = load_all_images(path)

    # get the width of the first image
    base_width, base_height = get_dimensions(path, images[1])
        
    page_number = start
    for image in images:
        # get the width of the image in pixels
        width, height = get_dimensions(path, image)
        
        # if the width of the image is higher than the base width, it's a double page
        if width > base_width:
            page_string = str(page_number).zfill(3)
            page_string += "-"
            page_string += str(page_number+1).zfill(3)

            # rename the file
            new_name = generate_name(pattern, series, volume, f"{page_string}")
            new_path = f"{path}/{new_name}.jpg"
            old_path = f"{path}/{image}"
            rename_file(old_path, new_path)
            page_number += 2
        else:
            # rename the file
            new_name = generate_name(pattern, series, volume, page_number)

            print(f"Renaming {image} to {new_name}.jpg")

            new_path = f"{path}/{new_name}.jpg"
            old_path = f"{path}/{image}"

            rename_file(old_path, new_path)
            page_number += 1



if __name__ == "__main__":
    path = input("Path: ")
    series = input("Series name: ")
    volume = input("Volume number: ")

    rename_files(path, series=series, volume=volume, start=1)
