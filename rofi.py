import subprocess

try:
    has_rofi = True if subprocess.run(['which', 'rofi'], stderr=STDOUT).returncode == 0 else False
except:
    has_rofi = False
try:
    has_dmenu = True if subprocess.run(['which', 'dmenu'], stderr=STDOUT).returncode == 0 else False
except:
    has_dmenu = False

def rofi(prompt, options, rofi_args=[], fuzzy=True):
    optionstr = '\n'.join(option.replace('\n', ' ') for option in options)
    if has_rofi:
        args = ['rofi', '-sort', '-no-levenshtein-sort']
        if fuzzy:
            args += ['-matching', 'fuzzy']
        args += ['-dmenu', '-p', prompt, '-format', 's', '-i']
        args += rofi_args
    elif has_dmenu:
        args = ['dmenu', '-i', '-l', '10', '-p', prompt]
    else:
        eprint("rofi nor dmenu has been found")
        return -1, -1, -1
    args = [str(arg) for arg in args]


    result = subprocess.run(args, input=optionstr, stdout=subprocess.PIPE, universal_newlines=True)
    returncode = result.returncode
    stdout = result.stdout.strip()

    selected = stdout.strip()
    try:
        index = [opt.strip() for opt in options].index(selected)
    except ValueError:
        index = -1

    if returncode == 0:
        key = 0
    elif returncode == 1:
        key = -1
    elif returncode > 9:
        key = returncode - 9

    return key, index, selected
