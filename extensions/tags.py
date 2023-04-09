import lightbulb
import re
import sqlite3
import comm
import hikari

plugin = lightbulb.Plugin('tags', 'Store some text and retrieve it')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

contag = sqlite3.connect("./db/tags.db")
curtag = contag.cursor()

def table_exist_check(s):
    curtag.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("tag_" + s,))
    if curtag.fetchone()[0] == 1:
        return True
    else:
        return False

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("tag", "Tags command group")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def tag(ctx: lightbulb.Context):
    comm.log_com(ctx)

@tag.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_GUILD) | lightbulb.owner_only)
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("ena", "Enables tags")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def ena(ctx: lightbulb.Context):
    comm.log_com(ctx)
    excstr = "CREATE TABLE IF NOT EXISTS tag_" + str(ctx.guild_id) + "(name TEXT PRIMARY KEY, id INTEGER, content TEXT)"
    curtag.execute(excstr)
    contag.commit()
    await comm.send_msg(ctx,"Created table " + "tag_" + str(ctx.guild_id))

@tag.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_GUILD) | lightbulb.owner_only)
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("dis", "Disables tags")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def dis(ctx: lightbulb.Context):
    comm.log_com(ctx)
    excstr = "DROP TABLE IF EXISTS tag_" + str(ctx.guild_id)
    curtag.execute(excstr)
    contag.commit()
    await comm.send_msg(ctx,"Deleted table " + "tag_" + str(ctx.guild_id))

@tag.child
@lightbulb.option("name", "Name", required=True)
@lightbulb.command("rec", "Recalls a tag")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def rec(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if table_exist_check(str(ctx.guild_id)):
        curtag.execute("SELECT content FROM tag_" + str(ctx.guild_id) + " WHERE name=?", (re.sub(r'[^a-zA-Z0-9_ ]', '',ctx.options.name),))
        r, = curtag.fetchone()
        await comm.send_msg(ctx,str(r))
    else:
        await comm.send_msg(ctx,"Tags need to be enabled. To do that, a user with the MANAGE_GUILD permission must run this command: '" + ctx.prefix + "tag ena'")

@tag.child
@lightbulb.option("content", "Content", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("name", "Name", required=True)
@lightbulb.command("crt", "Creates a tag")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def crt(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if table_exist_check(str(ctx.guild_id)):
        try:
            curtag.execute("INSERT INTO tag_" + str(ctx.guild_id) + " VALUES (?, ?, ?)", (re.sub(r'[^a-zA-Z0-9_ ]', '',ctx.options.name), ctx.author.id, ctx.options.content))
            await comm.send_msg(ctx,"Created tag " + str(ctx.options.name))
            contag.commit()
        except:
            await comm.send_msg(ctx,"Couldn't create tag, that name is already taken")
    else:
        await comm.send_msg(ctx,"Tags need to be enabled. To do that, a user with the MANAGE_GUILD permission must run this command: '" + ctx.prefix + "tag ena'")

@tag.child
@lightbulb.option("name", "Name", required=True)
@lightbulb.command("dlt", "Removes a tag")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def dlt(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if table_exist_check(str(ctx.guild_id)):
        curtag.execute("SELECT id FROM tag_" + str(ctx.guild_id) + " WHERE name=?", (re.sub(r'[^a-zA-Z0-9_ ]', '',ctx.options.name),))
        i, = curtag.fetchone()
        if int(i) == int(ctx.author.id) or int(ctx.author.id) == 738772518441320460:
            curtag.execute("DELETE from tag_" + str(ctx.guild_id) + " where name=?", (re.sub(r'[^a-zA-Z0-9_ ]', '',ctx.options.name),))
            await comm.send_msg(ctx,"Removed tag " + str(ctx.options.name))
            contag.commit()
        else:
            await comm.send_msg(ctx,"You are not allowed to remove tags that aren't yours")
    else:
        await comm.send_msg(ctx,"Tags need to be enabled. To do that, a user with the MANAGE_GUILD permission must run this command: '" + ctx.prefix + "tag ena'")

@tag.child
@lightbulb.command("lst", "Lists all tags")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def lst(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if table_exist_check(str(ctx.guild_id)):
        curtag.execute("SELECT name FROM tag_" + str(ctx.guild_id))
        r = str(curtag.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("',", "'")
        try:
            await comm.send_msg(ctx,str(r))
        except:
            await comm.send_msg(ctx,"There are no tags in this server, create one with: '" + ctx.prefix + "tag crt <tag name> <tag text>'")
    else:
        await comm.send_msg(ctx,"Tags need to be enabled. To do that, a user with the MANAGE_GUILD permission must run this command: '" + ctx.prefix + "tag ena'")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("g_tag", "Global tags command group (requires normal tags to be enabled)")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def g_tag(ctx: lightbulb.Context):
    comm.log_com(ctx)

@g_tag.child
@lightbulb.option("name", "Name", required=True)
@lightbulb.command("rec", "Recalls a tag")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def rec(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if table_exist_check(str(ctx.guild_id)):
        curtag.execute("SELECT content FROM global WHERE name=?", (re.sub(r'[^a-zA-Z0-9_ ]', '',ctx.options.name),))
        r, = curtag.fetchone()
        await comm.send_msg(ctx,str(r))
    else:
        await comm.send_msg(ctx,"Tags need to be enabled. To do that, a user with the MANAGE_GUILD permission must run this command: '" + ctx.prefix + "tag ena'")

@g_tag.child
@lightbulb.command("lst", "Lists all tags")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def lst(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if table_exist_check(str(ctx.guild_id)):
        curtag.execute("SELECT name FROM global")
        r = str(curtag.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("',", "'")
        await comm.send_msg(ctx,str(r))
    else:
        await comm.send_msg(ctx,"Tags need to be enabled. To do that, a user with the MANAGE_GUILD permission must run this command: '" + ctx.prefix + "tag ena'")
