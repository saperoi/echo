import os
import sys
from dotenv import load_dotenv
import hikari
import lightbulb
import comm
import miru

load_dotenv()

mode = sys.argv[1]
if mode.lower() == "echo":
    __tok = os.getenv("ECHO_T")
    __prf = os.getenv("ECHO_P")
elif mode.lower() == "ache":
    __tok = os.getenv("ACHE_T")
    __prf = os.getenv("ACHE_P")

bot = lightbulb.BotApp(token=__tok, prefix=__prf, intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT)

"""
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.SlashCommandErrorEvent):
    if isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
        await event.context.respond("This command is currently on cooldown!")
    elif isinstance(event.exception, lightbulb.errors.NotOwner):
        await event.context.respond("This command can only be used by the owner of the bot!")
    elif isinstance(event.exception, hikari.errors.ForbiddenError):
        await event.context.respond("I am unable to perform this action")
    elif isinstance(event.exception, lightbulb.errors.BotMissingRequiredPermission):
        await event.context.respond("I do not have permission to perform this action")
"""

bot.load_extensions_from("./extensions")

bot.run(activity=hikari.Activity(name="the " + __prf + "help command", type=hikari.presences.ActivityType.WATCHING), status=hikari.presences.Status.ONLINE)
