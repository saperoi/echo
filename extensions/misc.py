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
@lightbulb.option("text", "Text with the words that may or may not be in the bible.", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True, max_length=1000)
@lightbulb.option("bible", "The bible to pull from.", type=str, required=True, choices=["nasb", "kjv", "NASB", "KJV"])
@lightbulb.command("inbible", "ARE YOUR WORDS EVEN IN THE BIBLE?", aliases=["INBIBLE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def inbible(ctx: lightbulb.Context):
    comm.log_com(ctx)
    bibletext = open(f"./data/inbible/{ctx.options.bible.lower()}.txt", "r", encoding = "utf-8").read().splitlines()
    text = list(filter(None, re.sub(r"[^a-z0-9\- ]", " ", ctx.options.text.lower()).split(" ")))
    words_in = []
    incount = 0
    words_not = []
    for word in text:
        if word in bibletext:
            words_in.append(word)
            incount += 1
        else:
            words_not.append(word)
    embed = hikari.Embed(title=f"{(incount/len(text)*100):.1f}% of your words are in the bible", color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    if words_in != []:
        embed.add_field(name="**IN**", value=f"```diff\n+ {' '.join(words_in)}\n```")
    if words_not != []:
        embed.add_field(name="**NOT**", value=f"```diff\n- {' '.join(words_not)}\n```")
    await ctx.respond(embed)