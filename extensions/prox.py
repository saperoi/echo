import lightbulb
import hikari
import comm
import sqlite3

plugin = lightbulb.Plugin('prox', "Think hello and wait.")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

conmisc = sqlite3.connect("./db/misc.db")
curmisc = conmisc.cursor()
conprox = sqlite3.connect("./db/prox.db")
curprox = conprox.cursor()

@plugin.command
@lightbulb.option("text", "Text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("echo", "Repeats what you say", aliases=["parrot", "ECHO", "PARROT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def echo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if str(type(ctx.event)) == "<class 'hikari.events.message_events.GuildMessageCreateEvent'>":
        await ctx.app.rest.delete_message(ctx.event.message.channel_id, ctx.event.message.id)
    await ctx.respond(ctx.options.text)

@plugin.command
@lightbulb.option("text", "Text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.option("user", "The user to spoof as.", type=hikari.Member, required=True)
@lightbulb.command("spoof", "Repeats what you say as someone else", aliases=["SPOOF"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def spoof(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await comm.webhook_send(ctx, ctx.options.user.id, ctx.options.text)
    if str(type(ctx.event)) == "<class 'hikari.events.message_events.GuildMessageCreateEvent'>":
        await ctx.app.rest.delete_message(ctx.event.message.channel_id, ctx.event.message.id)

@plugin.command
@lightbulb.option("text", "Text to emojify", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("emojify", "Emojifies what you say", aliases=["emoji_echo", "EMOJIFY", "EMOJI_ECHO"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def emojify(ctx: lightbulb.Context):
    comm.log_com(ctx)
    s = list(ctx.options.text)
    for i in range(len(s)):
        if s[i] in "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN":
            s[i] = ":regional_indicator_" + s[i].lower() + ":"
        elif s[i] in " !?#*1234567890":
            s[i] = {" ": "     ", "!": ":exclamation", "?": ":question:", "#": ":hash:", "*": ":asterisk:", "1": ":one:", "2": ":two:", "3": ":three:", "4": ":four:", "5": ":five:", "6": ":six:", "7": ":seven:", "8": ":eight:", "9": ":nine:", "0": ":zero:"}[s[i]]
    await comm.webhook_send(ctx, ctx.author.id, ''.join(s))
    if str(type(ctx.event)) == "<class 'hikari.events.message_events.GuildMessageCreateEvent'>":
        await ctx.app.rest.delete_message(ctx.event.message.channel_id, ctx.event.message.id)

@plugin.command
@lightbulb.option("text", "Text to emojify", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.option("hard", "Hard or soft LEETCODE (Soft replaces A, E, I and O, hard replaces all)", type=bool, default=False, choices=[True, False])
@lightbulb.command("leet", "Emojifies what you say", aliases=["leetcode", "LEET", "LEETCODE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def leet(ctx: lightbulb.Context):
    comm.log_com(ctx)
    s = list(ctx.options.text.upper())
    hard = {"A": "4", "B": "13", "C": "[", "D": "|)", "E": "3", "F": "|=", "G": "6", "H": "#", "I": "1", "J": "]",
    "K": "|<", "L": "|_", "M": "/\\/\\", "N": "|\\|", "O": "0", "P": "", "Q": "|>", "R": "I2",
    "S": "5", "T": "7", "U": "(_)", "V": "\\/", "W": "\\/\\/", "X": "><", "Y": "`/", "Z": "2"
    }

    if ctx.options.hard == True or ctx.options.hard != "False":
        for i in range(len(s)):
            s[i] = hard[s[i]]
    else:
        s = list(''.join(s).replace("A", "4").replace("E", "3").replace("I", "1").replace("O", "0"))
    await comm.webhook_send(ctx, ctx.author.id, ''.join(s))
    if str(type(ctx.event)) == "<class 'hikari.events.message_events.GuildMessageCreateEvent'>":
        await ctx.app.rest.delete_message(ctx.event.message.channel_id, ctx.event.message.id)

@plugin.command
@lightbulb.option("text", "Text to ASCIIfy", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("ascii", "ASCIIfies what you say", aliases=["ASCII"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def ascii(ctx: lightbulb.Context):
    comm.log_com(ctx)
    fig = pyfiglet.Figlet(font="standard")
    ascii_text = fig.renderText(ctx.options.text)
    ascii_text = ascii_text.replace("```", "```")
    await comm.webhook_send(ctx, ctx.author.id, "```\n" + ascii_text + "\n```")
    if str(type(ctx.event)) == "<class 'hikari.events.message_events.GuildMessageCreateEvent'>":
        await ctx.app.rest.delete_message(ctx.event.message.channel_id, ctx.event.message.id)

@plugin.command
@lightbulb.option("text", "Text to Uwuify", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("uwuify", "UwUfies what you say", aliases=["uwu", "UWUIFY", "UWU"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def uwuify(ctx: lightbulb.Context):
    comm.log_com(ctx)
    s = ctx.options.text

    # just replacements
    s = s.replace("th", "d")
    s = s.replace("l", "w")
    s = s.replace("r", "w")
    s = s.replace("ou", "uw")
    s = s.replace("ohh", "uh")
    s = s.replace("ove", "uv")

    s = s.replace("at", "awt")
    s = s.replace("et", "ewt")
    s = s.replace("it", "iwt")
    s = s.replace("ot", "owt")
    s = s.replace("ut", "uwt")
    s = s.replace("na", "nya")
    s = s.replace("ne", "nye")
    s = s.replace("ni", "nyi")
    s = s.replace("no", "nyo")
    s = s.replace("nu", "nyu")
    s = s.replace("n!", "ny!")

    s = s.replace("Th", "D")
    s = s.replace("TH", "D")
    s = s.replace("L", "W")
    s = s.replace("R", "W")
    s = s.replace("OU", "UW")
    s = s.replace("OHH", "UHH")
    s = s.replace("OVE", "UV")

    s = s.replace("AT", "AWT")
    s = s.replace("ET", "EWT")
    s = s.replace("IT", "IWT")
    s = s.replace("OT", "OWT")
    s = s.replace("UT", "UWT")
    s = s.replace("NA", "NYA")
    s = s.replace("NE", "NYE")
    s = s.replace("NI", "NYI")
    s = s.replace("NO", "NYO")
    s = s.replace("NU", "NYU")
    s = s.replace("N!", "NY!")

    s = s.replace("Ou", "Uw")
    s = s.replace("Ohh", "Uhh")
    s = s.replace("Ove", "Uv")

    s = s.replace("At", "Awt")
    s = s.replace("Et", "Ewt")
    s = s.replace("It", "Iwt")
    s = s.replace("Ot", "Owt")
    s = s.replace("Ut", "Uwt")
    s = s.replace("Na", "Nya")
    s = s.replace("Ne", "Nye")
    s = s.replace("Ni", "Nyi")
    s = s.replace("No", "Nyo")
    s = s.replace("Nu", "Nyu")
    s = s.replace("N!", "Ny!")

    s = s.replace(".", " uwu\n")
    s = s.replace("!", " >w<\n")
    s = s.replace("??", " UmU\n")


    await comm.webhook_send(ctx, ctx.author.id, s)
    if str(type(ctx.event)) == "<class 'hikari.events.message_events.GuildMessageCreateEvent'>":
        await ctx.app.rest.delete_message(ctx.event.message.channel_id, ctx.event.message.id)

@plugin.command
@lightbulb.command("autoproxy", "Autoproxies as ECHO", aliases=["autoproxy"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def autoproxy(ctx: lightbulb.Context):
    comm.log_com(ctx)
    
    curprox.execute("SELECT * FROM echo_auto WHERE user=?", (ctx.author.id,) )
    if curprox.fetchall() == []:
        curprox.execute("INSERT INTO echo_auto VALUES (?, ?)", (ctx.author.id, "true") )
    conprox.commit()

    curprox.execute("SELECT state FROM echo_auto WHERE user=?", (ctx.author.id, ) )
    auto, = curprox.fetchone()
    conprox.commit()
    if auto == "false":
        curprox.execute("UPDATE echo_auto SET state=? WHERE user=?", ("true", ctx.author.id) )
        conprox.commit()
        await ctx.respond("Autoproxy TRUE")
    else:
        curprox.execute("UPDATE echo_auto SET state=? WHERE user=?", ("false", ctx.author.id) )
        conprox.commit()
        await ctx.respond("Autoproxy FALSE")


@plugin.listener(hikari.GuildMessageCreateEvent, bind=True)
async def echo_autoproxy_event(plugin, event: hikari.GuildMessageCreateEvent):
    curprox.execute("SELECT state FROM echo_auto WHERE user=?", (event.author_id, ) )
    try:
        auto, = curprox.fetchone()
    except:
        auto = "false"
        curprox.execute("INSERT INTO echo_auto VALUES (?, ?)", (event.author_id, auto) )
    conprox.commit()
    if auto != "true":
        return
    
    await event.app.rest.create_message(event.channel_id, event.content)
    await event.app.rest.delete_message(event.channel_id, event.message_id)