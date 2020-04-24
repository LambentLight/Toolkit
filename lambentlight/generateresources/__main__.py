import glob
import json
import os.path
import sys

import requests
from colorama import init, Fore

from lambentlight.schema import is_schema_valid

SCHEMA_EXTENDED = "https://raw.githubusercontent.com/LambentLight/Schemas/master/resource_extended.json"
SCHEMA_BASIC = "https://raw.githubusercontent.com/LambentLight/Schemas/master/resource_basics.json"


def main():
    """
    Generates a list of Resources.
    """
    # Initialize the console colors
    init()

    # If there is no directory called resources, exit
    if not os.path.isdir("resources"):
        print(f"{Fore.LIGHTRED_EX}The folder {Fore.WHITE}resources {Fore.LIGHTRED_EX}does not exists!")
        sys.exit(30)

    # Request the schema and exit if we failed
    req = requests.get(SCHEMA_EXTENDED)
    if req.status_code != 200:
        print(f"{Fore.LIGHTRED_EX}Got code {Fore.WHITE}{req.status_code} {Fore.LIGHTRED_EX}while downloading Schema!")
        sys.exit(31)
    schema = req.json()

    # Create a place to store the basic information
    resources = []

    # Iterate over the files in the resources folder
    for filename in glob.iglob("resources\\*.json"):
        # Get the contents of the file as JSON
        with open(filename) as file:
            try:
                info = json.load(file)
            except json.JSONDecodeError:
                print(f"{Fore.LIGHTRED_EX}The file {Fore.WHITE}{filename} {Fore.LIGHTRED_EX}contains invalid JSON!")
                sys.exit(32)

        # Make sure that we have a valid schema
        if not is_schema_valid(info, schema, filename):
            sys.exit(33)

        # And add a simpler version of it to the list
        resources.append({
            "name": info["name"],
            "author": info["author"],
            "target": info["target"]
        })
        print(f"{Fore.LIGHTBLUE_EX}Finished parsing {Fore.WHITE}{info['name']}{Fore.LIGHTBLUE_EX}!")

    # Finally, write the list into the disk
    with open("resources.json", "w") as file:
        json.dump({"$schema": SCHEMA_BASIC, "resources": resources}, file, indent=4)
        file.write("\n")


if __name__ == '__main__':
    main()
