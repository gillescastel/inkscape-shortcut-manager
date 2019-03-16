from Xlib import X, XK, display

from clipboard import copy
from constants import TARGET
from vim import open_vim
import styles
from time import sleep

pressed = set()

events = []

def print_event(self, event):

    updown = ''
    if event.type == X.KeyPress:
        updown = '⇓'
    if event.type == X.KeyRelease:
        updown = '⇑'

    mods = []
    if event.state & X.ShiftMask:
        mods.append('Shift')
    if event.state & X.ControlMask:
        mods.append('Control')

    keycode = event.detail
    keysym = self.disp.keycode_to_keysym(keycode, 0)
    char = XK.keysym_to_string(keysym)

    return ''.join((updown, '+'.join(mods), ('+' + char if char else '')))

def event_to_string(self, event):
    mods = []
    if event.state & X.ShiftMask:
        mods.append('Shift')

    if event.state & X.ControlMask:
        mods.append('Control')

    keycode = event.detail
    keysym = self.disp.keycode_to_keysym(keycode, 0)
    char = XK.keysym_to_string(keysym)

    return ''.join(mod + '+' for mod in mods) + (char if char else '?')

def replay(self):
    for e in events:
        self.inkscape.send_event(e, propagate = True)

    self.disp.flush()
    self.disp.sync()
    # print('Replayed: ',  ', '.join(print_event(self, e) for e in events))
    events.clear()
    pressed.clear()

def normal_mode(self, event, char):
    events.append(event)
    # print('Events:   ' + ', '.join(print_event(self, e) for e in events))

    if event.type == X.KeyPress:
        if char:
            pressed.add(event_to_string(self, event))

    elif event.type == X.KeyRelease:
        handled = False

        if len(pressed) >= 2:
            fire(self, pressed)
            handled = True

        if len(pressed) == 1:
            ev = next(iter(pressed))

            if ev == 't':
                open_vim(self, compile_latex=False)
                handled = True

            if ev == 'Shift+t':
                open_vim(self, compile_latex=True)
                handled = True

            if ev == 'a':
                self.mode = styles.object_mode
                handled = True

            if ev == 'Shift+a':
                styles.save_object_mode(self)
                handled = True

            if ev == 's':
                self.mode = styles.style_mode
                handled = True

            if ev == 'Shift+s':
                styles.save_style_mode(self)
                handled = True

            if ev == 'w':
                self.press('p')
                handled=True


            if ev == 'x':
                self.press('percent', X.ShiftMask)
                handled=True

            if ev == 'f':
                self.press('b')
                handled=True

            if ev == 'z':
                self.press('z', X.ControlMask)
                handled=True

            if ev == 'Shift+z':
                self.press('Delete')
                handled=True
        if handled:
            events.clear()
            pressed.clear()
        else:
            replay(self)
    else:
        pass
        # print("hu?")

def fire(self, combination):
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
        style['marker-end'] = 'none'
        style['marker-start'] = 'none'
    if 'b' in combination:
        style['fill'] = 'black'
        style['fill-opacity'] = 1
        style['marker-end'] = 'none'
        style['marker-start'] = 'none'
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

    copy(svg, target=TARGET)
    self.press('v', X.ControlMask | X.ShiftMask)
