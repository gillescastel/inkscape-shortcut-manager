from press import press
from Xlib import X
from evdev import ecodes

from clipboard import copy
from constants import KEYSYM_MAP, NORMAL, VIM, SAVE_OBJECT, OBJECT, SAVE_STYLE, STYLE, DISABLED

from mode import mode
from vim import open_vim
import styles
import disabled

pressed = set()
shift = False

def normal_mode(event, keysym, manager):
    global shift
    if event.state & X.ControlMask:
        # there are modifiers
        # eg. X.ControlMask
        # ~or X.ShiftMask~
        return

    if keysym in KEYSYM_MAP:
        character = KEYSYM_MAP.get(keysym, 0)

        if event.type == X.KeyPress:
            if event.state & X.ShiftMask:
                shift = True

            pressed.add(character)

        elif event.type == X.KeyRelease:

            if 'ESC' in pressed:
                press(ecodes.KEY_F1)
                pressed.clear()

            if character in pressed:
                if len(pressed) >= 2:
                    fire(pressed)
                else:
                    key = pressed.pop()
                    if key == 'w':
                        press(ecodes.KEY_F6) # pencil
                    if key == 'e':
                        press(ecodes.KEY_F5) # ellipse
                    if key == 'r':
                        press(ecodes.KEY_F4) # rectangle
                    if key == 't':
                        manager.teardown()
                        mode(VIM)
                        compile_latex = shift # shift-t compiles latex
                        open_vim(compile_latex)
                        mode(NORMAL)
                        manager.listen(normal_mode)
                    if key == 'y':
                        press(ecodes.KEY_F8) #text
                    
                    if key == '`':
                        manager.teardown()
                        mode(DISABLED)
                        manager.listen(disabled.disabled_mode)

                    if shift and key == 'a':
                        mode(SAVE_OBJECT)
                        manager.teardown()
                        styles.save_object_mode()
                        shift = False
                        mode(NORMAL)
                        manager.listen(normal_mode)
                    elif key == 'a':
                        mode(OBJECT)
                        manager.teardown()
                        manager.listen(styles.object_mode)

                    if shift and key == 's':
                        mode(SAVE_STYLE)
                        manager.teardown()
                        styles.save_style_mode()
                        shift = False
                        manager.listen(normal_mode)
                        mode(NORMAL)
                    elif key == 's':
                        mode(STYLE)
                        manager.teardown()
                        manager.listen(styles.style_mode)


                    if key == 'd':
                        press(ecodes.KEY_F7) # dropper
                    if key == 'f':
                        press(ecodes.KEY_F6, [ecodes.KEY_LEFTSHIFT]) # bezier
                    if key == 'h':
                        press(ecodes.KEY_H, [ecodes.KEY_LEFTSHIFT]) # flip

                    if key == 'z':
                        press(ecodes.KEY_DELETE) #delete

                    if key == 'x':
                        press(ecodes.KEY_5, [ecodes.KEY_LEFTSHIFT]) # snap

                    if key == 'v':
                        press(ecodes.KEY_V, [ecodes.KEY_LEFTSHIFT]) # flip

                pressed.clear()

                if shift:
                    shift = False

            if not (event.state & X.ShiftMask):
                shift = False


def fire(combination):
    pt = 1.327 # pixels
    w = 0.4 * pt
    thick_width = 0.8 * pt
    very_thick_width = 1.2 * pt

    style = {
        'stroke-opacity': 1
    }

    if {'s', 'a', 'd', 'g', 'h', 'x', 'e'} & combination:
        style['stroke'] = 'black'
        style['stroke-width'] = w
        style['marker-end'] = 'none'
        style['marker-start'] = 'none'
        style['stroke-dasharray'] = 'none'
    else:
        style['stroke'] = 'none'

    if 'g' in combination:
        w = thick_width
        style['stroke-width'] = w

    if 'h' in combination:
        w = very_thick_width
        style['stroke-width'] = w

    if 'a' in combination:
        style['marker-end'] = f'url(#marker-arrow-{w})'

    if 'x' in combination:
        style['marker-start'] = f'url(#marker-arrow-{w})'
        style['marker-end'] = f'url(#marker-arrow-{w})'

    if 'd' in combination:
        style['stroke-dasharray'] = f'{w},{2*pt}'

    if 'e' in combination:
        style['stroke-dasharray'] = f'{3*pt},{3*pt}'

    if 'f' in combination:
        style['fill'] = 'black'
        style['fill-opacity'] = 0.12
    if 'b' in combination:
        style['fill'] = 'black'
        style['fill-opacity'] = 1
    if not {'f', 'b'} & combination:
        style['fill'] = 'none'
        style['fill-opacity'] = 1


    if style['fill'] == 'none' and style['stroke'] == 'none':
        return

    svg = '''
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg>
'''

    if ('marker-end' in style and style['marker-end'] != 'none') or \
    ('marker-start' in style and style['marker-start'] != 'none'):
        svg += f'''
<defs id="marker-defs">
<marker
id="marker-arrow-{w}"
orient="auto-start-reverse"
refY="0" refX="0"
markerHeight="1.690" markerWidth="0.911">
  <g transform="scale({(2.40 * w + 3.87)/(4.5*w)})">
    <path
       d="M -1.55415,2.0722 C -1.42464,1.29512 0,0.1295 0.38852,0 0,-0.1295 -1.42464,-1.29512 -1.55415,-2.0722"
       style="fill:none;stroke:#000000;stroke-width:{0.6};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"
       inkscape:connector-curvature="0" />
   </g>
</marker>
</defs>
'''

    style_string = ';'.join('{}: {}'.format(key, value)
        for key, value in sorted(style.items(), key=lambda x: x[0])
    )
    svg += f'<inkscape:clipboard style="{style_string}" /></svg>'

    copy(svg, target='image/x-inkscape-svg')
    press(ecodes.KEY_V, [ecodes.KEY_LEFTSHIFT, ecodes.KEY_LEFTCTRL])
