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

"""
url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

querystring = {"term":"wat"}

headers = {
    "X-RapidAPI-Key": "1e8d7c0b8cmsh5be7f5eadc26662p1919bfjsn1850caabedb4",
    "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

data = json.loads(response.text)

print(data["list"][0]["definition"].replace("[","").replace("]",""))
"""
