import json
import os.path
import sys

import requests
from colorama import init, Fore
from jsonschema import validate, ValidationError

from lambentlight.schema import is_schema_valid


def main():
    """
    Checks that a JSON file matches the Schema.
    """
    # Initialize the console colors
    init()

    # If no parameters were specified, exit
    if len(sys.argv) < 2:
        print(f"{Fore.LIGHTRED_EX}You need to specify the file to check!")
        sys.exit(10)

    # Save the name of the file
    name = sys.argv[1]

    # If the schema does not exists, exit with code 6
    if not os.path.isfile(name):
        print(f"{Fore.LIGHTRED_EX}The file {Fore.WHITE}{name} {Fore.LIGHTRED_EX}does not exists!")
        sys.exit(11)

    # If the file exist, load it as JSON
    with open(name) as file:
        try:
            origin = json.load(file)
        except json.JSONDecodeError:
            print(f"{Fore.LIGHTRED_EX}The file {Fore.WHITE}{name} {Fore.LIGHTRED_EX}contains invalid JSON!")
            sys.exit(12)

    # If the file does not has a schema, exit
    if "$schema" not in origin:
        print(f"{Fore.LIGHTRED_EX}The file {Fore.WHITE}{name} {Fore.LIGHTRED_EX}doesnt have a schema!")
        sys.exit(13)

    # Request the schema
    req = requests.get(origin["$schema"])
    # Exit if we got an error code that is not 200
    if req.status_code != 200:
        print(f"{Fore.LIGHTRED_EX}Got code {Fore.WHITE}{req.status_code} {Fore.LIGHTRED_EX}while downloading Schema!")
        sys.exit(14)
    # Then, try to parse and exit if we fail
    try:
        schema = json.loads(req.text)
    except json.JSONDecodeError:
        print(f"{Fore.LIGHTRED_EX}The {Fore.WHITE}JSON Schema {Fore.LIGHTRED_EX}is not valid JSON!")
        sys.exit(15)

    # With the JSON parsed, validate the schema and exit if is not
    if not is_schema_valid(origin, schema, name):
        sys.exit(16)


if __name__ == '__main__':
    main()
