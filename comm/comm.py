from datetime import datetime
import lightbulb
import hikari
import textwrap
import random

def log_com(ctx: lightbulb.Context):
    commlog = open("log.txt", "a")
    ms = datetime.now().strftime("%H:%M:%S") + " : " + str(ctx.guild_id) + " : " + ctx.author.username + "#" + str(ctx.author.discriminator) + " - " + str(ctx.author.id) + " : " + str(ctx.event.content)
    print(ms)
    commlog.write(ms + "\n")
    commlog.close()

def user_id_check(u):
    if str(u).isnumeric():
        return int(u)
    elif type(u) == str:
        if u[0] == "<" and u[1] == "@" and u[-1] == ">":
            return int(u.replace('<', '').replace('>', '').replace('@', ''))
        else:
            raise ValueError
    else:
        raise ValueError

async def send_msg(ctx: lightbulb.Context, txt: str):
    if len(txt) > 6000:
        await ctx.respond('Sorry, but this command has resulted in a response message exceeding a length of 6000 characters. To prevent abuse, this message has not been sent.')
    else:
        lines = textwrap.wrap(txt, 2000, break_long_words=False)
        for i in range(len(lines)):
            await ctx.respond(lines[i])

def rndm_name():
    chars = [random.choice('azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890') for _ in range(10)]
    name = ""
    for i in range(len(chars)):
        name += chars[i]
    return name

def rai(arr:list): #Random Array Item
    n = random.randint(0, len(arr))
    return arr[n]

rarity = ["[Common]", "[UNCOMMON]", "[RARE]", "[EPIC]", "[LEGENDARY]", "[MYTHIC]"]

mats0 = ["Copper","Bronze","Steel","Iron","Gold"]
mats1 = ["Diamond","Crystal"]
mats2 = ["Carbon","Damascus Steel"]
mats3 = ["Adamantite","Cobaltite","Perovskite","Millerite"]
mats4 = ["Uraninite","Scarletite","Mythril","Oricalchum"]
mats5 = ["Dark Matter","Unobtanium"]

weapons = [
"Scythe",
"Sword", "Longsword", "Sabre", "Rapier", "Dagger", "Khatana", "Claymore", "Spatha", "Cutlass", "Scimitar", "Gladius", "Falchion", "Katana", "Cleaver", "Machete", "Greatsword", "Kunai",
"Axe", "Battleaxe", "Hatchet", "Handaxe", "Mattock", "Sagaris", "Broadaxe", "Double Axe",
"Spear", "Shortspear", "Trident", "Spetum", "Pike", "Halberd", "Lance", "Sceptre", "Staff", "Javelin", "Glaive",
"Hammer",
"Mace", "Battle Mace", "Pegged Mace", "Spiked Mace"
]

def rndm_mat():
    m = random.randint(1,21)
    if 1 <= m <= 6:
        mat = random.choice(mats0)
    elif 7 <= m <= 11:
        mat = random.choice(mats1)
    elif 12  <= m <= 15:
        mat = random.choice(mats2)
    elif 16 <= m <= 18:
        mat = random.choice(mats3)
    elif 19 <= m <= 20:
        mat = random.choice(mats4)
    elif 21 <= m <= 21:
        mat = random.choice(mats5)
    return m, mat

def rndm_rar(q):
    m = random.randint(q,21)
    if 1 <= m <= 6:
        n = 0
    elif 7 <= m <= 11:
        n = 1
    elif 12  <= m <= 15:
        n = 2
    elif 16 <= m <= 18:
        n = 3
    elif 19 <= m <= 20:
        n = 4
    elif 21 <= m <= 21:
        n = 5
    return rarity[n]
