import lightbulb
import hikari
import comm
import json
import requests
from dotenv import load_dotenv, find_dotenv
import os
import random
import sqlite3

plugin = lightbulb.Plugin('misc', "I've no clue where else to put these")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.option("word", "The word to search for.", type=str, required=True)
@lightbulb.command("urban", "Look up a word on Urban Dictionary")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
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
@lightbulb.command("dict", "Look up a word on DictionaryAPI.dev")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
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
@lightbulb.command("xkcd", "Look up an XKCD comic")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
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
    embed = hikari.Embed(title=data["title"] + " [#" + str(data["num"]) + "]", description=data["alt"], color=random.randint(0x0, 0xffffff))
    embed.set_image(data["img"])
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("meme", "Pull a random meme")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def meme(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://meme-api.com/gimme"
    r = requests.request("GET", url).text
    data = json.loads(r)
    embed = hikari.Embed(title=data["title"], description="Uploaded to r/" + data["subreddit"] + " by " + data["author"], url=data["postLink"], color=random.randint(0x0, 0xffffff))
    embed.set_image(data["url"])
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("sentence", "Sentence to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("echo", "Repeats what you say", aliases=["parrot"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.respond(ctx.options.sentence)

@plugin.command
@lightbulb.option("sentence", "Sentence to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("emojify", "Repeats what you say", aliases=["emoji_echo"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def emojify(ctx: lightbulb.Context):
    comm.log_com(ctx)
    s = list(ctx.options.sentence)
    for i in range(len(s)):
        if s[i] in "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN":
            s[i] = ":regional_indicator_" + s[i].lower() + ":"
        elif s[i] in " !?1234567890":
            s[i] = {" ": "     ", "!": ":exclamation", "?": ":question:", "1": ":one:", "2": ":two:", "3": ":three:", "4": ":four:", "5": ":five:", "6": ":six:", "7": ":seven:", "8": ":eight:", "9": ":nine:", "0": ":zero:"}[s[i]]
    await ctx.respond(''.join(s))
    cprmid = await ctx.previous_response.message()
    cprmid = cprmid.id
    await ctx.respond("Sent by: " + ctx.author.mention, reply=cprmid)
    if str(type(ctx.event)) == "<class 'hikari.events.message_events.GuildMessageCreateEvent'>":
        await ctx.app.rest.delete_message(ctx.event.message.channel_id, ctx.event.message.id)

@plugin.command
@lightbulb.command("cookie", "Shows the official count of cookies <@738772518441320460> has! And give them one more!", aliases=["cookies", "cookie_count"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cookie(ctx: lightbulb.Context):
    comm.log_com(ctx)
    conmisc = sqlite3.connect("./db/misc.db")
    curmisc = conmisc.cursor()
    curmisc.execute("SELECT value FROM misc_vars WHERE key=?", ("cookies", ) )
    cookie_count, = curmisc.fetchone()
    conmisc.commit()
    await ctx.respond(":cookie: !!! <@738772518441320460>'s cookie count is now " + cookie_count + "!!! :cookie:")
