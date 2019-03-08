from evdev.uinput import UInput
from evdev import ecodes

def press(key, modifiers=[], uinput=UInput()):
    for mod in modifiers:
        uinput.write(ecodes.EV_KEY, mod, 1)
    uinput.write(ecodes.EV_KEY, key, 1)
    uinput.write(ecodes.EV_KEY, key, 0)
    for mod in modifiers:
        uinput.write(ecodes.EV_KEY, mod, 0)

    # synchronize ...
    uinput.syn()
