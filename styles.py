from evdev import ecodes
from pathlib import Path
from time import sleep
import os
from Xlib import X

from clipboard import copy, get
from constants import KEYSYM_MAP, TARGET, NORMAL
from press import press
from rofi import rofi
import normal

from mode import mode

pressed = []

script_path = Path(os.path.realpath(__file__)).parents[0]

data_dirs = {
    'style': script_path / 'data' / 'styles',
    'object': script_path / 'data' / 'objects',
}


def check(what, manager, name):
    files = list(data_dirs[what].iterdir())
    names = [f.stem for f in files]

    filtered = list(i for i, n in enumerate(names) if n.startswith(name))
    # print(name,', '.join(n for n in names if n.startswith(name)))

    if len(filtered) == 0:
        pressed.clear()
        return back_to_normal(manager)

    if len(filtered) == 1:
        index = filtered[0]
        copy(files[index].read_text(), target=TARGET)
        if what == 'style':
            press(ecodes.KEY_V, [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT])
        else:
            press(ecodes.KEY_V, [ecodes.KEY_LEFTCTRL])

        sleep(0.5) # Give the user some time when an object is added.
        return back_to_normal(manager)


def back_to_normal(manager):
    mode(NORMAL)
    pressed.clear()
    manager.teardown()
    manager.listen(normal.normal_mode)


def paste_mode(what, event, keysym, manager):
    if event.state & X.ControlMask:
        # there are modifiers
        # eg. X.ControlMask
        # ~or X.ShiftMask~
        return

    if keysym in KEYSYM_MAP:
        character = KEYSYM_MAP.get(keysym, 0)

        if event.type == X.KeyPress:
            if character == 'ESC':
                if len(pressed) == 0:
                    return back_to_normal(manager)
                else:
                    pressed.clear()
            else:
                pressed.append(character)
                return check(what, manager, ''.join(pressed))

        elif event.type == X.KeyRelease:
            pass

def save_mode(what):
    sleep(0.1)
    press(ecodes.KEY_C, [ecodes.KEY_LEFTCTRL])
    sleep(0.1)
    svg = get(TARGET)
    if not 'svg' in svg:
        return

    directory  = data_dirs[what]
    files = list(directory.iterdir())
    names = [f.stem for f in files]
    key, index, name = rofi(
        'Save as',
        names,
        ['-theme', '~/.config/rofi/ribbon.rasi'],
        fuzzy=False
    )

    if index != -1:
        f = files[index];
        key, index, yn = rofi(
            f'Overwrite {name}?',
            ['y', 'n'],
            ['-theme', '~/.config/rofi/ribbon.rasi', '-auto-select'],
            fuzzy=False
        )
        if yn == 'n':
            return

    (directory / f'{name}.svg').write_text(get(TARGET))

def style_mode(event, keysym, manager):
    paste_mode('style', event, keysym, manager)

def object_mode(event, keysym, manager):
    paste_mode('object', event, keysym, manager)

def save_style_mode():
    save_mode('style')

def save_object_mode():
    save_mode('object')
