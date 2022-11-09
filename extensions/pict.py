import lightbulb
import hikari
import comm
import PIL

plugin = lightbulb.Plugin('pict', "Because esmBot doesn't work")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
