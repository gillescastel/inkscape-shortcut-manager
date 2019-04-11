2019-04-11
- Listens for new Inkscape windows.

2019-03-16
- implemented pencil, snap, text/disable mode, bezier, delete, undo
- TODO:
    - modifier commands via styles?
    - Listen for new inkscape windows? Multiple instances!

2019-03-15
- Replaying events works
- Inkscape doesnt hang with Ctrl + C (Changed int(time.time()) to X.CurrentTime)
- Grabbing affects which events get to inkscape, however, we watch for all keypress and release events (as indicated in change_attributes)
- TODO:
    * w: pencil
    * x: snap
    * text/disable mode (\` or y)
    * f: bezier
    * z: delete/undo?
    * Modifier commands? rb: remove border, etc?

2019-03-09
- Current state: replaying events is hard.
- Inkscape hangs when Ctrl + C / V
- Can't succeed in only capturing non-ctrl and shift events?
