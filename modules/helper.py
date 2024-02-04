import os
import re
import shutil

# ==============================================================================

# VARIABLES

valid_exts = [".jpg", ".png", ".jpeg"]

# PATH FUNCTIONS

def clean_path(path):
    # remove " from path
    # remove "& " from path
    # remove ' and ' from path if it starts and ends with them
    # remove trailing slash
    path = re.sub('"', "", path)
    path = re.sub("& ", "", path)
    path = re.sub(r"^'(.*)'$", r"\1", path)
    path = re.sub(r"\\$", "", path)

    # replace '' with '
    path = re.sub(r"''", "'", path)

    return path


def has_folder_in_path(path):
    # Get the list of files and folders in the path
    dir_list = os.listdir(path)
    # Iterate over the list
    for dir in dir_list:
        # If the item is a directory
        if os.path.isdir(os.path.join(path, dir)):
            # Return True
            return True
    # If no directories were found, return False
    return False


def create_folders(folder_path):
    # remove the temp directory if it exists
    # create a folder for the series in the cbz folder
    # create a temp directory

    shutil.rmtree("temp", ignore_errors=True)
    os.makedirs(f"{folder_path}", exist_ok=True)
    os.makedirs("temp", exist_ok=True)

# MENU FUNCTIONS

def check_for_return(input):
    return_strings = ["r", "return", "main", "menu", "q", "quit"]
    return input.lower() in return_strings

# SYSTEM FUNCTIONS

def get_terminal_width():
    return shutil.get_terminal_size().columns

def clear_print(message, clear_size=150, end="\n"):
    print(" " * clear_size, end="\r")
    print(message, end=end)

def error(message):
    print(message)
    exit(1)

def set_title(title):
    os.system(f"TITLE {title}")

def exit(message=None):
    if message:
        print(message)
    quit()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")