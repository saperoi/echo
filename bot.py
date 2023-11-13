import os
import sys
from dotenv import load_dotenv
import hikari
import lightbulb
import comm
import miru

load_dotenv()

try:
    mode = sys.argv[1]
except:
    mode = "echo"
mode = mode.lower()
if mode == "ache":
    __tok = os.getenv("ACHE_TOKEN")
    __prf = os.getenv("ACHE_PREFIX")
    __uid = os.getenv("ACHE_ID")
if mode == "echo":
    print('here')
    __tok = os.getenv("ECHO_TOKEN")
    __prf = os.getenv("ECHO_PREFIX")
    __uid = os.getenv("ECHO_ID")

bot = lightbulb.BotApp(token=__tok, prefix=[__prf, __prf.replace("/", "\/"), "<@" + __uid + ">"], intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT)
miru.install(bot)

if mode.lower() == "echo":
    @bot.listen(lightbulb.CommandErrorEvent)
    async def on_error(event):
        if isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
            await event.context.respond("This command is currently on cooldown!")
        elif isinstance(event.exception, lightbulb.errors.NotOwner):
            await event.context.respond("This command can only be used by the owner of the bot!")
        elif isinstance(event.exception, hikari.errors.ForbiddenError):
            await event.context.respond("I am unable to perform this action...")
        elif isinstance(event.exception, lightbulb.errors.BotMissingRequiredPermission):
            await event.context.respond("I do not have permission to perform this action...")
        elif isinstance(event.exception, lightbulb.errors.NSFWChannelOnly):
            await event.context.respond("This command can only be used in NSFW channels!")
        elif isinstance(event.exception, lightbulb.errors.CommandNotFound):
            await event.context.respond("This command doesn't exist...")
        elif isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
            await event.context.respond("You didn't provide enough arguments, check the help command.")
        elif isinstance(event.exception, lightbulb.errors.CheckFailure):
            await event.context.respond("You cannot run this command. It may be server-locked.")

bot.load_extensions_from("./extensions")
bot.run(activity=hikari.Activity(name="the " + __prf + "help command", type=hikari.presences.ActivityType.WATCHING), status=hikari.presences.Status.ONLINE)
