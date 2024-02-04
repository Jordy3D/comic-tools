import os

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

# go through all the files in the directory and name them from 00000.jpg and up
def rename_files(path):
    images = load_all_images(path)

    # rename the files
    for i in range(len(images)):
        # get the file extension
        extension = os.path.splitext(images[i])[1]
        # rename the file
        os.rename(os.path.join(path, images[i]), os.path.join(path, str(i).zfill(5) + extension))

    print("Done!")


if __name__ == "__main__":
    # get path to volume
    volume_path = input("Volume path: ")

    rename_files(volume_path)