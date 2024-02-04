import os
import re

class Chapter:
    def __init__(self, number, page):
        self.number = number
        self.page = page

def load_chapters_file(path="chapters.csv"):
    """Load chapters.csv to know where the split the chapters and return a list of Chapter objects.\n
    Format: chapter number, page number
    (eg 003,057)
    Default path: chapters.csv"""
    chapters = []

    try:
        with open(path, "r") as file:
            for line in file:
                # if line is empty or just a newline, skip it
                if not line or line == "\n":
                    continue

                line = line.rstrip("\n")
                # split the line into a list
                line = line.split(",")
                
                chap = Chapter(line[0], line[1])
                chapters.append(chap)
    except FileNotFoundError:
        print(f"File not found: {path}")

    return chapters

def show_chapter_list(chapters):
    for chapter in chapters:
        print(f"Chapter: {chapter.number + '  ' if not '#' in chapter.number else chapter.number}  |  Page: {chapter.page}")

def rename_files(volume_path, chapters):
    # loop through the pages
    for file in os.listdir(volume_path):
        if file.endswith(".jpg"):
            # get the page number, which is the 3 digits after - p
            page_number = re.search(r"- p(\d{3})", file).group(1)
            # convert page number to int
            page_number = int(page_number)

            # loop through the chapters
            for i in range(len(chapters)):
                check_chapter = chapters[i].number
                check_chapter_page = int(chapters[i].page)

                # if page is higher than or equal to the chapter page, it's a new chapter
                if page_number >= check_chapter_page:
                    chapter = check_chapter

            chapter = str(chapter).zfill(3)

            old = file
            if not re.search(r"\d{3}-\d{3}", file):     # if the file is not a double page
                old = old + "    "                      # add padding for formatting display
            new = file.replace(f"cXXX", f"c{chapter}")

            print(f"Old: {old}  |  New: {new}")

            # rename the page, replacing cXXX with the chapter number (eg cXXX to c001)
            os.rename(os.path.join(volume_path, file), os.path.join(volume_path, file.replace(f"cXXX", f"c{chapter}")))


if __name__ == "__main__":
    chapters = load_chapters_file("chapters.csv")

    print("Chapters:")
    for chap in chapters:
        print(f"Chapter: {chap.number}  |  Page: {chap.page}")
    print()

    # get path to volume
    volume_path = "test/baa"

    rename_files(volume_path, chapters)