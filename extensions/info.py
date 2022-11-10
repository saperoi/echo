import lightbulb
import comm
import math
import hikari
import random

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
@lightbulb.set_help("Only gets your user ID")
@lightbulb.command("uid", "Gets User ID")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def uid(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await comm.send_msg(ctx,"Your User ID is: " + str(ctx.author.id))

@plugin.command
@lightbulb.set_help("Only gets the current server ID")
@lightbulb.command("sid", "Gets Server ID")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def sid(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await comm.send_msg(ctx,"The Server ID is: " + str(ctx.guild_id))

@plugin.command
@lightbulb.option("user", "The user to get their avatar.", required=False)
@lightbulb.set_help("Gets a user's avatar. Can be ping or user ID")
@lightbulb.command("avatar", "Gets someone's avatar", aliases=["av"])
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def avatar(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = comm.user_id_check(ctx.options.user)
    except:
        u = int(ctx.author.id)
    ru = await ctx.app.rest.fetch_user(u)
    embed = hikari.Embed(title=str(ru.username) + "'s Avatar", description="", color=random.randint(0x0, 0xffffff))
    if ru.avatar_url == None:
        embed.set_image(ru.default_avatar_url)
    else:
        embed.set_image(ru.avatar_url)
    await ctx.respond(embed)

@avatar.set_error_handler
async def avatar_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.option("user", "The user to get their avatar.", required=False)
@lightbulb.set_help("The usual userinfo command. Can be ping or user ID")
@lightbulb.command("userinfo", "Gets someone's avatar", aliases=["whois"])
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def userinfo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = comm.user_id_check(ctx.options.user)
    except:
        u = int(ctx.author.id)
    ru = await ctx.app.rest.fetch_user(u)
    description = ""
    description += "UserID: " + str(ru.id) + "\n"
    description += "Created at: " + str(ru.created_at)[:16] + "\n"
    try:
        rm = await ctx.app.rest.fetch_member(ctx.guild_id, u)
        description += "Joined at: " + str(rm.joined_at)[:16] + "\n"
    except:
        pass
    embed = hikari.Embed(title=str(ru.username) + "#" + str(ru.discriminator), description=description, color=random.randint(0x0, 0xffffff))
    if ru.avatar_url == None:
        embed.set_thumbnail(ru.default_avatar_url)
    else:
        embed.set_thumbnail(ru.avatar_url)
    await ctx.respond(embed)

@userinfo.set_error_handler
async def userinfo_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.option("server", "The user to get their avatar.", required=False)
@lightbulb.set_help("The usual userinfo command. Can be ping or user ID")
@lightbulb.command("serverinfo", "Gets someone's avatar")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def serverinfo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.user == None:
        u = ctx.guild_id
    else:
        u = ctx.options.user
    su = await ctx.app.rest.fetch_guild(u)
    description = ""
    description += "ServerID: " + str(su.id) + "\n"
    description += "Created at: " + str(su.created_at)[:16] + "\n"
    description += "Owner: " + str(su.owner_id) + "<@" + str(su.owner_id) + ">\n"
    embed = hikari.Embed(title=str(su.name), description=description, color=random.randint(0x0, 0xffffff))
    embed.set_thumbnail(su.icon_url)
    await ctx.respond(embed)

@serverinfo.set_error_handler
async def serverinfo_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a server (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This server does not EXIST")
