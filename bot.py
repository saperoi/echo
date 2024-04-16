import os
import sys
from dotenv import load_dotenv
import hikari
import lightbulb
from lightbulb.ext import tasks
import comm
import miru
import random

load_dotenv()

try:
    mode = sys.argv[1]
except:
    mode = "echo"
mode = mode.lower()
if mode == "ache":
    token = os.getenv("ACHE_TOKEN")
    prefix = os.getenv("ACHE_PREFIX")
    uid = os.getenv("ACHE_ID")
if mode == "echo":
    print('here')
    token = os.getenv("ECHO_TOKEN")
    prefix = os.getenv("ECHO_PREFIX")
    uid = os.getenv("ECHO_ID")

bot = lightbulb.BotApp(token=token, prefix=[prefix, prefix.upper(), prefix.replace("/", "\/"), prefix.upper().replace("/", "\/"), "<@" + uid + ">"], intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT)

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
        else:
            print(event.exception)

activities = [
    hikari.Activity(name="the " + prefix + "help command", type=hikari.ActivityType.WATCHING),
    hikari.Activity(name="the " + prefix + "help command", type=hikari.ActivityType.WATCHING),
    hikari.Activity(name="THINK HELLO AND WAIT.", type=hikari.ActivityType.CUSTOM),
]

@tasks.task(s=40, auto_start=True, pass_app=True)
async def bot_status(bot):
    act = random.choice(activities)
    await bot.update_presence(activity=act, status=hikari.presences.Status.ONLINE)

miru.install(bot)
tasks.load(bot)
bot.load_extensions_from("./extensions")
bot.run(activity=hikari.Activity(name="THINK HELLO AND WAIT.", type=hikari.ActivityType.CUSTOM), status=hikari.presences.Status.ONLINE)
