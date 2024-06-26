import lightbulb
import hikari
import comm
import miru
import base64

plugin = lightbulb.Plugin('ownr', "Owner only commands")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.add_checks(comm.owners_only)
@lightbulb.option("extension_name", "The name of the extension to reload.")
@lightbulb.command("reload", "Reload an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def reload_cmd(ctx: lightbulb.Context):
    comm.log_com(ctx)
    ctx.app.reload_extensions("extensions." + ctx.options.extension_name)
    await ctx.respond("Reloaded " + ctx.options.extension_name)

@plugin.command
@lightbulb.add_checks(comm.owners_only)
@lightbulb.option("extension_name", "The name of the extension to load.")
@lightbulb.command("load", "Load an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def load_cmd(ctx: lightbulb.Context):
    comm.log_com(ctx)
    ctx.app.load_extensions("extensions." + ctx.options.extension_name)
    await ctx.respond("Loaded " + ctx.options.extension_name)

@plugin.command
@lightbulb.add_checks(comm.owners_only)
@lightbulb.option("extension_name", "The name of the extension to unload.")
@lightbulb.command("unload", "Unload an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def unload_cmd(ctx: lightbulb.Context):
    comm.log_com(ctx)
    ctx.app.unload_extensions("extensions." + ctx.options.extension_name)
    await ctx.respond("Unloaded " + ctx.options.extension_name)

@plugin.command
@lightbulb.add_checks(comm.owners_only)
@lightbulb.command("shutdown", "Shuts down the bot", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def shutdown(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.respond("Shutting down...")
    quit()

@plugin.command
@lightbulb.add_checks(comm.owners_only)
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
@lightbulb.add_checks(comm.owners_only)
@lightbulb.option("server", "The server to leave", type=int, required=True)
@lightbulb.command("leave", "Lists the bot's servers", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def leave(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.app.rest.leave_guild(ctx.options.server)
    print("Left server")


@plugin.command
@lightbulb.add_checks(comm.owners_only)
@lightbulb.option("server", "The server to create an invite for.", required=True, type=int)
@lightbulb.command("owner_ban_export", "Exports bans in server to a JSON.", aliases=["OWNER_BAN_EXPORT"], hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def owner_ban_export(ctx: lightbulb.Context):
    comm.log_com(ctx)
    bans = await ctx.app.rest.fetch_bans(ctx.options.server)
    j = "{"
    for ban in bans:
        j += '\n\t"' + str(ban.user.id) + '": {' + '\n\t\t"name": "' + str(ban.user.username) + "#" + str(ban.user.discriminator) + '", ' + '\n\t\t"banreason": "' + str(ban.reason).replace('"', '\\"').replace('\n', '\\n') + '"\n\t},'
    j = j[:-1] + "\n}"
    await ctx.respond(attachment = "data:application/json;base64,{}".format(base64.b64encode(str.encode(j)).decode() ))

@plugin.command
@lightbulb.add_checks(comm.owners_only)
@lightbulb.option("server", "The server to create an invite for.", required=True, type=int)
@lightbulb.command("invite", "Make a server invite", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def invite(ctx: lightbulb.Context):
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

@plugin.command
@lightbulb.add_checks(comm.owners_only)
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

@plugin.command
@lightbulb.add_checks(comm.owners_only)
@lightbulb.option("text", "The text to send.", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("channel", "The channel to send in.", required=True)
@lightbulb.command("sendmsg", "Sends messages", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def sendmsg(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.app.rest.create_message(ctx.options.channel, ctx.options.text)

"""
@plugin.command
@lightbulb.add_checks(comm.owners_only)
@lightbulb.option("text", "The text to send.", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("user", "The user to send to.", required=True)
@lightbulb.command("sendpm", "Sends DMs", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def sendpm(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.app.rest.dm(ctx.options.user, ctx.options.text)
"""
