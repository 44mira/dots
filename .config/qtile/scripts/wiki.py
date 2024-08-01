#!/usr/bin/env python3

import pathlib
import subprocess

BOOKMARKS = {
    "Stardew Valley": "https://stardewvalleywiki.com/",
    "Dead Cells": "https://deadcells.wiki.gg/wiki/",
}

ICONS_PATH = pathlib.Path.home() / ".config/qtile/scripts/icons"
ICONS = {
    "Stardew Valley": "stardew.png",
    "Dead Cells": "deadcells.png",
}


def select_wiki() -> str:
    # get keys in dict
    wikis = "\n".join(
        rf"{wiki}\0icon\x1f{ICONS_PATH.absolute() / ICONS[wiki]}"
        for wiki in BOOKMARKS.keys()
    )

    # create rofi menu
    selected_wiki = subprocess.run(
        f"echo -en '{wikis}' | rofi -dmenu -p 'wiki' -show-icons",
        shell=True,
        capture_output=True,
        text=True,
    )

    selected_text = selected_wiki.stdout.strip()

    if selected_text not in BOOKMARKS.keys():
        subprocess.run(
            [
                "rofi",
                "-e",
                f"'{selected_text}' is not a valid bookmarked wiki.",
            ],
            capture_output=True,
        )
        return "ERROR!"

    return selected_text


def search_wiki(selected_wiki: str):
    # Create the search bar
    search_term = subprocess.run(
        rf"rofi -dmenu -p '{selected_wiki}' -theme-str 'listview {{lines: 0;}}'",
        shell=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    if search_term == "":
        subprocess.run(
            [
                "rofi",
                "-e",
                "Search term cannot be empty.",
            ],
            capture_output=True,
        )
        return

    # Run browser with the link
    subprocess.run(
        ["firefox", "--new-window", BOOKMARKS[selected_wiki] + search_term],
        capture_output=True,
    )


if __name__ == "__main__":
    selected_wiki = select_wiki()
    if selected_wiki == "ERROR!":
        exit(1)
    search_wiki(selected_wiki)
