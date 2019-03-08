from Xlib.display import Display
from Xlib import X
import time
import signal 
import sys

disp=Display()
screen=disp.screen()
root=screen.root

def handle_event(evt):
    print(evt)

def main():
    inkscapes = [
        w for w in screen.root.query_tree().children
        if w.get_wm_class() and w.get_wm_class()[0] ==  'inkscape'
    ]

    print(inkscapes)

    for inkscape in inkscapes:
        inkscape.grab_key(10, X.NONE, True,X.GrabModeAsync, X.GrabModeAsync)

    signal.signal(signal.SIGALRM, lambda a,b:sys.exit(1))
    signal.alarm(10)
    # grab_key(62, X.NONE)
    while True:
          evt=root.display.next_event()
          if evt.type in [X.KeyPress, X.KeyRelease]: #ignore X.MappingNotify(=34)
             handle_event(evt)

if __name__ == '__main__':
   main()
