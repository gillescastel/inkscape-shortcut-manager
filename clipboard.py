import subprocess

def copy(string, target=None):
    extra_args = []
    if target != None:
        extra_args += ['-target', target]

    return subprocess.run(
        ['xclip', '-selection', 'c'] + extra_args,
        universal_newlines=True,
        input=string
    )

def get(target=None):
    extra_args = []
    if target != None:
        extra_args += ['-target', target]

    result = subprocess.run(
        ['xclip', '-selection', 'c', '-o'] + extra_args,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    # returncode = result.returncode
    stdout = result.stdout.strip()
    return stdout
