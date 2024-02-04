import os
import re
import zipfile

import modules.helper as hp


def zip_files_in_folder(path):
    # Get all .cbz files in the folder
    cbz_files = [f for f in os.listdir(path) if f.endswith(".cbz")]

    # get series name from folder name
    series_name = os.path.basename(path)

    # create cbv/series_name folder
    os.makedirs(f"cbv/{series_name}", exist_ok=True)
    # create temp folder
    os.makedirs("temp", exist_ok=True)

    # Group files by volume
    volumes = {}
    print("Checking for volumes...", end="\r")
    for file in cbz_files:
        # look for someting like (v01) in the file name
        vol_pattern = re.compile(r"\(v(\d+)\)")
        volume = re.search(vol_pattern, file)
        volume = "" if volume is None else volume.group(1)

        if volume not in volumes:
            volumes[volume] = []
        volumes[volume].append(file)
    hp.clear_print("Volumes found.", end="\r")

    # Zip files in each volume into the root of the zip
    for volume, files in volumes.items():
        # add a space before the volume number if it exists, for formatting
        string_volume = f" {volume}" if volume else ""

        print(f"Zipping volume{string_volume}...", end="\r")

        # set the name of the zip file appropriately
        file_name = f"{series_name} v{volume}.cbv" if volume else f"{series_name}.cbv"

        with zipfile.ZipFile(file_name, "w") as zipf:
            for file in files:
                # write the file into temp folder
                src = os.path.join(path, file)
                dst = os.path.join("temp", file)

                # write the file into the root of the zip
                zipf.write(src, arcname=file)
        hp.clear_print(f"Volume{string_volume}...", end="\r")

        print(f"Moving volume{string_volume}...", end="\r")
        src = file_name
        dst = os.path.join(f"cbv/{series_name}", file_name)

        os.replace(src, dst)
        hp.clear_print(f"Volume{string_volume}...", end="\r")

    # remove temp folder
    os.rmdir("temp")

    hp.clear_print("Done!")


def main():
    hp.clear_screen()
    hp.set_title("Bane's Manga Tools // Convert to CBV\n")

    print("Enter \"r\" or \"q\" to return to the main menu at any time.\n")

    print("Enter the path to the folder full of CBZ files you want to convert to CBV.")
    print("Example: /path/to/cool_story")
    path = input("> ")
    path = hp.clean_path(path)

    if hp.check_for_return(path):       # if the user wants to return to the main menu
        return

    zip_files_in_folder(path)


if __name__ == "__main__":
    os.system("cls")
    main()
