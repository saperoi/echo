import os
import sys
from dotenv import load_dotenv
import hikari
import lightbulb
import comm

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

@bot.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("server", "The server to create an invite for.", required=True, type=int)
@lightbulb.command("inv", "Make a server invite")
@lightbulb.implements(lightbulb.PrefixCommand)
async def inv(ctx: lightbulb.Context):
    comm.log_com(ctx)
    g = await ctx.app.rest.fetch_my_guilds()
    gr = [item for item in g]
    gre = []
    for i in range(len(gr)):
        gre.append(int(gr[i].id))
    if ctx.options.server not in gre:
        re = "I am not a member of that guild"
    else:
        s = await ctx.app.rest.fetch_guild(ctx.options.server)
        print(s)
        print(s.id)
        c = await ctx.app.rest.fetch_guild_channels(s.id)
        re = ""
        print(c)
        f = True
        i = 0
        while f:
            try:
                t = type(c[i])
                print(t)
                if str(t) != "<class 'hikari.channels.GuildTextChannel'>":
                    raise Exception
                invite = await ctx.app.rest.create_invite(c[i])
                re = str(invite)
                f = False
            except:
                i += 1
    await ctx.respond(re)

bot.load_extensions_from("./extensions")

bot.run(activity=hikari.Activity(name="the " + __prf + "help command", type=hikari.presences.ActivityType.WATCHING), status=hikari.presences.Status.ONLINE)
