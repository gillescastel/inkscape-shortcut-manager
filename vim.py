import os
import tempfile
import subprocess
from constants import TARGET
from clipboard import copy
from Xlib import X

def open_vim(self, compile_latex):
    f = tempfile.NamedTemporaryFile(mode='w+', delete=False)

    f.write('$$')
    f.close()

    subprocess.run([
        'urxvt',
        '-fn', 'xft:Iosevka Term:pixelsize=24',
        '-geometry', '60x5',
        '-name', 'popup-bottom-center',
        '-e', "vim",
        "-u", "~/.minimal-tex-vimrc",
        f"{f.name}",
    ])

    latex = ""
    with open(f.name, 'r') as g:
        latex = g.read().strip()

    os.remove(f.name)

    if latex != '$$':
        if not compile_latex:
            svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <svg>
              <text
                 style="font-size:15px; font-family:'Latin Modern Math';-inkscape-font-specification:'Latin Modern Math, Normal';fill:#000000;fill-opacity:1;stroke:none;"
                 xml:space="preserve"><tspan sodipodi:role="line">{latex}</tspan></text>
            </svg> """
            copy(svg, target=TARGET)
        else:
            m = tempfile.NamedTemporaryFile(mode='w+', delete=False)
            m.write(r"""
                \documentclass[12pt,border=12pt]{standalone}

                \usepackage[utf8]{inputenc}
                \usepackage[T1]{fontenc}
                \usepackage{textcomp}
                \usepackage[dutch]{babel}
                \usepackage{amsmath, amssymb}
                \newcommand{\R}{\mathbb R}

                \begin{document}
            """ + latex + r"""\end{document}""")
            m.close()

            working_directory = tempfile.gettempdir()
            subprocess.run(
                ['pdflatex', m.name],
                cwd=working_directory,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            subprocess.run(
                ['pdf2svg', f'{m.name}.pdf', f'{m.name}.svg'],
                cwd=working_directory
            )

            with open(f'{m.name}.svg') as svg:
                subprocess.run(
                    ['xclip', '-selection', 'c', '-target', TARGET],
                    stdin=svg
                )

        self.press('v', X.ControlMask)
    self.press('Escape')
