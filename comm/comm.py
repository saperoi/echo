from datetime import datetime
from dataclasses import dataclass
from PIL import Image
import lightbulb
import hikari
import textwrap
import random
import codecs
import sqlite3
import requests
import base64
import json
import hashlib
import io
import re

bot_id = [1039988982253092926, 1045057369085841458]

conmisc = sqlite3.connect("./db/misc.db")
curmisc = conmisc.cursor()

with open("data/item_data.json", 'r', encoding = "utf-8") as file:
    item_data = json.load(file)
with open("data/name_data.json", 'r', encoding = "utf-8") as file:
    name_data = json.load(file)

@lightbulb.Check
def owners_only(ctx: lightbulb.Context) -> bool:
    return ctx.author.id in [738772518441320460]

def cookies_table():
    curmisc.execute("CREATE TABLE IF NOT EXISTS misc_vars(key TEXT, value TEXT)")

    curmisc.execute("SELECT * FROM misc_vars WHERE key=?", ("cookies",) )
    if curmisc.fetchall() == []:
        curmisc.execute("INSERT INTO misc_vars VALUES (?, ?)", ("cookies", "0") )
    conmisc.commit()

    curmisc.execute("SELECT value FROM misc_vars WHERE key=?", ("cookies", ) )
    cookie_count, = curmisc.fetchone()
    cookie_count = str(int(cookie_count) +1)
    curmisc.execute("UPDATE misc_vars SET value=? WHERE key=?", (cookie_count, "cookies") )
    conmisc.commit()

def log_com(ctx: lightbulb.Context):
    cookies_table()
    commlog = open("logs/" + str(ctx.guild_id) + ".txt", "a+", encoding="utf_16")
    ms = datetime.now().strftime("%H:%M:%S") + " : " + str(ctx.guild_id) + " : " + ctx.author.username + "#" + str(ctx.author.discriminator) +  " - " + str(ctx.author.id) + " : " + str(ctx.event.content).replace("\n", "\\n")
    print(ms)
    commlog.write(ms + "\n")
    commlog.close()

def user_id_check(u):
    if str(u).isnumeric():
        return int(u)
    elif type(u) == str:
        if u[0] == "<" and u[1] == "@" and u[-1] == ">":
            if str(u.replace('<', '').replace('>', '').replace('@', '')).isnumeric():
                return int(u.replace('<', '').replace('>', '').replace('@', ''))
            else:
                raise ValueError
        else:
            raise ValueError
    else:
        raise ValueError

async def send_msg(ctx: lightbulb.Context, txt: str):
    if len(txt) > 6000:
        await ctx.respond('Sorry, but this command has resulted in a response message exceeding a length of 6000 characters. To prevent abuse, this message has not been sent.')
    else:
        lines = textwrap.wrap(txt, 2000, break_long_words=False, replace_whitespace=False)
        for j in range(len(lines)):
            await ctx.respond(lines[j])

def rndm_name():
    return "".join([random.choice('azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890') for _ in range(10)])

def random_name(category = "deity"):
    global name_data
    if category == "anime":
        name_type = random.choices(["male", "neutral", "female"], weights = [0.33, 0.33, 0.34], k = 1)[0]
        random_3 = random.choice(name_data["anime"]["pt5"])
        random_4 = random.choice(name_data["anime"]["pt6"])
        if name_type == "male":
            random_1 = random.choice(name_data["anime"]["pt3"])
            random_2 = random.choice(name_data["anime"]["pt4"])
            return random_1 + random_2 + " " + random_3 + random_4
        elif name_type == "neutral":
            random_1 = random.choice(name_data["anime"]["pt7"])
            random_2 = random.choice(name_data["anime"]["pt8"])
            return random_1 + random_2 + " " + random_3 + random_4
        else:
            random_1 = random.choice(name_data["anime"]["pt1"])
            random_2 = random.choice(name_data["anime"]["pt2"])
            return random_1 + random_2 + " " + random_3 + random_4
    elif category == "deity":
        name_type = random.choices(["male", "neutral", "female"], weights = [0.33, 0.33, 0.34], k = 1)[0]
        random_2 = random.choice(name_data["deity"]["pt2"])
        random_3 = random.choice(name_data["deity"]["pt3"])
        if name_type == "male":
            random_1 = random.choice(name_data["deity"]["pt1"])
            random_5 = random.choice(name_data["deity"]["pt5"])
            return random_1 + random_2 + random_3 + random_5
        elif name_type == "neutral":
            random_1 = random.choice(name_data["deity"]["pt1b"])
            random_4 = random.choice(name_data["deity"]["pt6"])
            return random_1 + random_2 + random_3 + random_4
        else:
            random_1 = random.choice(name_data["deity"]["pt1a"])
            random_4 = random.choice(name_data["deity"]["pt4"])
            return random_1 + random_2 + random_3 + random_4

def random_rarity():
    global item_data
    rarity = random.choices(item_data["rarity"], weights = [0.5, 0.25, 0.15, 0.05, 0.02, 0.02, 0.01], k = 1)[0]
    return rarity.upper()

def random_material(rarity = "common"):
    global item_data
    material = random.choice(item_data["materials"][rarity.lower()])
    return material.title()

def random_item_type(rarity = "common"):
    global item_data
    item_type = random.choice(item_data["weapons"][rarity.lower()])
    return item_type.title()

# https://stackoverflow.com/questions/35772848/python-retrieve-a-file-from-url-and-generate-data-uri
def url2uri(url):
    response = requests.get(url)
    content_type = response.headers["content-type"]
    encoded_body = base64.b64encode(response.content)
    return "data:{};base64,{}".format(content_type, encoded_body.decode())

# https://stackoverflow.com/questions/60676893/converting-pil-pillow-image-to-data-url
def pillow_image_to_base64_string(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
def url2pil(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    return img

def color():
    return random.randint(0x0, 0xffffff)

async def webhook_send(ctx: lightbulb.Context, user, content):
    member = await ctx.app.rest.fetch_member(ctx.guild_id, user)
    if ctx.channel_id == None:
        await send_msg(ctx, content)
    elif isinstance(ctx.get_channel(), hikari.GuildThreadChannel):
        hook = await ctx.app.rest.create_webhook(channel=ctx.get_channel().parent_id, name="ECHO: " + str(member.id), avatar=member.display_avatar_url)
        await ctx.app.rest.execute_webhook(webhook=hook.webhook_id, token=hook.token, content=content, username=member.display_name if ctx.author.id == user else "\"" + member.display_name + "\"", thread=ctx.channel_id)
    else:
        hook = await ctx.app.rest.create_webhook(channel=ctx.channel_id, name="ECHO: " + str(member.id), avatar=member.display_avatar_url)
        await hook.execute(content=content, username=member.display_name if ctx.author.id == user else "\"" + member.display_name + "\"")
    await hook.delete()

async def plurality_webhook_send(ctx: lightbulb.Context, user, content):
    name = {"letterbot": "LetterBot"}[user]
    with Image.open({"letterbot": "./data/img/letterbot.jpg"}[user]) as im:
        avatar = 'data:image/jpeg;base64,' + pillow_image_to_base64_string(im)
    if ctx.channel_id == None:
        await send_msg(ctx, content)
    elif isinstance(ctx.get_channel(), hikari.GuildThreadChannel):
        hook = await ctx.app.rest.create_webhook(channel=ctx.get_channel().parent_id, name="ECHO HEADMATE: " + name, avatar=avatar)
        await ctx.app.rest.execute_webhook(webhook=hook.webhook_id, token=hook.token, content=content, username=name, thread=ctx.channel_id)
    else:
        hook = await ctx.app.rest.create_webhook(channel=ctx.channel_id, name="ECHO HEADMATE: " + name, avatar=avatar)
        await ctx.app.rest.execute_webhook(webhook=hook.webhook_id, token=hook.token, content=content, username=name)
    await hook.delete()

def texthasher(text):
    return int(hashlib.sha256(str(text).encode('utf-8')).hexdigest(), 16)

def clean(inputstring):
    return re.sub(r'[^a-zA-Z0-9_ ]', '', inputstring)