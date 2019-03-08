from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

import time
from constants import KEYSYM_MAP, NORMAL

from mode import mode
from normal import normal_mode

class ShortcutManager():
    def __init__(self):
        self.disp2 = Display()

    def is_inkscape(self):
        window = self.disp2.get_input_focus().focus
        cls = window.get_wm_class()
        return cls and cls[0] == 'inkscape'

    def meta_handler(self, handler):
        def handle(reply):
            print('yes')
            data = reply.data
            while len(data):
                event, data = rq.EventField(None).parse_binary_value(
                    data, self.disp.display, None, None)

                if not self.is_inkscape():
                    return

                keysym = self.disp.keycode_to_keysym(event.detail, 0)
                handler(event, keysym, self)

        return handle

    def listen(self, handler):
        self.disp = Display()
        root = self.disp.screen().root
        self.ctx = self.disp.record_create_context(
            # datum_flags
            0,
            # clients
            [record.AllClients],
            # rangers
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (0x02, 0x05),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }])

        self.disp.record_enable_context(self.ctx, self.meta_handler(handler))
        self.disp.record_free_context(self.ctx)

        try:
            while True:
                time.sleep(1)
                # Infinite wait, doesn't do anything as no events are grabbed
                event = root.display.next_event()
        except:
            print('exception!')

    def teardown(self):
        self.disp.record_disable_context(self.ctx)

sm = ShortcutManager()
mode('INIT')
time.sleep(1)
mode(NORMAL)
sm.listen(normal_mode)
