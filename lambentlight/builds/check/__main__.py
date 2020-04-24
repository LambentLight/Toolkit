import json
import os.path
import sys

from colorama import init, Fore
from jsonschema import validate, ValidationError


def main():
    """
    Checks that the Builds match the JSON Schema.
    """
    # Initialize the console colors
    init()

    # If the builds do not exist, exit with code 5
    if not os.path.isfile("builds.json"):
        print(f"{Fore.LIGHTRED_EX}The file {Fore.WHITE}builds.json {Fore.LIGHTRED_EX}does not exists!")
        sys.exit(5)

    # If the schema does not exists, exit with code 6
    if not os.path.isfile("schema.json"):
        print(f"{Fore.LIGHTRED_EX}The {Fore.WHITE}JSON Schema {Fore.LIGHTRED_EX}does not exists!")
        sys.exit(6)

    # If both files exist, load them up as JSON
    with open("builds.json") as file:
        try:
            builds = json.load(file)
        except json.JSONDecodeError:
            print(f"{Fore.MAGENTA}The file {Fore.WHITE}builds.json {Fore.MAGENTA}contains invalid JSON!")
            sys.exit(7)
    with open("schema.json") as file:
        try:
            schema = json.load(file)
        except json.JSONDecodeError:
            print(f"{Fore.MAGENTA}The {Fore.WHITE}JSON Schema {Fore.MAGENTA}contains invalid JSON!")
            sys.exit(8)

    # With the JSON parsed, validate the schema
    try:
        validate(builds, schema)
    except ValidationError as e:
        path = " > ".join(str(x) for x in e.path)
        print(f"{Fore.CYAN}The {Fore.WHITE}Builds File {Fore.CYAN}does not complies with "
              f"the {Fore.WHITE}JSON Schema{Fore.CYAN}:")
        print(f"\t{Fore.WHITE}{e.message} on {path}")
        sys.exit(9)


if __name__ == '__main__':
    main()
