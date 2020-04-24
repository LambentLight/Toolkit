from colorama import Fore
from jsonschema import validate, ValidationError


def is_schema_valid(origin, schema, name):
    """
    Checks the schema against the dictionary.
    """
    try:
        validate(origin, schema)
    except ValidationError as e:
        path = " > ".join(str(x) for x in e.path)
        print(f"{Fore.CYAN}The File {Fore.WHITE}{name} {Fore.CYAN}does not complies with "
              f"the {Fore.WHITE}JSON Schema{Fore.CYAN}:")
        print(f"\t{Fore.WHITE}{e.message} on {path}")
        return False
    else:
        print(f"{Fore.LIGHTGREEN_EX}The File {Fore.WHITE}{name} {Fore.LIGHTGREEN_EX}complies with the Schema!")
        return True
