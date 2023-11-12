import lightbulb
import comm
import sqlite3
import random
import hikari
import math

plugin = lightbulb.Plugin('econ', 'MONEY MONEY MONEY MONEY MONEY -Mr Krabs')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

coneco = sqlite3.connect("./db/econ.db")
cureco = coneco.cursor()

def table_check(s, i):
    cureco.execute("CREATE TABLE IF NOT EXISTS eco_" + str(s) + "(uid INTEGER PRIMARY KEY, bank INTEGER, wallet INTEGER)")
    coneco.commit()
    cureco.execute("SELECT * FROM eco_" + str(s) + " WHERE uid=?", (int(i),))
    if cureco.fetchall() == []:
        cureco.execute("INSERT INTO eco_" + str(s) + " VALUES (?, ?, ?)", (int(i), 10, 90) )
        coneco.commit()
    coneco.commit()

@plugin.command
@lightbulb.option("user", "The user to check balance from.", type=hikari.Member, required=False)
@lightbulb.set_help("Checks a user's balance (yours if user is not specified). Can use mention or user ID")
@lightbulb.command("balance", "See the balances of a user", aliases=["bal", "b"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def balance(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = ctx.options.user.id
    except:
        u = int(ctx.author.id)
    if u == int(ctx.author.id):
        selfcheck = "Your"
    else:
        mem = await ctx.app.rest.fetch_user(u)
        selfcheck = mem.username + "'s"
    table_check(ctx.guild_id, u)
    cureco.execute("SELECT bank, wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (u,))
    bank, wallet = cureco.fetchone()
    coneco.commit()

    m = selfcheck + " balance:\nWallet: Ξ" + str(wallet) + "\nBank: Ξ" + str(bank)
    await comm.send_msg(ctx,m)

@plugin.command
@lightbulb.option("amount", "The amount of money to deposit.", required=True, type=int)
@lightbulb.set_help("Deposits a set amount of money in the bank. 10% of your net worth must remain in your wallet when depositing.")
@lightbulb.command("deposit", "Put the money in the bank", aliases=["dep"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def deposit(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.author.id
    table_check(ctx.guild_id, u)
    cureco.execute("SELECT bank, wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (u,))
    bank, wallet = cureco.fetchone()
    coneco.commit()
    max_b = 0.9 * (bank + wallet)
    if ctx.options.amount > wallet:
        await comm.send_msg(ctx,"You don't have that amount of money to deposit")
    elif ctx.options.amount < 0:
        await comm.send_msg(ctx,"You can't deposit negative money")
    elif (bank + ctx.options.amount) > max_b:
        await comm.send_msg(ctx,"You cannot deposit this amount of money. 10% of your money must be left in your wallet.\nFor you, the max amount of money in the bank is currently: Ξ" + str(max_b) + ", meaning you can only deposit Ξ" + str(max_b - bank))
    else:
        bank += ctx.options.amount
        wallet -= ctx.options.amount
        cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET bank=?, wallet=? WHERE uid=?", (bank,wallet, ctx.author.id))
        coneco.commit()
        await comm.send_msg(ctx,"Deposited Ξ" + str(ctx.options.amount))

@deposit.set_error_handler
async def deposit_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotEnoughArguments):
        await comm.send_msg(ctx,"You didn't tell me how much to deposit!")

@plugin.command
@lightbulb.option("amount", "The amount of money to withdraw.", required=True, type=int)
@lightbulb.set_help("Withdraws a set of money from your bank")
@lightbulb.command("withdraw", "Put the money in the bag", aliases=["wd", "with", "w"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def withdraw(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.author.id
    table_check(ctx.guild_id, u)
    cureco.execute("SELECT bank, wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (u,))
    bank, wallet = cureco.fetchone()
    coneco.commit()
    if ctx.options.amount > bank:
        await comm.send_msg(ctx,"You don't have that amount of money to deposit")
    elif ctx.options.amount < 0:
        await comm.send_msg(ctx,"You can't withdraw negative money")
    else:
        bank -= ctx.options.amount
        wallet += ctx.options.amount
        cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET bank=?, wallet=? WHERE uid=?", (bank,wallet, ctx.author.id))
        coneco.commit()
        await comm.send_msg(ctx,"Withdrew Ξ" + str(ctx.options.amount))

@withdraw.set_error_handler
async def withdraw_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotEnoughArguments):
        await comm.send_msg(ctx,"You didn't tell me how much to withdraw!")

@plugin.command
@lightbulb.option("amount", "The amount of money to gamble.", required=True, type=int)
@lightbulb.set_help("Almost 50% odds! 5/11 chance to win.")
@lightbulb.command("gamble", "Spin away!")
@lightbulb.implements(lightbulb.PrefixCommand)
async def gamble(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id, ctx.author.id)
    cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (ctx.author.id,))
    wallet, = cureco.fetchone()
    coneco.commit()
    if ctx.options.amount > wallet:
        await comm.send_msg(ctx,"You don't have that amount of money to gamble")
    elif ctx.options.amount < 0:
        await comm.send_msg(ctx,"You can't gamble negative money")
    else:
        r = random.randint(0,10)
        if r in [0,1,2,3,4,5]:
            cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (wallet-ctx.options.amount, ctx.author.id))
            coneco.commit()
            await comm.send_msg(ctx,"💸💸💸 You LOST Ξ" + str(ctx.options.amount))
        elif r in [6,7,8,9,10]:
            cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (wallet+ctx.options.amount, ctx.author.id))
            coneco.commit()
            await comm.send_msg(ctx,"💰💰💰 You WON Ξ" + str(ctx.options.amount))

@plugin.command
@lightbulb.option("page", "The page you want (1 page = 10)", type=int, default=1)
@lightbulb.set_help("See the top 10 richest folks")
@lightbulb.command("leaderboard", "Check the top 10 users", aliases=["lb"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def leaderboard(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.author.id
    table_check(ctx.guild_id, ctx.author.id)
    cureco.execute("SELECT uid, wallet + bank AS netto FROM eco_" + str(ctx.guild_id) + " ORDER BY netto DESC")
    t = cureco.fetchall()
    coneco.commit()
    if ctx.options.page > math.ceil(len(t)/10):
        page = math.ceil(len(t)/10) -1
    else:
        page = ctx.options.page -1
    msg = ""
    for b in range(len(t) % 10):
        id, net = t[b + page*10]
        if len(str(net)) > 3:
            trunc = str(net)[0] + "." + str(net)[1]
            trunc += str(int(str(net)[2])+1) if int(str(net)[3]) >= 5 else str(net)[2]
            trunc += "e" + str(len(str(net))-1)
        else:
            trunc = str(net)
        msg += str(b+1 + page*10) + ". <@" + str(id) +">: Ξ" + trunc + "\n"
    msg += "Page " + str(page +1) + " out of " + str(math.ceil(len(t)/10))
    embed = hikari.Embed(title="Economy Leaderboard", description=msg, color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3600, 1, lightbulb.UserBucket)
@lightbulb.set_help("1 hour cooldown. Get between Ξ20 and Ξ120.")
@lightbulb.command("work", "Get money nicely", aliases=["job"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def work(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id, ctx.author.id)
    p = random.randint(20, 120)
    cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (ctx.author.id,))
    wallet, = cureco.fetchone()
    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (wallet + p, ctx.author.id))
    coneco.commit()
    await comm.send_msg(ctx,"You earned Ξ" + str(p) + " for your hard work.")

"""
@plugin.command
@lightbulb.add_cooldown(3600*24, 1, lightbulb.UserBucket)
@lightbulb.set_help("1 day cooldown.")
@lightbulb.command("daily", "Get cash yo")
@lightbulb.implements(lightbulb.PrefixCommand)
async def daily(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id, ctx.author.id)
    p = random.randint(50, 200)
    cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (ctx.author.id,))
    wallet, = cureco.fetchone()
    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (wallet + p, ctx.author.id))
    coneco.commit()
    await comm.send_msg(ctx,"You earned Ξ" + str(p) + " for existing.")

@plugin.command
@lightbulb.add_cooldown(3600*24*7, 1, lightbulb.UserBucket)
@lightbulb.set_help("1 week cooldown.")
@lightbulb.command("weekly", "Get cash yo")
@lightbulb.implements(lightbulb.PrefixCommand)
async def weekly(ctx: lightbulb.Context):
    comm.log_com(ctx)
    table_check(ctx.guild_id, ctx.author.id)
    p = random.randint(350, 1400)
    cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (ctx.author.id,))
    wallet, = cureco.fetchone()
    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (wallet + p, ctx.author.id))
    coneco.commit()
    await comm.send_msg(ctx,"You earned Ξ" + str(p) + " for existing.")

@plugin.command
@lightbulb.add_cooldown(3600, 1, lightbulb.UserBucket)
@lightbulb.set_help("1 hour cooldown. Ξ100 fine if caught (50%).")
@lightbulb.option("user", "The user to rob.", type=hikari.Member, required=True)
@lightbulb.command("rob", "Put their money in the bag")
@lightbulb.implements(lightbulb.PrefixCommand)
async def rob(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
    if u == ctx.author.id:
        await comm.send_msg(ctx,"You cannot rob yourself")
    else:
        table_check(ctx.guild_id, u)
        table_check(ctx.guild_id, ctx.author.id)
        cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (int(ctx.author.id),))
        self_wallet, = cureco.fetchone()
        coneco.commit()
        if 100 > self_wallet:
            await comm.send_msg(ctx,"You need to have at least Ξ100 in your wallet")
        else:
            cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (u,))
            other_wallet, = cureco.fetchone()
            coneco.commit()
            if other_wallet == 0:
                await comm.send_msg(ctx,"This user is broke, idiot")
            else:
                r = random.randint(1,2)
                if r == 1:
                    w = random.randint(0.3*other_wallet, other_wallet)
                    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (self_wallet + w, ctx.author.id))
                    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (other_wallet - w, u))
                    coneco.commit()
                    await comm.send_msg(ctx,"YOU GOT EM DAWG. YOU STOLE Ξ" + str(w) + " FROM <@" + str(u) + ">!")
                elif r == 2:
                    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (self_wallet - 100, ctx.author.id))
                    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (other_wallet + 100, u))
                    coneco.commit()
                    await comm.send_msg(ctx,"You got caught attempting to steal from <@" + str(u) + ">. You have been fined Ξ100.")
                else:
                    await comm.send_msg(ctx,"Something has gone wrong")

@rob.set_error_handler
async def rob_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID) to rob.")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.option("amount", "The amount of money to pay.", required=True, type=int)
@lightbulb.option("user", "The user to pay.", type=hikari.Member, required=True)
@lightbulb.set_help("Give a user money, may use ping or user ID.")
@lightbulb.command("pay", "Put your money in the bag")
@lightbulb.implements(lightbulb.PrefixCommand)
async def pay(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
    if u == ctx.author.id:
        await comm.send_msg(ctx,"You cannot give money to yourself")
    else:
        table_check(ctx.guild_id, u)
        table_check(ctx.guild_id, ctx.author.id)
        cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (int(ctx.author.id),))
        self_wallet, = cureco.fetchone()
        coneco.commit()
        if ctx.options.amount > self_wallet:
            await comm.send_msg(ctx,"You dont have that amount of money to give away")
        else:
            cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (u,))
            other_wallet, = cureco.fetchone()
            coneco.commit()
            cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (self_wallet - ctx.options.amount, ctx.author.id))
            cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (other_wallet + ctx.options.amount, u))
            coneco.commit()
            await comm.send_msg(ctx,"Gave <@" + str(u) + "> Ξ" + str(ctx.options.amount))

@pay.set_error_handler
async def pay_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID) to give cash to.")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")
"""

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("amount", "The amount of money to add", required=True, type=int)
@lightbulb.option("user", "The user to check balance from.", type=hikari.Member, required=True)
@lightbulb.command("deb_add", "Add money to a user", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def deb_add(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = ctx.options.user.id
    table_check(ctx.guild_id, u)
    cureco.execute("SELECT wallet FROM eco_" + str(ctx.guild_id) + " WHERE uid=?", (u,))
    wallet, = cureco.fetchone()
    coneco.commit()
    cureco.execute("UPDATE eco_" + str(ctx.guild_id) + " SET wallet=? WHERE uid=?", (wallet + ctx.options.amount,u))
    coneco.commit()
