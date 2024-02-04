# IMPORTS
import modules.rename as rename  # rename volume files
import modules.split  as split   # split volume into chapters
import modules.toCBZ  as toCBZ   # convert folder to CBZ
import modules.toCBV  as toCBV   # convert volumes to CBV

import modules.helper as hp      # helper functions

# FUNCTIONS
def print_options(options, columns=2, header=None, end="\n"):
    if not isinstance(options, dict):
        new_options = {}
        for option in options:
            new_options[option[0]] = option[1]
        options = new_options
                
    if header:
        print(header)

    # get the longest option
    longest = 0
    for option in options:
        if len(options[option]) > longest:
            longest = len(options[option])
    
    # automatically set column count
    if columns == -1:
        columns = hp.get_terminal_width() // (longest + 5)

    # print options
    for option in options:
        option_len = len(options[option])
        print(f"  {option}: {options[option]}{' ' * (longest - option_len)}", end="")
        if int(option) % columns == 0:
            print()

    print(end, end="")

def convert_options_into_choices(options):
    choices = []
    for option in options:
        new_choice = {option[0]: option[2]}
        choices.append(new_choice)

    return choices

def process_choice(choices, choice, fallback=None):
    # loop through the choices, and run the function if the choice is found
    for c in choices:
        if choice in c:
            c[choice]()
            return
        
    # if no choice is found, run fallback
    input("Invalid choice. Press enter to continue.")
    if fallback:
        fallback()

# MAIN
def main():
    options = [
        ["1", "Rename volume files",        rename.main],
        ["2", "Convert folder to CBZ",      toCBZ.main],
        ["3", "Split volume into chapters", split.main],
        ["4", "Convert volumes to CBV",     toCBV.main],
    ]

    exit_options = [
        ["q",    "Exit", lambda: hp.exit("Exiting...")],
        ["quit", "Exit", lambda: hp.exit("Exiting...")],
        ["exit", "Exit", lambda: hp.exit("Exiting...")],
    ]

    while True:
        hp.clear_screen()
        hp.set_title("Bane's Manga Tools // Main Menu")

        print_options(options, columns=-1, header="Options", end="\n")

        print("\nEnter the number of the option you want.")
        print("Enter 'q', 'quit', or 'exit' to quit.")
        choice = str(input("> ")).lower()

        choices = convert_options_into_choices(options + exit_options)
        process_choice(choices, choice)

if __name__ == "__main__":
    main()
