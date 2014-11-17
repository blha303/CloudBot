from util import hook, web
from os import listdir


@hook.command(permissions=["adminonly"])
def plpaste(inp):
    if "/" in inp and inp.split("/")[0] != "util":
        return "Invalid input"
    try:
        with open("plugins/%s.py" % inp) as f:
            return web.haste(f.read(), ext='py')
    elif inp + ".py" in listdir('plugins/'):
        with open('plugins/{}.py'.format(inp)) as f:
            return web.haste(f.read(), ext='py')
    else:
        return "Could not find specified plugin."
