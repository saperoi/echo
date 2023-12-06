import lightbulb
import hikari
import comm
import sqlite3
import ast
import base64

plugin = lightbulb.Plugin('star', 'Like Starboard but more !')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

constr = sqlite3.connect("./db/star.db")
curstr = constr.cursor()

def table_exist_check(s):
    curstr.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("board_" + str(s),))
    if curstr.fetchone()[0] == 1:
        return True
    else:
        return False

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("board", "Board command group", aliases=["BOARD"])
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def board(ctx: lightbulb.Context):
    comm.log_com(ctx)
    embed = hikari.Embed(title="Boards!", color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    embed.add_field(name="**__WARNING__**", value="THIS DOES NOT WORK YET")
    embed.add_field(name=f"{ctx.prefix}board **lst**", value="List all boards")
    embed.add_field(name=f"{ctx.prefix}board **crt** <name> <channel> <emoji> <count>", value="Create a board")
    embed.add_field(name=f"{ctx.prefix}board **rmv** <name>", value="Does nothing yet")
    embed.add_field(name=f"{ctx.prefix}board **set** <name> <channel> <emoji> <count>", value="Update a pre-existing board.")
    await ctx.respond(embed)

@board.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("lst", "List all boards", aliases=["LST"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def lst(ctx: lightbulb.Context):
    comm.log_com(ctx)
    emojitable = "board_" + str(ctx.guild_id)
    try:
        curstr.execute("SELECT * FROM " + emojitable)
        r = curstr.fetchall()
        if str(r) == "[]":
            raise Exception

    except:
        await ctx.respond("This server has no reaction boards")
        return

    embed = hikari.Embed(title="Boards!", color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))

    for i in r:
        embed.add_field(name=f"{i[0]} - <#{i[1]}>", value=f"{i[3]} {hikari.Emoji.parse(i[2])}'s")

    await ctx.respond(embed)

@board.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("minimum", "Minimum emoji count for the bot", type=int, required=True)
@lightbulb.option("emoji", "Emoji for the reactions", type=str, required=True)
@lightbulb.option("channel", "The channel that mesages will be relayed to", type=hikari.GuildChannel, required=True)
@lightbulb.option("name", "Name for the board", type=str, required=True)
@lightbulb.command("crt", "Create a board", aliases=["CRT"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def crt(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.channel.guild_id != ctx.guild_id:
        await ctx.respond("The channel must be in the same server.")
        return
    emoji = hikari.Emoji.parse(ctx.options.emoji)
    await ctx.respond(f"Name: {ctx.options.name}, Channel: {ctx.options.channel}, Emoji: {emoji}, Minimum: {ctx.options.minimum}")
    if not table_exist_check(ctx.guild_id):
        curstr.execute("CREATE TABLE IF NOT EXISTS board_" + str(ctx.guild_id) + "(name TEXT PRIMARY KEY, channel TEXT, emoji TEXT, minimum TINYINT)")
    try:
        curstr.execute("INSERT INTO board_" + str(ctx.guild_id) + " VALUES (?, ?, ?, ?)", (comm.clean(ctx.options.name), (ctx.options.channel.id), str(ctx.options.emoji), ctx.options.minimum))
        constr.commit()
        await ctx.respond("Created board")
    except:
        await ctx.respond("A board already has this name")

@board.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("name", "Name for the board", type=str, required=True)
@lightbulb.command("rmv", "Remove a board", aliases=["RMV"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def rmv(ctx: lightbulb.Context):
    comm.log_com(ctx)
    pass
    try:
        curstr.execute("DELETE from board_" + str(ctx.guild_id) + " where name=?", (comm.clean(ctx.options.name),))
    except:
        await ctx.respond("This board does not exist")
    constr.commit()

@board.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("minimum", "Minimum emoji count for the bot", type=int, required=True)
@lightbulb.option("emoji", "Emoji for the reactions", type=hikari.Emoji, required=True)
@lightbulb.option("channel", "The channel that mesages will be relayed to", type=hikari.GuildChannel, required=True)
@lightbulb.option("name", "Name of the board", type=str, required=True)
@lightbulb.command("set", "Update a pre-existing board", aliases=["SET"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def set_board(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.channel.guild_id != ctx.guild_id:
        await ctx.respond("The channel must be in the same server.")
        return
    try:
        curstr.execute("UPDATE board_" + str(ctx.guild_id) + " SET channel=?, emoji=?, minimum=? WHERE name=?", ((ctx.options.channel.id), str(ctx.options.emoji), ctx.options.minimum, comm.clean(ctx.options.name)))
        constr.commit()
        await ctx.respond("Updated")
    except:
        await ctx.respond("An exception occured")

@plugin.listener(hikari.GuildReactionAddEvent, bind=True)
async def on_add_reaction(plugin, event: hikari.GuildReactionAddEvent):
    guild = event.guild_id
    channel = event.channel_id
    message = event.message_id
    emoji = event.emoji_name
    message_obj = await plugin.app.rest.fetch_message(channel, message)
    og_msg = f"{channel}/{message}"
    curstr.execute("SELECT * FROM board_" + str(guild) + " WHERE emoji=?", (emoji,))
    r = curstr.fetchall()
    constr.commit()
    if not r:
        return
    emoji = hikari.Emoji.parse(emoji)
    for c in r:
        for e in message_obj.reactions:
            if e.emoji == emoji:
                if e.count >= c[3]:
                    curstr.execute("SELECT * FROM message_equ WHERE original=? and emoji=?", (og_msg, emoji))
                    relays = curstr.fetchall()
                    if not relays:
                        embed = hikari.Embed(title="[Original Message]", url=f"https://discord.com/channels/{guild}/{channel}/{message}", description=message_obj.content)
                        if message_obj.author.avatar_url == None:
                            embed.set_author(name=message_obj.author.username, icon=comm.url2uri(message_obj.author.default_avatar_url))
                        else:
                            embed.set_author(name=message_obj.author.username, icon=comm.url2uri(message_obj.author.avatar_url))
                        if message_obj.attachments:
                            try:
                                print(message_obj.attachments)

                                embed.set_image(comm.url2uri(list(filter(lambda x: "image" in x.media_type, message_obj.attachments))[0].url))
                            except:
                                pass
                        own_message = f"{e.count} {e} | <#{channel}>"
                        new_msg = await event.app.rest.create_message(c[1], content=own_message, embed=embed)
                        new_msg = f"{new_msg.channel_id}/{new_msg.id}"
                        curstr.execute("INSERT INTO message_equ VALUES (?, ?, ?)", (new_msg, og_msg, emoji))
                        constr.commit()
                    else:
                        for relay in relays:
                            relayed_channel, relayed_message = relay[0].split("/")
                            bot_message_obj = await plugin.app.rest.fetch_message(relayed_channel, relayed_message)
                            own_message = f"{e.count} {e} | <#{channel}>"
                            await bot_message_obj.edit(content=own_message, attachments=None, embeds=bot_message_obj.embeds)

@plugin.listener(hikari.GuildReactionDeleteEvent, bind=True)
async def on_rmv_reaction(plugin, event: hikari.GuildReactionDeleteEvent):
    guild = event.guild_id
    channel = event.channel_id
    message = event.message_id
    emoji = event.emoji_name
    message_obj = await plugin.app.rest.fetch_message(channel, message)
    og_msg = f"{channel}/{message}"
    curstr.execute("SELECT * FROM board_" + str(guild) + " WHERE emoji=?", (emoji,))
    r = curstr.fetchall()
    constr.commit()
    if not r:
        return
    emoji = hikari.Emoji.parse(emoji)
    for c in r:
        for e in message_obj.reactions:
            if e.emoji == emoji:
                curstr.execute("SELECT * FROM message_equ WHERE original=? and emoji=?", (og_msg, emoji))
                relays = curstr.fetchall()
                print(e.count, c[3])
                if e.count >= c[3]:
                    for relay in relays:
                        relayed_channel, relayed_message = relay[0].split("/")
                        bot_message_obj = await plugin.app.rest.fetch_message(relayed_channel, relayed_message)
                        own_message = f"{e.count} {e} | <#{channel}>"
                        await bot_message_obj.edit(content=own_message, attachments=None, embeds=bot_message_obj.embeds)
                else:
                    for relay in relays:
                        relayed_channel, relayed_message = relay[0].split("/")
                        await plugin.app.rest.delete_message(relayed_channel, relayed_message)
                    curstr.execute("DELETE FROM message_equ WHERE relayed=?", (relay[0],))
