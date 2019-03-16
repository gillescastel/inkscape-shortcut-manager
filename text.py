from Xlib import X
import normal
from time import sleep

def text_mode(self, event, char):
    if char and char == '`':
        self.press('Escape')
        sleep(0.1)
        self.press('Escape')
        self.mode = normal.normal_mode
        return 

    self.inkscape.send_event(event, propagate = True)
    self.disp.flush()
    self.disp.sync()
