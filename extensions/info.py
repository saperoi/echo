import lightbulb
import comm
import math
import hikari

plugin = lightbulb.Plugin('info', 'Kowalski, analysis')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.set_help("Checks latency time in ms")
@lightbulb.command("ping", "Says pong!")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await comm.send_msg(ctx,"Pong! 🏓\t\tIt took " + str(math.floor(1000*plugin.bot.heartbeat_latency)) + " ms to arrive")

@plugin.command
@lightbulb.set_help("Checks if the bot is functioning (sees command and can reply)")
@lightbulb.command("check", "For debugging")
@lightbulb.implements(lightbulb.PrefixCommand)
async def check(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await comm.send_msg(ctx,"Was registered and could send message")
    print("Sent")

@plugin.command
@lightbulb.set_help("Only gets your user ID")
@lightbulb.command("uid", "Gets User ID")
@lightbulb.implements(lightbulb.PrefixCommand)
async def uid(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await comm.send_msg(ctx,"Your User ID is: " + str(ctx.author.id))

@plugin.command
@lightbulb.set_help("Only gets the current server ID")
@lightbulb.command("sid", "Gets Server ID")
@lightbulb.implements(lightbulb.PrefixCommand)
async def sid(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await comm.send_msg(ctx,"The Server ID is: " + str(ctx.guild_id))

@plugin.command
@lightbulb.option("user", "The user to get their avatar.", type=hikari.User, required=False)
@lightbulb.set_help("Gets a user's avatar. Can be ping or user ID")
@lightbulb.command("avatar", "Gets someone's avatar", aliases=["av"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def avatar(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = ctx.options.user.id
    except:
        u = int(ctx.author.id)
    ru = await ctx.app.rest.fetch_user(u)
    embed = hikari.Embed(title=str(ru.username) + "'s Avatar", description="", color=comm.color())
    if ru.avatar_url == None:
        embed.set_image(comm.url2uri(ru.default_avatar_url))
    else:
        embed.set_image(comm.url2uri(ru.avatar_url))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@avatar.set_error_handler
async def avatar_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.option("user", "The user to get their info.", type=hikari.User, required=False)
@lightbulb.set_help("The usual userinfo command. Can be ping or user ID")
@lightbulb.command("userinfo", "Pulls information about a user", aliases=["whois"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def userinfo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = ctx.options.user.id
    except:
        u = int(ctx.author.id)
    ru = await ctx.app.rest.fetch_user(u)
    try:
        rm = await ctx.app.rest.fetch_member(ctx.guild_id, u)
        if rm.nickname != None:
            nickname = rm.nickname
        else:
            nickname = None
        if rm.guild_avatar_url != None:
            servav = comm.url2uri(rm.guild_avatar_url)
        else:
            servav = None
        join = str(rm.joined_at)[:16]
    except:
        nickname = None
        servav = None
        join = None
    description = ""
    if nickname != None:
        description += "**Nickname**: " + nickname + "\n"
    description += "**UserID**: " + str(ru.id) + "\n"
    description += "**Created at**: " + str(ru.created_at)[:16] + "\n"
    if join != None:
        description += "**Joined at**: " + join + "\n"
    embed = hikari.Embed(title=str(ru.username) + "#" + str(ru.discriminator), description=description, color=comm.color())
    if ru.avatar_url == None:
        embed.set_thumbnail(comm.url2uri(ru.default_avatar_url))
    else:
        embed.set_thumbnail(comm.url2uri(ru.avatar_url))
    if servav != None:
        embed.set_image(servav)
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@userinfo.set_error_handler
async def userinfo_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.option("server", "The server to get their info.", type=int, required=False)
@lightbulb.set_help("The usual serverinfo command. Can be ping or user ID")
@lightbulb.command("serverinfo", "Pulls information about a server")
@lightbulb.implements(lightbulb.PrefixCommand)
async def serverinfo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.server == None:
        u = ctx.guild_id
    else:
        u = ctx.options.server
    su = await ctx.app.rest.fetch_guild(u)
    description = ""
    description += "**ServerID**: " + str(su.id) + "\n"
    description += "**Created at**: " + str(su.created_at)[:16] + "\n"
    description += "**Owner**: " + str(su.owner_id) + " <@" + str(su.owner_id) + ">\n"
    embed = hikari.Embed(title=str(su.name), description=description, color=comm.color())
    embed.set_thumbnail(comm.url2uri(su.icon_url))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@serverinfo.set_error_handler
async def serverinfo_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a server (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This server does not EXIST")
