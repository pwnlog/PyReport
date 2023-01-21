#!/usr/bin/python3

from argparse import RawTextHelpFormatter
import argparse
import re
import sys

def convert(new_filename, lines, image):
    for line in lines:
        line = line.strip()
        find = re.compile(r"^!\[(.*?)\]$", re.IGNORECASE)
        try:
            pattern = find.search(line).group()
            #print("[+] Old pattern: " + pattern)
            #print("[+] Extracting filename")
            #print("[+] Filename: " + pattern.strip("![[]]"))
            filename = pattern.strip("![[]]")
            title = filename.strip(".png")
            new_pattern = line.replace(pattern, f"![{title}]({image}{filename} " + f"'{title}'" + ")")
            print("[+] New pattern: " + new_pattern)
            new_filename.write(new_pattern + "\n")
        except AttributeError:
            new_filename.write(line + "\n")

def main():
    """
    Parse the arguments and decides the program flow
    This is also the help menu
    allow_abbrev=False; Disables abbreviations
    """

    parser = argparse.ArgumentParser(description=f"""

   ____  _         _     _ _             ___  _    _                   
  / __ \| |       (_)   | (_)           |__ \| |  | |                  
 | |  | | |__  ___ _  __| |_  __ _ _ __    ) | |__| |_   _  __ _  ___  
 | |  | | '_ \/ __| |/ _` | |/ _` | '_ \  / /|  __  | | | |/ _` |/ _ \ 
 | |__| | |_) \__ \ | (_| | | (_| | | | |/ /_| |  | | |_| | (_| | (_) |
  \____/|_.__/|___/_|\__,_|_|\__,_|_| |_|____|_|  |_|\__,_|\__, |\___/ 
                                                            __/ |      
                                                           |___/       

            Version: 0.0.1
            Author: pwnlog
            Twitter: @pwnlog
""", 
    formatter_class=RawTextHelpFormatter, add_help=False, allow_abbrev=False)
    
    # Main Options
    parser._optionals.title = "Main Options"
    parser.add_argument(
        "-f",
        "--file",
        metavar="<filename>",
        action="store",
        dest="input_file",
        type=str,
        required=True,
        help="Specify the file to convert"
    )
    parser.add_argument(
        "-i",
        "--image",
        metavar="<image>",
        action="store",
        dest="image",
        type=str,
        required=True,
        help="The path of the images directory"
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="<new file>",
        action="store",
        dest="new_file",
        type=str,
        required=True,
        help="The name of the new file that's created"
    )

    help_arg = parser.add_argument_group("Help Option")
    help_arg.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit"
    ) 

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()      

    filename = args.input_file
    new_file = args.new_file
    images = args.image

    # Verify input
    if len(filename) == 100:
        print("[-] The filename is too long")
        exit(1)

    if len(new_file) == 100:
        print("[-] The new filename is too long")
        exit(1)

    if images.endswith("/"):
        pass
    else:
        images = images + "/"

    # Start taking action
    obsidian_filename = open(filename, 'r', encoding="utf-8")
    lines = obsidian_filename.readlines()
    new_filename = open(new_file, 'w', encoding="utf-8")

    # Convert
    convert(new_filename, lines, images)

    # Close
    obsidian_filename.close()
    new_filename.close()

if __name__ == "__main__":
    main()