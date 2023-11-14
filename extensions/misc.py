import lightbulb
import hikari
import comm
import json
import requests
from dotenv import load_dotenv, find_dotenv
import os
import random
import sqlite3
import pyfiglet
import re

plugin = lightbulb.Plugin('misc', "I've no clue where else to put these")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.option("emoji", "The emoji to enlarge.", type=hikari.Emoji)
@lightbulb.set_help("Enlarge an emoji")
@lightbulb.command("emoji", "Emoji enlarger", aliases=["emoji_enlarge", "EMOJI", "EMOJI_ENLARGE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def emoji_enlarge(ctx: lightbulb.Context):
    comm.log_com(ctx)
    embed = hikari.Embed(title=ctx.options.emoji.name, color=comm.color())
    embed.set_image(ctx.options.emoji.url)
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("word", "The word to search for.", type=str, required=True)
@lightbulb.command("urban", "Look up a word on Urban Dictionary", aliases=["URBAN"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def urban(ctx: lightbulb.Context):
    comm.log_com(ctx)

    load_dotenv(find_dotenv())
    headers = {
        "X-RapidAPI-Key": os.getenv("URBAN_API"),
        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
    }

    querystring = {"term": ctx.options.word}
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    await comm.send_msg(ctx, data["list"][0]["definition"].replace("[","").replace("]",""))

@plugin.command
@lightbulb.option("word", "The word to search for.", type=str, required=True)
@lightbulb.command("dict", "Look up a word on DictionaryAPI.dev", aliases=["dictionary", "DICT", "DICTIONARY"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def dict(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + ctx.options.word
    r = requests.request("GET", url).text

    if r == """{"title":"No Definitions Found","message":"Sorry pal, we couldn't find definitions for the word you were looking for.","resolution":"You can try the search again at later time or head to the web instead."}""":
        await comm.send_msg(ctx, "This word doesn't exist.")
        return

    data = json.loads(r)

    re = ""

    for base_ in range(len(data)):
        re += str(base_ + 1) + ". " + data[base_]["word"] + " "
        try:
            re += + "*" + data[base_]["phonetic"] + "*\n"
        except:
            for f_ in range(len(data[base_]["phonetics"])):
                try:
                    re += "*" + data[base_]["phonetic"][f_][text] + "* "
                except:
                    pass
            re += "\n"
        for m_ in range(len(data[base_]["meanings"])):
            re += "\t" + str(m_ + 1) + ". *" + data[base_]["meanings"][m_]["partOfSpeech"] + "*\n"
            for def_ in range(len(data[base_]["meanings"][m_]["definitions"])):
                re += "\t\t" + str(def_ + 1) + ". " +  data[base_]["meanings"][m_]["definitions"][def_]["definition"] + "\n"
    await comm.send_msg(ctx, re.replace("\t", "        ").replace(" ", "\u00A0"))

@plugin.command
@lightbulb.option("comic", "The comic to pull.", type=int, required=False)
@lightbulb.command("xkcd", "Look up an XKCD comic", aliases=["XKCD"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def xkcd(ctx: lightbulb.Context):
    comm.log_com(ctx)
    num = ctx.options.comic
    if num == None:
        url = "https://xkcd.com/info.0.json"
        r = requests.request("GET", url).text
        data = json.loads(r)
        num = random.randint(1, data["num"])
    url = "https://xkcd.com/" + str(num) + "/info.0.json"
    r = requests.request("GET", url).text
    data = json.loads(r)
    embed = hikari.Embed(title=data["title"] + " [#" + str(data["num"]) + "]", description=data["alt"], color=comm.color())
    embed.set_image(data["img"])
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("joke", "Pull a random joke", aliases=["JOKE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def joke(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://v2.jokeapi.dev/joke/Any?type=single"
    r = requests.request("GET", url).text
    data = json.loads(r)
    embed = hikari.Embed(title=data["category"] + " [#" + str(data["id"]) + "]", description=data["joke"], color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("search", "Search terms", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("google", "Let me Google that for you...", aliases=["lmgtfy", "GOOGLE", "LMGTFY"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def lmgtfy(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if len(ctx.options.search) > 500:
        await ctx.respond("Your search should be no longer than 500 characters.")
        return
    await ctx.respond("<https://letmegooglethat.com/?q=" + ctx.options.search.replace(' ', '+') + ">")

@plugin.command
@lightbulb.option("search", "Search terms", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("duckduckgo", "Let me Duck Duck Go that for you...", aliases=["ddg", "lmddgtfy", "DUCKDUCKGO", "DDG", "LMDDGTFY"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def lmddgtfy(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if len(ctx.options.search) > 500:
        await ctx.respond("Your search should be no longer than 500 characters.")
        return
    await ctx.respond("<https://lmddgtfy.net/?q=" + ctx.options.search.replace(' ', '+') + ">")

@plugin.command
@lightbulb.option("url", "The URL to shorten", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("linkshortener", "Shorten a URL", aliases=["url", "link", "urlshortener", "isgd", "LINKSHORTENER", "URL", "LINK", "URLSHORTENER", "ISGD"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def linkshort(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://is.gd/create.php?format=simple&url=" + ctx.options.url
    r = requests.request("GET", url).text
    await ctx.respond(r)

@plugin.command
@lightbulb.command("meme", "Pull a random meme", aliases=["MEME"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def meme(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://meme-api.com/gimme"
    r = requests.request("GET", url).text
    data = json.loads(r)
    embed = hikari.Embed(title=data["title"], description="Uploaded to r/" + data["subreddit"] + " by " + data["author"], url=data["postLink"], color=comm.color())
    embed.set_image(data["url"])
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("numfact", "Pull a fact about a random number", aliases=["mathfact", "numberfact", "NUMFACT", "MATHFACT", "NUMBERFACT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def numfact(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "http://numbersapi.com/random/math?json"
    r = requests.request("GET", url).text
    data = json.loads(r)
    embed = hikari.Embed(title=str(data["number"]), description=data["text"], color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("yearfact", "Pull a fact about a random year", aliases=["YEARFACT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def yearfact(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "http://numbersapi.com/random/year?json"
    r = requests.request("GET", url).text
    data = json.loads(r)
    embed = hikari.Embed(title=str(data["number"]), description=data["text"], color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("datefact", "Pull a fact about a random date", aliases=["DATEFACT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def datefact(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "http://numbersapi.com/random/date?json"
    r = requests.request("GET", url).text
    data = json.loads(r)
    embed = hikari.Embed(title=str(data["year"]) + " #" + str(data["number"]), description=data["text"], color=comm.color())
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("inspirobot", "Generate a random inspirational quote", aliases=["INSPIROBOT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def inspirobot(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://inspirobot.me/api?generate=true"
    r = requests.request("GET", url).text
    embed = hikari.Embed(title="Inspirational Quote", description="", color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    embed.set_image(r)
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("text", "Text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("echo", "Repeats what you say", aliases=["parrot", "ECHO", "PARROT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def echo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.respond(ctx.options.text)

@plugin.command
@lightbulb.option("text", "text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("qr", "Generate a QR code", aliases=["qrcode", "QR", "QRCODE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def qr(ctx: lightbulb.Context):
    comm.log_com(ctx)
    embed = hikari.Embed(title="QR code", description=ctx.options.text, color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    embed.set_image(comm.url2uri("https://api.qrserver.com/v1/create-qr-code/?data=" + ctx.options.text))
    await ctx.respond(embed)

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
@lightbulb.command("cookie", "Shows the official count of cookies <@738772518441320460> has! And give them one more!", aliases=["cookies", "cookie_count", "COOKIE", "COOKIE_COUNT", "COOKIES"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def cookie(ctx: lightbulb.Context):
    comm.log_com(ctx)
    conmisc = sqlite3.connect("./db/misc.db")
    curmisc = conmisc.cursor()
    curmisc.execute("SELECT value FROM misc_vars WHERE key=?", ("cookies", ) )
    cookie_count, = curmisc.fetchone()
    conmisc.commit()
    await ctx.respond(":cookie: !!! <@738772518441320460>'s cookie count is now " + cookie_count + "!!! :cookie:")

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
