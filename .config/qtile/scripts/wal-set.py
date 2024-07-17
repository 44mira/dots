#!/usr/bin/env python3

import subprocess, pathlib, json
import os

# Get directory for the wpg scheme
HOME = os.environ.get("HOME")
schemes_path = pathlib.Path(f"{HOME}/.config/wpg/schemes")
pictures_path = pathlib.Path(f"{HOME}/Pictures")


def set_wpg():
    # Clear wpg schemes and then set new wallpaper
    choice = subprocess.run(
        f"ls {str(pictures_path)} | rofi -dmenu",
        shell=True,
        capture_output=True,
        text=True,
    )
    wallppr_path = pictures_path / choice.stdout.strip()

    if not wallppr_path.exists():
        wallppr_path = pictures_path / "wallpaper.png"

    # Remove all pre-existing schemes
    for scheme in schemes_path.glob("*.json"):
        scheme.unlink()

    # Add the wallpaper to wpg
    subprocess.run(["wpg", "-a", str(wallppr_path)])

    # Set the wallpaper and generate the colorscheme.
    subprocess.run(["wpg", "-s", str(wallppr_path)])

    return wallppr_path


def get_colors():
    # Retrieve colorscheme json

    scheme_file = [*schemes_path.glob("*.json")][0]
    colorscheme = {}

    with open(scheme_file, "r") as f:
        colorscheme = json.load(f)

    return [color for color in colorscheme["colors"].values()]


def set_rofi(colors: list[str]):
    # Replace pywal-color in my_theme.rasi
    subprocess.run(
        f' sed -i "s|pywal-color:.*|pywal-color:                 {colors[12]};|" {HOME}/.config/rofi/themes/my_theme.rasi',
        shell=True,
    )


def set_dunst(colors: list[str]):
    # Replace normal background in dunstrc
    subprocess.run(
        f'sed -i "305 s/background =.*/background = \\"{colors[0]}\\"/" {HOME}/.config/dunst/dunstrc',
        shell=True,
        capture_output=True,
    )
    subprocess.run("killall -q dunst &", shell=True, capture_output=True)


def set_cava(colors: list[str]):
    # Replace gradient in cava config
    for i in range(8):
        search_expression = f"gradient_color_{i}"
        replace_expression = f"gradient_color_{i} = {colors[i]}"
        subprocess.run(
            f"sed -i s|^{search_expression}.*|{replace_expression}| {HOME}/.config/cava/config",
            shell=True,
            capture_output=True,
        )


def set_qtile_bar(colors: list[str]):
    # Replace current color array in qtile layouts
    for i in range(9, 25):
        subprocess.run(
            f'sed -i -E \'{i} s/".*"/"{colors[i-9]}"/\' {HOME}/.config/qtile/settings/layouts.py',
            shell=True,
            capture_output=True,
        )


def set_omp(colors: list[str]):
    subprocess.run(
        f'sed -i -E -e \'8 s/"#\\w*"/"{colors[4]}"/\' -e \'14 s/"#\\w*"/"{colors[7]}"/\' {HOME}/.thm.omp.json',
        shell=True,
        capture_output=True,
    )


def reload_qtile():
    subprocess.run(
        "qtile cmd-obj -o cmd -f reload_config", shell=True, capture_output=True
    )


def update_lockscreen(wallppr_path):
    notification = "dunstify -i 'icons8-info-48' -t 2000 "
    subprocess.run(
        notification + "Updating Betterlockscreen Cache",
        shell=True,
        capture_output=True,
    )
    subprocess.run(
        f"betterlockscreen -u {str(wallppr_path)}", shell=True, capture_output=True
    )
    subprocess.run(
        notification + "Betterlockscreen Cache Updated", shell=True, capture_output=True
    )


if __name__ == "__main__":
    wallppr_path = set_wpg()
    colors = get_colors()

    set_dunst(colors)
    set_rofi(colors)
    set_cava(colors)
    set_qtile_bar(colors)
    set_omp(colors)
    reload_qtile()
    update_lockscreen(wallppr_path)
