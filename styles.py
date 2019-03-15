from pathlib import Path
from time import sleep
import os
from Xlib import X

from clipboard import copy, get
from constants import TARGET
from rofi import rofi
import normal

pressed = []

script_path = Path(os.path.realpath(__file__)).parents[0]

data_dirs = {
    'style': script_path / '..' / 'data' / 'styles',
    'object': script_path / '..' / 'data' / 'objects',
}


def check(what, self, name):
    files = list(data_dirs[what].iterdir())
    names = [f.stem for f in files]

    filtered = list(i for i, n in enumerate(names) if n.startswith(name))
    # print(name,', '.join(n for n in names if n.startswith(name)))

    if len(filtered) == 0:
        pressed.clear()
        return back_to_normal(self)

    if len(filtered) == 1:
        index = filtered[0]
        copy(files[index].read_text(), target=TARGET)
        if what == 'style':
            self.press('v', X.ShiftMask | X.ControlMask)
        else:
            self.press('v', X.ControlMask)

        sleep(0.5) # Give the user some time when an object is added.
        return back_to_normal(self)


def back_to_normal(self):
    self.mode = normal.normal_mode
    pressed.clear()

def paste_mode(what, self, event, char):
    print('paste mode')
    if event.state & X.ControlMask:
        # there are modifiers
        # eg. X.ControlMask
        # ~or X.ShiftMask~
        return

    if not char:
        return

    if event.type != X.KeyRelease:
        return

    if char == 'Escape':
        if len(pressed) == 0:
            return back_to_normal(self)
        else:
            pressed.clear()
    else:
        pressed.append(char)
        return check(what, self, ''.join(pressed))


def save_mode(what, self):
    self.press('c', X.ControlMask)
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

def style_mode(self, event, char):
    paste_mode('style', self, event, char)

def object_mode(self, event, char):
    paste_mode('object', self, event, char)

def save_style_mode(self):
    save_mode('style', self)

def save_object_mode(self):
    save_mode('object', self)
