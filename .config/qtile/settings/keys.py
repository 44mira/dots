from libqtile.lazy import lazy
from libqtile.config import Key, Group, Drag, Click, ScratchPad, DropDown, Match
import pathlib

scripts = (pathlib.Path.home() / ".config/qtile/scripts").absolute()
mod = "mod4"
terminal = "kitty"

keys = [
    # [[ Base qtile commands ]] {{{
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "l", lazy.spawn("betterlockscreen -l"), desc="Lock screen"),
    # }}}
    # [[ Move focus ]] {{{
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # }}}
    # [[ Move windows ]] {{{
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"],
        "left",
        lazy.layout.shuffle_left(),
        desc="Move window to the left",
    ),
    Key(
        [mod, "shift"],
        "right",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    Key(
        [mod, "control", "shift"],
        "left",
        lazy.layout.swap_column_left(),
        desc="Swap window left",
    ),
    Key(
        [mod, "control", "shift"],
        "right",
        lazy.layout.swap_column_right(),
        desc="Swap window right",
    ),
    # }}}
    # [[ Grow windows ]] {{{
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod, "control"],
        "left",
        lazy.layout.grow_left(),
        desc="Grow window to the left",
    ),
    Key(
        [mod, "control"],
        "right",
        lazy.layout.grow_right(),
        desc="Grow window to the right",
    ),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # }}}
    # [[ Toggle layouts ]] {{{
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # }}}
    # [[ Window toggles ]] {{{
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod, "Shift"],
        "space",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    # }}}
    #  [[ Function sliders (volume and brightness) ]] {{{
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl s +5%"),
        desc="Increase brightness",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl s 5%-"),
        desc="Decrease brightness",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer -q set Master toggle"),
        desc="Toggle audio",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer -D default sset Master 1%+ unmute"),
        desc="Increase volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer -D default sset Master 1%- unmute"),
        desc="Decrease volume",
    ),
    # }}}
    # [[ Spawn commands ]] {{{
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "w", lazy.spawn("firefox"), desc="Launch firefox"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Launch flameshot"),
    Key(
        [mod, "shift"],
        "s",
        lazy.group["scratchpad"].dropdown_toggle("spotify"),
        desc="Launch spotify scratchpad",
    ),
    Key(
        [mod, "shift"],
        "d",
        lazy.group["scratchpad"].dropdown_toggle("discord"),
        desc="Launch spotify scratchpad",
    ),
    Key(
        [mod, "shift"],
        "Return",
        lazy.group["scratchpad"].dropdown_toggle("terminal"),
        desc="Launch terminal scratchpad",
    ),
    Key(
        [mod],
        "c",
        lazy.spawn(str(scripts / "colorpick")),
        desc="Grab a color from screen and put it in clipboard",
    ),
    # }}}
    # [[ Rofi menu commands ]] {{{
    Key(
        [mod],
        "d",
        lazy.spawn("rofi -show drun"),
        desc="Spawn a command using a prompt widget",
    ),
    Key(
        [mod, "shift"],
        "e",
        lazy.spawn(str(scripts / "power-menu")),
        desc="Launch powermenu",
    ),
    Key(
        [mod, "shift"],
        "w",
        lazy.spawn(str(scripts / "wiki.py")),
        desc="Launch wiki search",
    ),
    # }}}
]

# [[ Groups ]] {{
groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

CENTERED_SQUARE_DIMENSIONS = {"x": 0.1, "y": 0.08}

groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "cal",
                terminal + " --hold zsh -c cal",
                x=0.6785,
                width=0.13,
                height=0.22,
                opacity=1,
            ),
            DropDown(
                "spotify",
                "env LD_PRELOAD=/usr/lib/spotify-adblock.so spotify",
                match=Match(wm_class="Spotify"),
                height=0.8,
                width=0.8,
                opacity=1,
                **CENTERED_SQUARE_DIMENSIONS,
            ),
            DropDown(
                "discord",
                "vesktop",
                match=Match(wm_class="vesktop"),
                height=0.8,
                width=0.8,
                opacity=1,
                on_focus_lost_hide=False,
                **CENTERED_SQUARE_DIMENSIONS,
            ),
            DropDown(
                "terminal",
                terminal,
                height=0.8,
                width=0.8,
                opacity=1,
                **CENTERED_SQUARE_DIMENSIONS,
            ),
        ],
    )
)
# }}

# [[ Mouse binds ]] {{{
# Drag floating layouts
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]
# }}}
