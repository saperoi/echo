import lightbulb
import hikari
import comm
import json
import requests
from dotenv import load_dotenv, find_dotenv
import os

plugin = lightbulb.Plugin('misc', "I've no clue where else to put these")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.option("word", "The word to search for.", type=str, required=True)
@lightbulb.command("urban", "Look up a word on Urban Dictionary")
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
@lightbulb.command("dict", "Look up a word on DictionaryAPI.dev")
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
@lightbulb.option("sentence", "Sentence to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=True)
@lightbulb.command("echo", "Repeats what you say", aliases=["parrot"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def echo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.respond(ctx.options.sentence)
