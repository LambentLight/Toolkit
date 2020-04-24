import json
import re
import sys

import lxml.html
import requests

from colorama import init, Fore

REGEX = "\\.\\/([0-9]{3,4}-[0-9a-z]{40})\\/(server\\.zip|fx\\.tar\\.xz)"  # https://regexr.com/4nl34
SCHEMA = "https://raw.githubusercontent.com/LambentLight/Schemas/master/builds.json"
DOWNLOAD = "https://runtime.fivem.net/artifacts/fivem/build_server_windows/master/{0}/server.zip"


def parse(text: str):
    """
    Parses the builds onto a LambentLight compatible format.
    """
    # Load the HTML and get the <a> nodes
    html = lxml.html.fromstring(text)
    a_nodes = html.xpath("//a[contains(@class, 'panel-block')]")

    # Create a temporary place to store the builds that we find
    builds = []

    # Iterate over the nodes
    for node in a_nodes:
        # Try to find the identifier on the link
        regex = re.search(REGEX, node.attrib.get("href", ""))
        # If it was found, add it onto the list
        if regex and regex.group(1):
            group = regex.group(1)
            print(f"{Fore.GREEN}Found Build {Fore.WHITE}{group}{Fore.GREEN}!")
            item = {
                "name": group,
                "download": DOWNLOAD.format(group),
                "target": 0
            }
            builds.append(item)

    # Finally, return all of the builds
    return builds


def main():
    """
    Generates an up to date list of Builds from the CitizenFX Website.
    """
    # Initialize the console colors
    init()

    # Request the contents of the page
    req = requests.get("https://runtime.fivem.net/artifacts/fivem/build_server_windows/master/")
    # Exit if we didn't got a 200 OK
    if req.status_code != 200:
        print(f"{Fore.LIGHTRED_EX}Got code {Fore.WHITE}{req.status_code} {Fore.LIGHTRED_EX}while updating Builds!")
        sys.exit(20)

    # Get the individual builds from the HTML
    builds = parse(req.text)
    print(f"{Fore.LIGHTBLUE_EX}Got {Fore.WHITE}{len(builds)}{Fore.LIGHTBLUE_EX} Builds!")
    # And save them onto the builds.json file
    with open("builds.json", "w") as file:
        out = {
            "$schema": SCHEMA,
            "builds": builds
        }
        json.dump(out, file, indent=4)
        file.write("\n")


if __name__ == '__main__':
    main()
