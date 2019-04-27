from Xlib import X
import normal
from time import sleep

def text_mode(self, event, char):
    """
    'text mode' for when you just want to type text, i.e. 'disabled mode'.

    """
    if char and char == '`':
        """
        Go to normal mode again!
        """
        self.press('Escape')
        sleep(0.1)
        self.press('Escape')
        self.mode = normal.normal_mode
        return 

    self.inkscape.send_event(event, propagate = True)
    self.disp.flush()
    self.disp.sync()
