import os
import re
import shutil
import zipfile

try:
    import modules.helper as hp
except ImportError:
    import helper as hp


class Chapter:
    def __init__(self, series_name, chapter_number, volume_number):
        self.series_name = series_name
        self.chapter_number = chapter_number
        self.volume_number = volume_number
        self.files = []

    def __str__(self) -> str:
        string = f"Series:      {self.series_name}\n"
        string += f"Chapter:     {self.chapter_number}\n"
        string += f"Volume:      {self.volume_number}\n"
        string += f"Files:       {len(self.files)}\n"
        return string


def find_chapter_and_volume(file_name):
    # look for something like c001#1 in the file name
    ch_pattern = re.compile(r"c(\d+)(#\d+)")
    chapter = re.search(ch_pattern, file_name)
    # chapter becomes 001#1
    chapter = "" if chapter is None else f"{chapter.group(1)}{chapter.group(2)}"
    if chapter == "":
        # look for someting like c001 in the file name
        ch_pattern = re.compile(r"c(\d+)")
        chapter = re.search(ch_pattern, file_name)
        chapter = "" if chapter is None else chapter.group(1)
    
    vol_pattern = re.compile(r"v(\d+)")  # Matches both v(01) and v01
    volume = re.search(vol_pattern, file_name)
    volume = "" if volume is None else volume.group(1)

    # print(f"\n\nChapter: {chapter}, Volume: {volume}\n")

    return chapter, volume


def find_series_name(file_name):
    # if the file name is Cool Story - c001... then the series name is Cool Story
    series_name = re.sub(r" - c\d+.*", "", file_name)
    
    # if the chapter number wasn't found, try to find the volume number
    if series_name == file_name: 
        series_name = re.sub(r" v\d+.*", "", file_name)

    # if it still wasn't found, get everything before the first (
    if series_name == file_name: 
        # find everything before the first ( in the file name
        series_name = re.sub(r" \(.+", "", file_name)

    # print(f"\n\nSeries name: {series_name}\n")

    return series_name


def split_chapters(cbz_file):

    # NOTES:
    # - A volume file looks like: Cool Story - v01... .cbz
    # - A chapter file looks like: Cool Story - Chapter 001 (v01).cbz

    # get filename from path
    file_name = os.path.basename(cbz_file)
    print(f"Extracting {file_name}...", end="\r")

    series_name = find_series_name(file_name)

    hp.create_folders(f"chapters/{series_name}")
    
    # Extract the files into the temp directory
    with zipfile.ZipFile(cbz_file, "r") as zipf:
        zipf.extractall("temp")

    hp.clear_print(f"Extracted {file_name}.")

    # Get all the files in the temp directory
    files = os.listdir("temp")
    files.sort()

    # Group files by chapter
    chapters = []
    print("Checking for chapters...", end="\r")
    for file in files:
        chapter_number, volume_number = find_chapter_and_volume(file)
        
        # if there's not a chapter object for this chapter, create one
        found = False
        for chapter in chapters:
            if chapter.chapter_number == chapter_number:
                found = True
                break

        if not found:
            chapters.append(Chapter(series_name, chapter_number, volume_number))

        # add the file to the chapter object with the same chapter number
        for chapter in chapters:
            if chapter.chapter_number == chapter_number:
                chapter.files.append(file)

    # for chapter in chapters:
    #     print(chapter)

    hp.clear_print(f"{len(chapters)} chapters found.")

    # create a .cbz file for each chapter
    for chapter in chapters:
        hp.clear_print(f"Chapterizing {chapter.chapter_number}...", end="\r")

        # set the name of the zip file appropriately
        chapter_file_name = f"{series_name} - "
        chapter_file_name += f"Chapter {chapter.chapter_number} "
        chapter_file_name += f"(v{chapter.volume_number}).cbz"

        with zipfile.ZipFile(chapter_file_name, "w") as zipf:
            for file in chapter.files:
                # write the file into temp folder
                src = os.path.join("temp", file)
                dst = os.path.join("temp", file)

                # write the file into the root of the zip
                zipf.write(src, arcname=file)

        hp.clear_print(f"Moving {chapter_file_name}...", end="\r")
        src = chapter_file_name
        dst = os.path.join(f"chapters/{series_name}", chapter_file_name)

        os.replace(src, dst)

    # remove the temp directory
    shutil.rmtree("temp")
    hp.clear_print(f"Chapterized {file_name}.")
    

def main():
    hp.clear_screen()
    hp.set_title("Bane's Manga Tools // Split Volume Into Chapters\n")

    print("Enter \"r\" or \"q\" to return to the main menu at any time.\n")
      
    print("Enter the path to the CBZ file or folder full of CBZ files you want to split.")
    print("Example: /path/to/cool_story/cool_story_v01.cbz")
    print("Example: /path/to/cool_story")
    path = input("> ")
    path = hp.clean_path(path)

    if hp.check_for_return(path):       # if the user wants to return to the main menu
        return
    
    valid_ext = [".cbz", ".zip", "cbr"]
    ext = os.path.splitext(path)[1]
    # if the path is a cbz file, split it
    if ext in valid_ext:
        split_chapters(path)
    else:
        # if the path is a folder, split all the cbz files in it
        for file in os.listdir(path):
            ext = os.path.splitext(file)[1]
            if ext in valid_ext:
                split_chapters(os.path.join(path, file))

    
if __name__ == "__main__":
    main()