#!/usr/bin/env python3

import pathlib
import subprocess
from dataclasses import dataclass
from typing import Literal

# The configuration CSV is found in ~/.config/qtile/scripts/wiki_links.csv


@dataclass(slots=True)
class Game:
    name: str
    link: str
    icon: str

    def __str__(self) -> str:
        return self.name


SCRIPTS_PATH = pathlib.Path.home() / ".config/qtile/scripts"
ICONS_PATH = SCRIPTS_PATH / "icons"


def select_wiki(games: list[Game]) -> Game | Literal["ERROR!"]:
    game_hashmap = {game.name: index for index, game in enumerate(games)}

    # add icons to the displayed wiki names
    wikis = "\n".join(
        rf"{game}\0icon\x1f{ICONS_PATH.absolute() / game.icon}" for game in games
    )

    # create rofi menu
    selected_wiki = subprocess.run(
        f"echo -en '{wikis}' | rofi -dmenu -i -p 'wiki' -show-icons",
        shell=True,
        capture_output=True,
        text=True,
    )

    selected_text = selected_wiki.stdout.strip()

    if selected_text not in [game.name for game in games]:
        subprocess.run(
            [
                "rofi",
                "-e",
                f"'{selected_text}' is not a valid bookmarked wiki.",
            ],
            capture_output=True,
        )
        return "ERROR!"

    return games[game_hashmap[selected_text]]


def search_wiki(selected_wiki: Game):
    # Create the search bar
    search_term = subprocess.run(
        f"rofi -dmenu -p '{selected_wiki}' -theme-str 'listview {{lines: 0;}}'",
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
        ["firefox", "--new-tab", selected_wiki.link + search_term],
        capture_output=True,
    )


if __name__ == "__main__":
    # Parse the CSV into the dictionaries
    games = []
    with open(SCRIPTS_PATH / "wiki_links.csv", "r") as f:
        for line in f:
            values = line.strip().split(",")
            games.append(Game(*(value for value in values)))

    selected_wiki = select_wiki(games)
    if selected_wiki == "ERROR!":
        exit(1)
    search_wiki(selected_wiki)
