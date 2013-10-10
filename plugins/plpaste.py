from util import hook, web


@hook.command(adminonly=True)
def plpaste(inp, bot=None):
    if inp in bot.commands:
        with open(bot.commands[inp][0].func_code.co_filename.strip()) as f:
            return web.haste(f.read(), ext='py')
    else:
        return "Could not find specified plugin."
