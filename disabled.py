from Xlib import X
from constants import KEYSYM_MAP, NORMAL
from mode import mode
import normal

def disabled_mode(event, keysym, manager):
    if keysym in KEYSYM_MAP:
        character = KEYSYM_MAP.get(keysym, 0)

        if event.type == X.KeyPress:
            if character == '`':
                mode(NORMAL)
                manager.teardown()
                manager.listen(normal.normal_mode)
        elif event.type == X.KeyRelease:
            pass
