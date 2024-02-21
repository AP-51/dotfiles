# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pwd
import subprocess

from typing import List  # noqa: F401
from colors import pallete

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

uname = get_username()

# pywal
#colors = []
#cache='/home/{}/.cache/wal/colors'.format(uname)
#def load_colors(cache):
    #with open(cache, 'r') as file:
        #for i in range(8):
            #colors.append(file.readline().strip())
    #colors.append('#ffffff')
    #lazy.reload()
#load_colors(cache)

foreground = pallete["color_midtone"]
background = pallete["color_dark"]
#foreground="#3aa5b4"
#background="#11192c"

mod = "mod4"
alt = "mod1"
terminal = "kitty"
app_launcher="rofi -show drun -disable-history -show-icons"
win_launcher="rofi -show window -show-icons"
file_manager="pcmanfm"
screenshot="flameshot full"
screenshot_gui="flameshot gui"
lock ="betterlockscreen -l"
browser="firefox"

keys = [
    #programs
    Key([mod], "z", lazy.spawn(browser), desc="launches browser"), 
    Key([mod], "r", lazy.spawn("kitty -e ranger_pw"), desc="launches ranger"), 
    Key([mod, alt], "l", lazy.spawn(lock), desc="locks screen"), 
    Key([mod, "shift"], "s", lazy.spawn(screenshot_gui), desc="launches flameshot_gui"),
    Key([], "Print", lazy.spawn(screenshot), desc="takes full screenshot"),
    Key([mod], "x", lazy.spawn(file_manager), desc="launches file manager"), 
    #volume keys
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 5- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 5+ unmute")),
    #screenshot
    #Key([], "Print", lazy.spawn('scrot ss/telatiro-"$%y%m%d-%H%M-%S.png"')),
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
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
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn(app_launcher), desc="Spawn a command using a prompt widget"),
    Key([mod], "f",lazy.window.toggle_fullscreen(),desc="toggle full screen"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
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
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(margin=5, border_width=2, border_focus=pallete["color_gray"], border_normal=background),
    #layout.Floating(border_width=2, border_focus=colors[1], border_normal=colors[0]),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="AnonymicePro Nerd Font Bold",
    fontsize=16,
    padding=3,
    foreground=pallete["color_extra2"],
    #background=pallete["color_dark"]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayoutIcon(custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")]),
                #widget.CurrentLayout(),
                widget.Prompt( cursor_color=foreground),
                widget.GroupBox(
                    rounded=False, 
                    center_aligned=False,
                    hide_unused=True,
                    inactive=pallete["color_light"], 
                    active=pallete["color_extra2"],
                    highlight_method="line",
                    linesize=1,
                    urgent_border=pallete["color_light"],
                    this_current_screen_border=pallete["color_extra2"],
                    this_screen_border="#504945",
                    foreground=pallete["color_extra2"],
                    background=pallete["color_dark"],
                    fontsize=15,
                    font="AnonymicePro Nerd Font Bold",
                    ),
                widget.WindowName(max_chars=120, format='{name}',foreground=pallete["color_light"]),
                #widget.TextBox(text=" "),
                #widget.CryptoTicker(crypto='BTC', format='{crypto}:{amount:.2f} '),
                #widget.CryptoTicker(crypto='ETH', format='{crypto}:{amount:.2f}'),
                #widget.TextBox(text=" "),
                #widget.TextBox(text=""),
                #widget.TextBox(text=" "),
                #widget.Battery(format='{char} {percent:2.0%} ETA {hour:d}:{min:02d}', low_foreground=colors[1], charge_char='', discharge_char='', full_char='f',show_short_text=False),
                widget.Battery(charge_char=' ', discharge_char=' ', full_char=' ', format='{char} {percent:2.0%}', low_foreground=pallete["color_light"], show_short_text=False),
                widget.TextBox(text=" "),
                #widget.TextBox(text=" "),
                #widget.Backlight(),
                #widget.TextBox(text=" "),
                #widget.TextBox(text=" "),
                widget.TextBox(text=" "),
                widget.Volume(),
                widget.TextBox(text=" "),
                #widget.TextBox(text=" "),
                #widget.Wlan(interface="wlp3s0"),
                #widget.TextBox(text=" "),
                widget.Clock(format="%H:%M:%S %d/%m/%Y", foreground=pallete["color_extra2"]),
            ],
            30,
            fontsize=18,
            background=pallete["color_dark"]
            ,
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
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(border_width=2, border_focus=foreground, border_normal=background,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="rofi"),
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

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
