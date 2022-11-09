import os
from dotenv import load_dotenv
import hikari
import lightbulb
import comm

load_dotenv()

__tok = os.getenv("T")
__prf = os.getenv("P")

bot = lightbulb.BotApp(token=__tok, prefix=__prf)

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

@bot.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("shutdown", "Shuts down the bot")
@lightbulb.implements(lightbulb.PrefixCommand)
async def shutdown(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.respond("Shutting down...")
    quit()

@bot.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("slst", "Lists the bot's servers")
@lightbulb.implements(lightbulb.PrefixCommand)
async def slst(ctx: lightbulb.Context):
    comm.log_com(ctx)
    g = await ctx.app.rest.fetch_my_guilds()
    results = [item for item in g]
    re = ""
    for i in range(len(results)):
        re += str(results[i].id) + " - " + results[i].name + "\n"
    await ctx.respond(re)

bot.load_extensions_from("./extensions")

bot.run()
