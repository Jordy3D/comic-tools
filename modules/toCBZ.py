import os
import re
import zipfile

import modules.helper as hp

class Volume:
    # contains the path, series name, volume number, and year of a volume
    def __init__(self, path):
        self.path = path
        self.base_name = self.prep_name()
        self.series_name = self.get_series_name()
        self.volume_number = self.get_volume_number()
        self.year = self.get_year()
        self.output_name = self.create_output_name()

    def prep_name(self):
        temp = self.path
        temp = os.path.basename(temp)
        temp = re.sub(r"Vol\. ", "v", temp)
        temp = re.sub(r"Volume ", "v", temp)
        temp = re.sub(r" - v(\d+)", " v\\1", temp)

        return temp

    def get_series_name(self):
        temp = re.search(r"(.+?) v\d+", self.base_name)
        temp = temp.group(1) if temp else self.base_name

        if temp == self.base_name:
            temp = self.base_name.split(" - ")[0]

        return temp
    
    def get_volume_number(self):
        temp = re.search(r"v(\d+)", self.base_name)
        temp = temp.group(1) if temp else ""

        if temp == "":
            temp = re.search(r"Volume (\d+)", self.base_name)
            temp = temp.group(1) if temp else ""

        return temp

    def get_year(self):
        temp = re.search(r"\((\d{4})\)", self.base_name)
        temp = temp.group(1) if temp else ""

        return temp
    
    def create_output_name(self):
        temp = f"{self.series_name}"
        if self.volume_number:
            temp += f" v{self.volume_number}"
        if self.year:
            temp += f" ({self.year})"
        
        return temp

def zip_to_cbz(vol_path):
    
    vol = Volume(vol_path)
    
    hp.create_folders(f"volumes/{vol.series_name}")
    
    # Create a CBZ file with the same name as the directory
    output_path = f"volumes/{vol.series_name}/{vol.output_name}.cbz"
    with zipfile.ZipFile(f"{output_path}", "w") as cbz_file:
        file_count = len(os.listdir(vol_path))

        # Iterate over all the files in the directory
        for i, file_name in enumerate(os.listdir(vol_path)):
            # Add each file to the CBZ file
            cbz_file.write(f"{vol_path}/{file_name}", arcname=file_name)

            message = f"Zipping {vol.output_name} to CBZ... {i+1}/{file_count}"
            message += f" ({round((i+1)/file_count*100, 2)}%)"

            print(message, end="\r")

    hp.clear_print(f"Zipped {vol.output_name} to CBZ!")

def main():
    hp.clear_screen()
    hp.set_title("Bane's Manga Tools // Convert to CBZ\n")

    print("Enter \"r\" or \"q\" to return to the main menu at any time.\n")

    print("Enter the path to the directory you want to convert to CBZ.")
    print("Example: /path/to/cool_story/cool_story_v01")
    path = input("> ")
    path = hp.clean_path(path)

    if hp.check_for_return(path):       # if the user wants to return to the main menu
        return

    dir_list = os.listdir(path)
    is_root_dir = hp.has_folder_in_path(path)

    # if the directory contains only files
    if len(dir_list) > 0 and not is_root_dir:
        zip_to_cbz(path)
    else:
        for dir in dir_list:
            if not os.path.isdir(os.path.join(path, dir)):
                continue
            zip_to_cbz(os.path.join(path, dir))
            
if __name__ == "__main__":
    main()