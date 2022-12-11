import lightbulb
import comm
import sqlite3
import random
import hikari
import math
import random

plugin = lightbulb.Plugin('econ', 'MONEY MONEY MONEY MONEY MONEY -Mr Krabs')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

coneco = sqlite3.connect("./db/econ.db")
cureco = coneco.cursor()
coninv = sqlite3.connect("./db/invt.db")
curinv = coninv.cursor()

def eco_table_check(s, i):
    cureco.execute("CREATE TABLE IF NOT EXISTS eco_" + str(s) + "(uid INTEGER PRIMARY KEY, bank INTEGER, wallet INTEGER)")
    coneco.commit()
    cureco.execute("SELECT * FROM eco_" + str(s) + " WHERE uid=?", (int(i),))
    if cureco.fetchall() == []:
        cureco.execute("INSERT INTO eco_" + str(s) + " VALUES (?, ?, ?)", (int(i), 0, 100) )
        coneco.commit()
    coneco.commit()

def inv_table_check(s, uid, iid):
    curinv.execute("CREATE TABLE IF NOT EXISTS inv_" + str(s) + "(uid INTEGER, item INTEGER, amount INTEGER)")
    coninv.commit()
    curinv.execute("SELECT * FROM inv_" + str(s) + " WHERE uid=? and item=?", (int(uid), int(iid)))
    if curinv.fetchall() == []:
        curinv.execute("INSERT INTO inv_" + str(s) + " VALUES (?, ?, ?)", (int(uid), int(iid), 0) )
        coninv.commit()
    coninv.commit()

@plugin.command
@lightbulb.option("page", "The page you want (1 page = 10)", type=int, default=1)
@lightbulb.command("shop", "Shows you all items")
@lightbulb.implements(lightbulb.PrefixCommand)
async def shop(ctx: lightbulb.Context):
    comm.log_com(ctx)
    curinv.execute("SELECT id, name, price FROM item")
    t = curinv.fetchall()
    coninv.commit()
    if ctx.options.page > math.ceil(len(t)/10):
        page = math.ceil(len(t)/10) -1
    else:
        page = ctx.options.page -1
    msg = ""
    for b in range(len(t) % 10):
        id, name, price = t[b + page*10]
        msg += str(id) + ". " + name + ": Ξ" + str(price) + "\n"
    msg += "Page " + str(page +1) + " out of " + str(math.ceil(len(t)/10))
    print(msg)
    await comm.send_msg(ctx,msg)

@plugin.command
@lightbulb.option("item", "The item you want (USE THE ID SHOWN IN THE SHOP)", type=int, default=1)
@lightbulb.command("buy", "Shows you all items")
@lightbulb.implements(lightbulb.PrefixCommand)
async def buy(ctx: lightbulb.Context):
    print(ctx.options.item)
    comm.log_com(ctx)
    curinv.execute("SELECT name, price, lim FROM item WHERE id=?", (ctx.options.item,))
    t = curinv.fetchone()
    coninv.commit()
    if t == None:
        await ctx.respond("There is no item with that ID.")
        return
    inv_table_check(ctx.guild_id, ctx.author.id, ctx.options.item)
    curinv.execute("SELECT name, price, lim FROM item WHERE id=?", (ctx.options.item,))
    name, price, limit = t
    cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (ctx.author.id,))
    wallet, = cureco.fetchone()
    if wallet < price:
        await ctx.respond("You don't have enough money to buy this")
        return
    coneco.commit()
    curinv.execute("SELECT amount FROM inv_" + str(ctx.guild_id) + " WHERE uid=? and item=?", (ctx.author.id, ctx.options.item))
    amount, = curinv.fetchone()
    coninv.commit()
    if limit != None and amount >= limit:
        await ctx.respond("You can't buy any more of this item.")
        return
    curinv.execute("UPDATE inv_" + str(ctx.guild_id) + " SET amount=? WHERE uid=? and item=?", (amount+1, ctx.author.id, ctx.options.item))
    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (wallet-price, ctx.author.id))
    coninv.commit()
    coneco.commit()
    await ctx.respond("You've bought the " + name)

@plugin.command
@lightbulb.option("page", "The page you want (1 page = 10)", type=int, default=1)
@lightbulb.command("inv", "Shows you all items", aliases=["inventory"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def inv(ctx: lightbulb.Context):
    comm.log_com(ctx)
    curinv.execute("CREATE TABLE IF NOT EXISTS inv_" + str(ctx.guild_id) + "(uid INTEGER, item INTEGER, amount INTEGER)")
    coninv.commit()
    curinv.execute("SELECT item, amount FROM inv_" + str(ctx.guild_id) + " WHERE uid=?", (ctx.author.id,))
    t = curinv.fetchall()
    if t == []:
        await ctx.respond("You have no items")
        return
    coninv.commit()
    if ctx.options.page > math.ceil(len(t)/10):
        page = math.ceil(len(t)/10) -1
    else:
        page = ctx.options.page -1
    msg = ""
    for b in range(len(t) % 10):
        item, amount = t[b + page*10]
        curinv.execute("SELECT name FROM item WHERE id=?", (item,))
        name, = curinv.fetchone()
        msg += str(amount) + " " + name + "\n"
    msg += "Page " + str(page +1) + " out of " + str(math.ceil(len(t)/10))
    print(msg)
    await comm.send_msg(ctx,msg)

@plugin.command
@lightbulb.option("item", "The item you want to use (USE THE ID SHOWN IN THE SHOP)", type=int, required=True)
@lightbulb.command("use", "Use an item of yours")
@lightbulb.implements(lightbulb.PrefixCommand)
async def use(ctx: lightbulb.Context):
    comm.log_com(ctx)
    inv_table_check(ctx.guild_id, ctx.author.id, ctx.options.item)
    curinv.execute("SELECT amount FROM inv_" + str(ctx.guild_id) + " WHERE uid=? and item=?", (ctx.author.id, ctx.options.item))
    amount, = curinv.fetchone()
    coninv.commit()
    if amount == 0:
        await ctx.respond("You don't own this item")
        return

    if ctx.options.item not in [0]:
        await ctx.respond("You can't use this item")
        return

# SHOVEL
    if ctx.options.item == 0:
        curinv.execute("SELECT amount FROM inv_" + str(ctx.guild_id) + " WHERE uid=? and item=?", (ctx.author.id, 1))
        license = curinv.fetchone()
        if license in [None, (0,)]:
            re = "You need a license to dig!"
        else:
            re = "You tried to dig..."
            p = random.randint(0,10)
            if p == 0:
                re += " BUT YOUR SHOVEL BROKE!"
                curinv.execute("UPDATE inv_" + str(ctx.guild_id) + " SET amount=? WHERE uid=? and item=?", (amount-1, ctx.author.id, ctx.options.item))
                coninv.commit()
            else:
                re += " and you found..."
                if p in [1, 3, 5, 7, 9]:
                    k = random.randint(0,101) * math.ceil(p/2)
                    re += " Ξ" + str(k) + "! Lucky you!"
                    cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (ctx.author.id,))
                    wallet, = cureco.fetchone()
                    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (wallet+k, ctx.author.id))
                    coneco.commit()
                else:
                    re += " something, but we don't know what it is yet."
        await ctx.respond(re)
