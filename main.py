import Xlib
from Xlib.display import Display
from Xlib import X, XK
from Xlib.ext import xtest
from Xlib.protocol import event

from normal import normal_mode
import time

MASK = X.Mod2Mask

class Manager():
    def __init__(self):
        self.disp = Display()
        self.screen = self.disp.screen()
        self.root = self.screen.root
        self.inkscape = next(
            w for w in self.root.query_tree().children
            if w.get_wm_class() and w.get_wm_class()[0] == 'inkscape'
        )
        self.mode = normal_mode

    def event(self, name, detail, state):
        return name(
            time = X.CurrentTime,
            root = self.root,
            window = self.inkscape,
            same_screen = 0, child = Xlib.X.NONE,
            root_x = 0, root_y = 0, event_x = 0, event_y = 0,
            state = state,
            detail = detail
        )

    def string_to_keycode(self, key):
        keysym = XK.string_to_keysym(key)
        keycode = self.disp.keysym_to_keycode(keysym)
        return keycode

    def press(self, key, mask=X.NONE):
        keycode = self.string_to_keycode(key)
        self.inkscape.send_event(self.event(event.KeyPress, keycode, mask), propagate = True)
        self.inkscape.send_event(self.event(event.KeyRelease, keycode, mask), propagate = True)
        self.disp.flush()
        self.disp.sync()

    def grab(self):
        self.inkscape.grab_key(X.AnyKey, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)
        self.inkscape.change_attributes(event_mask = X.KeyReleaseMask | X.KeyPressMask)

    def ungrab(self):
        self.inkscape.ungrab_key(X.AnyKey, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)

    def listen(self):
        self.grab()
        while True:
            evt = self.disp.next_event()
            if evt.type in [X.KeyPress, X.KeyRelease]: #ignore X.MappingNotify(=34)
                keycode = evt.detail
                keysym = self.disp.keycode_to_keysym(keycode, 0)
                char = XK.keysym_to_string(keysym)
                self.disp.allow_events(X.ReplayKeyboard, X.CurrentTime)
                self.mode(self, evt, char)

m = Manager()
m.listen()
