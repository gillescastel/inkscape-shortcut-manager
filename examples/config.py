import subprocess

def open_editor(filename):
    subprocess.run([
        'urxvt',
        '-fn', 'xft:Iosevka Term:pixelsize=24',
        '-geometry', '60x5',
        '-name', 'popup-bottom-center',
        '-e', "vim",
        "-u", "~/.minimal-tex-vimrc",
        f"{filename}",
    ])

def latex_document(latex):
    return r"""
        \documentclass[12pt,border=12pt]{standalone}

        \usepackage[utf8]{inputenc}
        \usepackage[T1]{fontenc}
        \usepackage{textcomp}
        \usepackage{amsmath, amssymb}
        \newcommand{\R}{\mathbb R}
        \usepackage{cmbright}

        \begin{document}
    """ + latex + r"\end{document}"

config = {
    'rofi_theme': '~/.config/rofi/ribbon.rasi',
    'font': 'Iosevka Term',
    'font_size': 10,
    'open_editor': open_editor,
    'latex_document': latex_document
}
