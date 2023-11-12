import lightbulb
import hikari
import comm
import miru

plugin = lightbulb.Plugin('ownr', "Owner only commands")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("shutdown", "Shuts down the bot", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def shutdown(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.respond("Shutting down...")
    quit()

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("slst", "Lists the bot's servers", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def slst(ctx: lightbulb.Context):
    comm.log_com(ctx)
    g = await ctx.app.rest.fetch_my_guilds()
    results = [item for item in g]
    re = ""
    for i in range(len(results)):
        re += str(results[i].id) + " - " + results[i].name + "\n"
    await ctx.respond(re)

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("server", "The server to leave", type=int, required=True)
@lightbulb.command("leave", "Lists the bot's servers", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def leave(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.app.rest.leave_guild(ctx.options.server)
    print("Left server")

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("bancount", "Count bans in a server", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def bancount(ctx: lightbulb.Context):
    comm.log_com(ctx)
    bans = await ctx.app.rest.fetch_bans(ctx.guild_id)
    await ctx.respond("This server has " + str(len(bans)) + " bans.")

"""
@plugin.command
@lightbulb.command("test", "test 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def test(ctx: lightbulb.Context):
    comm.log_com(ctx)
    print(ctx.event.message.attachments)

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("channel", "The channel to read.", required=True)
@lightbulb.command("readmsg", "Reads messages", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def readmsg(ctx: lightbulb.Context):
    comm.log_com(ctx)
    messages = ( await ctx.app.rest.fetch_messages(int(ctx.options.channel)).limit(100) )
    s = ""
    for i in messages:
        m = await ctx.app.rest.fetch_message(i.channel_id, i.id)
        t = str(m.author) + ": " + m.content + "\n"
        s += t
        print(t)


"""
