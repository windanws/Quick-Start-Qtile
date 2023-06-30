# lang: UTF-8
#
# ███╗░░░███╗██╗██╗░░░██╗██╗░░░██╗
# ████╗░████║██║╚██╗░██╔╝██║░░░██║
# ██╔████╔██║██║░╚████╔╝░██║░░░██║
# ██║╚██╔╝██║██║░░╚██╔╝░░██║░░░██║
# ██║░╚═╝░██║██║░░░██║░░░╚██████╔╝
# ╚═╝░░░░░╚═╝╚═╝░░░╚═╝░░░░╚═════╝░
#
# ~Qtile Config~

import os
import re
import socket
import subprocess
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List

from qtile_extras import widget
# from qtile_extras.widget.decorations import PowerLineDecoration

mod = "mod4"
terminal = "alacritty"

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod,], "l", lazy.spawn("i3lock"), desc="Screenlock Qtile"),
    Key([mod], "r", lazy.spawn("rofi -combi-modi window, drun, ssh -font 'Jetbrains Mono 12' -show drun")),

    # Control Volume
    Key([], "XF86AudioMute", lazy.spawn("amixer -q sset Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.widget["volume"].decrease_vol()),
    Key([], "XF86AudioRaiseVolume", lazy.widget["volume"].increase_vol()),

    # Brightness Controls
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 10")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 10")),


]

groups = [
    Group('1',label='Dev'),
    Group('2',label='Web'),
    Group('3',label='Term'),
    Group('4',label='File'),
    Group('5',label='Disc'),
    Group('6',label='Note'),
    Group('7',label='PDF'),
    Group('8',label='Music'),
    Group('9',label='Doc'),
    ]


for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )


layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "#FFD95A",
                "border_normal": "#4C3D3D"
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
]


colors = [["#282c34", "#282c34"], # [0]
          ["#1c1f24", "#1c1f24"], # [1]
          ["#dfdfdf", "#dfdfdf"], # [2]
          ["#FFF7D4", "#FFF7D4"], # [3]
          ["#ff6c6b", "#ff6c6b"], # [4] Error Colour
          ["#98be65", "#98be65"], # [5] Correct Colour
          ["#FFD953", "#FFD953"], # [6] Main Colour
          ["#4C3D3D", "#4C3D3D"], # [7] Secondary Colour
          ["#A75D5D", "#A75D5D"], # [8]
          ["#D3756B", "#D3756B"]] # [9]
          

widget_defaults = dict(
    font="JetBrains Mono Bold",
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

'''
Arrow Directions
powerline = {
    "decorations": [
            PowerLineDecoration()   
        ]
     }
'''


screens = [
    Screen(
        wallpaper='~/Picture/ubuntu.jpg',
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                    scale = 0.5,
                    padding = 0,
                    ),
                widget.GroupBox(
                    active = colors[2],
                    inactive = colors[0],
                    highlight_color = colors[7],
                    highlight_method = "line",
                    this_current_screen_border = colors[6],
                    foreground = colors[2],
                    ),
                widget.Prompt(),
                widget.WindowName(
                    font = "JetBrains Mono",
                    fontsize = 11,
                    ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Sep(
                    linewidth=1,
                    padding=10,
                    ),
                widget.Volume(
                    fmt = "  {}"
                    ),
                widget.Sep(
                    linewidth=1,
                    padding=10,
                    ),
                widget.Backlight(
                    fmt = " {}", 
                    backlight_name ="amdgpu_bl0",
                    update_interval = 0.3,
                    ),
                widget.TextBox(
                    font="FontAwesome",
                    text="   ",
                    padding = 0, 
                    mouse_callbacks = {'Button1': lazy.spawn('alacritty --hold -e acpi')},
                    ),
                widget.Battery(
                    format = "{percent:2.0%}",
                    low_percentage = 0.1,
                    update_interval = 60,
                    mouse_callbacks = {"Button1": lazy.spawn('alacritty --hold -e acpi')},
                    **widget_defaults,
                    ),
                widget.Sep(
                    linewidth=1,
                    padding=10,
                    ),
                widget.Systray(padding = 1),
                widget.Sep(
                    linewidth=1,
                    padding=10,
                    ),

                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.Sep(
                    linewidth=1,
                    padding=10,
                        ),
                widget.Wlan(
                    format = "{essid}",
                    mouse_callbacks = {"Button1": lazy.spawn("alacritty --hold -e cat .config/qtile/Guides/networkGuide.md")},
                        ),
                widget.Sep(
                    linewidth = 0, 
                    padding = 6,
                    foreground=colors[1],

                        ),
            ],
            32,
            background = colors[1],
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

wmname = "LG3D"
