import threading
import Xlib
from Xlib.display import Display
from Xlib import X, XK
from Xlib.protocol import event

from normal import normal_mode

class Manager():
    def __init__(self, inkscape_id):
        self.id = inkscape_id
        self.disp = Display()
        self.screen = self.disp.screen()
        self.root = self.screen.root

        self.inkscape = self.disp.create_resource_object('window', inkscape_id)
        self.mode = normal_mode

    def event(self, name, detail, state):
        return name(
            time=X.CurrentTime,
            root=self.root,
            window=self.inkscape,
            same_screen=0, child=Xlib.X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=state,
            detail=detail
        )

    def string_to_keycode(self, key):
        keysym = XK.string_to_keysym(key)
        keycode = self.disp.keysym_to_keycode(keysym)
        return keycode

    def press(self, key, mask=X.NONE):
        keycode = self.string_to_keycode(key)
        self.inkscape.send_event(self.event(event.KeyPress, keycode, mask), propagate=True)
        self.inkscape.send_event(self.event(event.KeyRelease, keycode, mask), propagate=True)
        self.disp.flush()
        self.disp.sync()

    def grab(self):
        self.inkscape.grab_key(X.AnyKey, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)

        # Ungrab window manager shortcuts (Super + ...)
        self.inkscape.ungrab_key(self.string_to_keycode('Super_L'), X.AnyModifier, True)
        self.inkscape.change_attributes(event_mask=X.KeyReleaseMask | X.KeyPressMask | X.StructureNotifyMask)

    def ungrab(self):
        self.inkscape.ungrab_key(X.AnyKey, X.AnyModifier, True)

    def listen(self):
        self.grab()
        while True:
            evt = self.disp.next_event()
            if evt.type in [X.KeyPress, X.KeyRelease]:
                keycode = evt.detail
                keysym = self.disp.keycode_to_keysym(keycode, 0)
                char = XK.keysym_to_string(keysym)
                self.disp.allow_events(X.ReplayKeyboard, X.CurrentTime)

                self.mode(self, evt, char)

            if evt.type == X.DestroyNotify:
                if evt.window.id == self.id:
                    self.ungrab()
                    return


def create(inkscape_id):
    m = Manager(inkscape_id)
    m.listen()

def is_inkscape(window):
    return window.get_wm_class() and window.get_wm_class()[0] == 'inkscape'

def main():
    disp = Display()
    screen = disp.screen()
    root = screen.root

    # First listen for existing windows
    for window in root.query_tree().children:
        if is_inkscape(window):
            print('Found existing window')
            listen = threading.Thread(target=create, args=[window.id])
            listen.start()


    # New windows
    root.change_attributes(event_mask=X.SubstructureNotifyMask)
    while True:
        evt = disp.next_event()
        if evt.type == X.CreateNotify:
            window = evt.window
            try:
                if is_inkscape(window):
                    print('New window!')
                    listen = threading.Thread(target=create, args=[window.id])
                    listen.start()

            except Xlib.error.BadWindow:
                pass

if __name__ == '__main__':
    main()
