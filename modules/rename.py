import modules.chapters as chapters
import modules.pages as pages
import modules.reset as reset

import modules.helper as hp


def main():
    hp.clear_screen()
    hp.set_title("Bane's Manga Tools // Rename Volume Files\n")

    print("Enter \"r\" or \"q\" to return to the main menu at any time.\n")
      
    # THE PROCESS:
    # For the first volume of a series called Cool Story
    #                           Original --> Becomes
    # =========================================================================
    #                 cool_story_001.jpg --> 00001.jpg
    #                          00001.jpg --> Cool Story - cXXX (v01) - p001.jpg
    # Cool Story - cXXX (v01) - p001.jpg --> Cool Story - c001 (v01) - p001.jpg


    manual_chapter_mode = False

    # INPUTS:

    # get path to volume
    print("Enter the path to the volume you want to rename.")
    print("Example: /path/to/cool_story/cool_story_v01")
    volume_path = input("> ")
    volume_path = hp.clean_path(volume_path)
    if not volume_path:
        hp.error("Invalid path")

    if hp.check_for_return(volume_path):       # if the user wants to return to the main menu
        return

    # get series name
    print("Enter the name of the series.")
    print("Example: Cool Story")
    series_name = input("> ")
    if not series_name:
        hp.error("Invalid series name")

    if hp.check_for_return(series_name):       # if the user wants to return to the main menu
        return

    # get volume number
    print("Enter the volume number.")
    print("Example: 1")
    volume_number = input("> ")
    if not volume_number:
        hp.error("Invalid volume number")

    if hp.check_for_return(volume_number):       # if the user wants to return to the main menu
        return

    # load chapters file
    chapter_list = chapters.load_chapters_file()
    if len(chapter_list) == 0 and not manual_chapter_mode:
        hp.error("Invalid chapter file")

    print("What page number does the first page of the volume start on?")
    print("Example: 1")
    start_page = input("> ") or 0
    if start_page.isdigit():
        start_page = int(start_page)
    else:
        hp.error("Invalid start page number")
    
    # chapters.show_chapter_list(chapter_list)

    # ACTIONS:
        
    # resets filenames to a standard numbered format
    reset.rename_files(volume_path)
    
    # renames the files to the SERIES - cXXX (vYY) - pZZZ format
    pages.rename_files(volume_path, series=series_name, volume=volume_number, start=start_page)
    
    # replaces cXXX with the chapter number (eg cXXX to c001) from the chapters file
    chapters.rename_files(volume_path, chapter_list)


if __name__ == "__main__":
    main()