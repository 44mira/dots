from libqtile.lazy import lazy
import libqtile.layout as layout
from libqtile.config import Match, Screen
from libqtile import bar, qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

colors = [
    "#020202",
    "#A6628B",
    "#D268A4",
    "#F875BC",
    "#FC77C1",
    "#C1A2B5",
    "#D9CCD6",
    "#ecdce5",
    "#a59aa0",
    "#A6628B",
    "#D268A4",
    "#F875BC",
    "#FC77C1",
    "#C1A2B5",
    "#D9CCD6",
    "#ecdce5",
]

# colors[0] : Background
# colors[7] : Foreground
# colors[4] : Primary
# colors[2] : Secondary
# colors[1] : Tertiary

# [[ Layouts ]] {{{
layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors[7],
    "border_normal": colors[0],
}

layouts = [
    # layout.xmonad.MonadTall(**layout_theme),
    layout.columns.Columns(
        **layout_theme,
        border_on_single=True,
        border_focus_stack=colors[7],
        grow_amount=5,
    ),
    layout.max.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.xmonad.MonadWide(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]
# }}}

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="steam", title="Friends List"),  # steam friendlist
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    **layout_theme,
)

widget_defaults = dict(
    font="CommitMono Nerd Font",
    fontsize=15,
    foreground=colors[7],
    padding=8,
)
extension_defaults = widget_defaults.copy()

screens = [
    # [[ Main monitor ]] {{{
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    "  ",
                    background=colors[4],
                    foreground=colors[0],
                    decorations=[PowerLineDecoration(path="back_slash")],
                ),
                widget.CurrentLayout(
                    background=colors[2],
                    foreground=colors[7],
                    padding=10,
                    decorations=[
                        PowerLineDecoration(path="back_slash"),
                    ],
                ),
                widget.WindowName(
                    background="#000000",
                    foreground=colors[7],
                    padding=10,
                ),
                widget.Spacer(
                    length=bar.STRETCH,
                    decorations=[
                        PowerLineDecoration(path="forward_slash"),
                    ],
                ),
                widget.GroupBox(
                    background=colors[4],
                    foreground=colors[7],
                    highlight_color=[colors[2], colors[1]],
                    this_current_screen_border=[colors[0]],
                    highlight_method="line",
                    decorations=[
                        PowerLineDecoration(path="back_slash"),
                    ],
                ),
                widget.Spacer(
                    length=bar.STRETCH,
                    decorations=[PowerLineDecoration(path="forward_slash")],
                ),
                # Only poll per day
                widget.CheckUpdates(
                    distro="Arch_yay",
                    no_update_string="Up to date",
                    update_interval=86400,
                    colour_have_updates=colors[7][1:],
                    colour_no_updates=colors[7][1:],
                ),
                widget.Sep(),
                widget.Clock(
                    format="%I:%M %p",
                    mouse_callbacks={
                        "Button1": lazy.group["scratchpad"].dropdown_toggle("cal")
                    },
                ),
                widget.Sep(),
                widget.Volume(
                    emoji=True,
                    emoji_list=["󰝟", "󰕿", "󰖀", "󰕾"],
                    padding=5,
                ),
                widget.Volume(mute_format="Muted", foreground=colors[7][1:]),
                widget.Sep(),
                widget.Memory(measure_mem="G", format="{MemUsed: .2f}GB"),
                widget.Sep(),
                widget.Battery(
                    show_short_text=False,
                    charge_char="󰂄",
                    full_char=" ",
                    discharge_char=" ",
                    format="{char} {percent:2.0%}",
                    notify_below=0.2,
                ),
                widget.Sep(),
                widget.Systray(),
                widget.TextBox(padding=2),
            ],
            24,
            border_width=[0, 0, 1, 0],
            border_color=colors[4],
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    # }}}
]
