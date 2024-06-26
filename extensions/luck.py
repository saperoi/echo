import lightbulb
import hikari
import comm
import math
import random
import itertools
import datetime as dt
from PIL import Image

plugin = lightbulb.Plugin('luck', 'Test fate')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.option("bonus", "+/- bonus to add/subtract", type=int, required=False)
@lightbulb.option("dx", "Type of dice (e.g. 6 for d6, 20 for d20)")
@lightbulb.option("amount", "Amount of dice", type=int)
@lightbulb.set_help("Rolls a set amount of dice with some amount of sides. Example command: a//dice 2 d6 (the d is optional)")
@lightbulb.command("dice", "Rolls a dice", aliases=["roll", "DICE", "ROLL"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def dice(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if list(str(ctx.options.dx))[0] == "d":
        dx = int(str(ctx.options.dx)[1:])
    else:
        dx = int(ctx.options.dx)
    rolls = []
    sum = 0
    for r in range(ctx.options.amount):
        _g = (random.randint(1, dx))
        sum += _g
        rolls.append(_g)
    if dx == 6:
        dice_unicode = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
        rolls = [dice_unicode[x] for x in rolls]
    mm = "You rolled " + str(ctx.options.amount) + " d" + str(dx) + " for a sum of **" + str(sum) + "**, with the following rolls: **" + str(rolls) + "**"
    if ctx.options.bonus != None:
        mm += "\nWith the bonus of " + str(ctx.options.bonus) + ", the resulting total is: **" + str(sum+ctx.options.bonus) +"**"
    mm +="\nLowest: " + str(min(rolls)) + "\t\tHighest: " + str(max(rolls))
    await comm.send_msg(ctx,mm)

@dice.set_error_handler
async def dice_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("You did not provide enough arguments.\nThe command is structured like so: \t\t" + event.context.prefix + "dice <n> <dx>\n*<n>* is the amount of dice you want to roll.\t\t\t*<dx>* is the amount of faces on the die.")

@plugin.command
@lightbulb.add_cooldown(5, 1, lightbulb.UserBucket)
@lightbulb.set_help("Flips a coin, 1 in 6K chance of landing on its side.")
@lightbulb.command("coin", "Flips an American nickel", aliases=["flip", "COIN", "FLIP"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def coin(ctx: lightbulb.Context):
    comm.log_com(ctx)
    r = random.randint(0,6000)
    if 0 <= r <= 2999:
        await comm.send_msg(ctx,"H!   The coin landed **heads** up.")
    elif 3000 <= r <= 5999:
        await comm.send_msg(ctx,"T!   The coin landed **tails** up.")
    elif r == 6000:
        await comm.send_msg(ctx,"S?   The coin landed ON ITS SIDE.")
    else:
        await comm.send_msg(ctx,"!!   Something has gone wrong.")

@plugin.command
@lightbulb.option("question", "Your question")
@lightbulb.command("8ball", "See the fortune", aliases=["eightball", "8BALL", "EIGHTBALL"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def eightball(ctx: lightbulb.Context):
    comm.log_com(ctx)
    ball = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don’t count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
    ]

    await comm.send_msg(ctx,random.choice(ball))

@plugin.command
@lightbulb.option("question", "Your question")
@lightbulb.command("3ball", "See the fortune", aliases=["shitty8ball", "SHITTY8BALL", "3BALL", "threeball", "THREEBALL"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def threeball(ctx: lightbulb.Context):
    comm.log_com(ctx)
    ball = [
        "Of course.",
        "No shit, Sherlock.",
        "A hundred percent, bestie.",
        "Yeah, for sure, bud.",
        "Mhm.",
        "Hell yeah!!!",
        "Probably.",
        "Ehhh...",
        "Ask a higher power at this point.",
        "Sure??? I guess???",
        "I can't even begin to explain.",
        "Fucked up if true.",
        "Of course not!",
        "Nope. Not at all",
        "NO!!!",
        "No! Absolutely not! Go to hell!",
        "In your dreams.",
        "Never in a million years.",
        "What.",
        "I'm biting you for that one."
    ]

    await comm.send_msg(ctx,random.choice(ball))

@threeball.set_error_handler
async def threeball_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("You did not ask me a question!")

@plugin.command
@lightbulb.option("shoe", "Your hand", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("You can only throw 'rock', 'paper', or 'scissors'")
@lightbulb.command("rps", "ROCK, PAPER, SCISSORS", aliases=["RPS"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def rps(ctx: lightbulb.Context):
    comm.log_com(ctx)
    ms = ""
    shot = ctx.options.shoe
    shot = shot.lower()
    if shot not in ['rock', 'paper', 'scissors']:
        raise ValueError('Argument is not allowed')
    if shot == "rock":
        ms += "You threw **rock** 🪨\n\n"
    elif shot == "paper":
        ms += "You threw **paper** 📄\n\n"
    elif shot == "scissors":
        ms += "You threw **scissors** ✂️\n\n"
    r = ["rock","paper","scissors"][math.floor(3*(random.random()-0.1))]
    if r == "rock":
        ms += "I threw **rock** 🪨\n"
    elif r == "paper":
        ms += "I threw **paper** 📄\n"
    elif r == "scissors":
        ms += "I threw **scissors** ✂️\n"
    wins = [('rock','scissors'),('paper','rock'),('scissors','paper')]
    loses = [('rock','paper'),('paper','scissors'),('scissors','rock')]
    ties = [('rock','rock'),('paper','paper'),('scissors','scissors')]
    if (r,shot) in ties:
        ms += "It's a tie!"
    elif (r,shot) in loses:
        ms += "I lost? :("
    elif (r,shot) in wins:
        ms += "LET'S GO! I WON! OH YEAH"
    await comm.send_msg(ctx,ms)

@rps.set_error_handler
async def rps_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("You did not provide enough arguments.\nThe command is structured like so: \t\t" + ctx.prefix + "rps <shoe> \n*<shoe>* is what you want to throw up. It must be either 'rock', 'paper' or 'scissors'")
    if isinstance(exception, ValueError):
        await event.context.respond("You are not allowed to use that as your hand. It must either be 'rock', 'paper' or 'scissors'")

@plugin.command
@lightbulb.set_help("Existing commands:\n- dndalign - D&D Alignment\n- twunkscale - Rates on the Twink-Hunk-Bear Scale\n- smash_or_pass - Pass, Smass or Smash someone")
@lightbulb.command("rtg", "Random text generator", aliases=["RTG"])
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def rtg(ctx: lightbulb.Context):
    comm.log_com(ctx)

@rtg.child
@lightbulb.option("range", "Year range", type=str, default="100", choices=["1k", "1K", "200", "100", "fut", "FUT", "911"])
@lightbulb.set_help("Generate a random date. You can write after the function 1k (for between 1000 and 3000), 200 (for between 1800 and 2200), 100 (for between 1900 and 2100), or fut (for between now and 2100). Defaults to 100")
@lightbulb.command("date", "Random date", aliases=["DATE"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def date(ctx: lightbulb.Context):
    comm.log_com(ctx)
    year1, year2 = {"1k": (1000, 3000), "200": (1800, 2200), "100": (1900, 2100), "fut": (dt.datetime.now().year, 2100), "911": (2001, 2001)}[ctx.options.range.lower()]
    d1 = dt.datetime.strptime(f"1/1/{year1}", '%d/%m/%Y')
    d2 = dt.datetime.strptime(f"31/12/{year2}", '%d/%m/%Y')
    if ctx.options.range.lower() == "fut":
        d1 = dt.datetime.now()
    diff = d2 - d1
    date = (d1 + dt.timedelta(days=random.randrange(diff.days))).strftime("%d %B %Y")
    if ctx.options.range == "911":
        date = "9 September 2001"
    if date == "9 September 2001":
        with Image.open("./data/img/yuri911.jpg") as im:
            data_url = 'data:image/png;base64,' + comm.pillow_image_to_base64_string(im)
        embed = hikari.Embed(title="9/11", color=comm.color())
        embed.set_image(data_url)
        embed.set_footer("Ordered by: " + str(ctx.author))
        await ctx.respond(embed)
    else:
        await ctx.respond(date)

@rtg.child
@lightbulb.option("who", "Who to determine the classpect of", type=str, required=True, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("HOMESTUCK SBURB Classpects")
@lightbulb.command("classpect", "HOMESTUCK SBURB Classpects", aliases=["CLASSPECT"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def classpect(ctx: lightbulb.Context):
    comm.log_com(ctx)
    sway = ["Derse", "Prospit"]
    classes =  ["Knight", "Prince", "Thief", "Mage", "Witch", "Maid", "Page", "Bard", "Rogue", "Seer", "Heir", "Sylph"]
    aspects = ["Space", "Time", "Mind", "Heart", "Hope", "Rage", "Breath", "Blood", "Life", "Doom", "Light", "Void"]
    classp = list(itertools.product(sway,classes,aspects))
    random.seed(comm.texthasher(ctx.options.who))
    classp = random.choice(classp)
    classpects = classp[0] + " " + classp[1] + " of " + classp[2]
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I am a " + classpects)
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " is a " + classpects)
    else:
        await comm.send_msg(ctx, ctx.options.who + " is a " + classpects)

@rtg.child
@lightbulb.option("who", "Who to determine the alignment of", type=str, required=True, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("D&D Alignments")
@lightbulb.command("dndalign", "D&D Alignments", aliases=["DNDALIGN"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def dndalign(ctx: lightbulb.Context):
    comm.log_com(ctx)
    ethos = ["Lawful", "Neutral", "Chaotic"]
    moral = ["Good", "Neutral", "Evil"]
    align = list(itertools.product(ethos,moral))
    random.seed(comm.texthasher(ctx.options.who))
    align = random.choice(align)
    alignment = align[0] + " " + align[1]
    if alignment == "Neutral Neutral":
        alignment = "True Neutral"
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I am a " + alignment)
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " is a " + alignment)
    else:
        await comm.send_msg(ctx, ctx.options.who + " is a " + alignment)

@rtg.child
@lightbulb.option("who", "Who to put on the twunkscale", type=str, required=True, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("Rates on the Twink-Hunk-Bear Scale")
@lightbulb.command("twunkscale", "Rates on the Twink-Hunk-Bear Scale", aliases=["TWUNKSCALE"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def twunkscale(ctx: lightbulb.Context):
    comm.log_com(ctx)
    arr = ["Twink", "Twinkish", "Hunkish Twink", "Twunk", "Twinkish Hunk", "Hunkish", "Hunk", "Bearish Twink", "Cub", "No Leaning", "Bunk", "Bearish Hunk", "Twinkish Bear", "Bearish", "Hunkish Bear", "Bear"]
    random.seed(comm.texthasher(ctx.options.who))
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I am a " + random.choice(arr))
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " is a " + random.choice(arr))
    else:
        await comm.send_msg(ctx, ctx.options.who + " is a " + random.choice(arr))

@rtg.child
@lightbulb.option("who", "Who to put on the futchscale", type=str, required=True, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("Rates on the Femme-Butch Scale")
@lightbulb.command("futchscale", "Rates on the Femme-Butch Scale", aliases=["FUTCHSCALE"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def futchscale(ctx: lightbulb.Context):
    comm.log_com(ctx)
    arr = ["High Femme", "Femme", "Butchy Femme", "Futch", "Soft Butch", "Butch", "Stone Butch"]
    random.seed(comm.texthasher(ctx.options.who))
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I am a " + random.choice(arr))
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " is a " + random.choice(arr))
    else:
        await comm.send_msg(ctx, ctx.options.who + " is a " + random.choice(arr))

@rtg.child
@lightbulb.option("who", "Who to S/P", type=str, required=True, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("Pass, Smass or Smash someone")
@lightbulb.command("smash_or_pass", "Pass, Smass or Smash someone", aliases=["sop", "SMASH_OR_PASS", "SOP"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def smash_or_pass(ctx: lightbulb.Context):
    comm.log_com(ctx)
    arr = ["Smash", "Pass", "Smass"]
    random.seed(comm.texthasher(ctx.options.who))
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I would " + random.choice(arr) + " myself")
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond("I would " + random.choice(arr) + " " + ctx.author.mention)
    else:
        await comm.send_msg(ctx, "I would " + random.choice(arr) + " " + ctx.options.who)

@rtg.child
@lightbulb.option("who", "Who to measure", type=str, required=True, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("Measure someone's sussiness")
@lightbulb.command("susmeter", "Measure someone's sussiness", aliases=["SUSMETER"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def susmeter(ctx: lightbulb.Context):
    comm.log_com(ctx)
    random.seed(comm.texthasher(ctx.options.who))
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I am " + str(random.randint(0,101)) + "% sus.")
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " is " + str(random.randint(0,100)) + "% sus.")
    else:
        await comm.send_msg(ctx, ctx.options.who + " is " + str(random.randint(0,100)) + "% sus.")

@rtg.child
@lightbulb.option("who", "Who to measure", type=str, required=True, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("Measure someone's waifuness")
@lightbulb.command("ratewaifu", "Measure someone's waifuness", aliases=["waifu", "RATEWAIFU", "WAIFU"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def ratewaifu(ctx: lightbulb.Context):
    comm.log_com(ctx)
    random.seed(comm.texthasher(ctx.options.who))
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I am " + str(random.randint(0,100)) + "% waifu.")
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " is " + str(random.randint(0,100)) + "% waifu.")
    else:
        await comm.send_msg(ctx, ctx.options.who + " is " + str(random.randint(0,100)) + "% waifu.")

@rtg.child
@lightbulb.option("who", "Who to measure", type=str, required=True, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("Measure someone's PP")
@lightbulb.command("ppmeter", "Measure someone's PP", aliases=["PPMETER"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def ppmeter(ctx: lightbulb.Context):
    comm.log_com(ctx)
    random.seed(comm.texthasher(ctx.options.who))
    pp = "c" + "".join("=" for _ in range(random.randint(0,15))) + "3"
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I have a: " + pp)
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " has a: " + pp)
    else:
        await comm.send_msg(ctx, ctx.options.who + " has a: " + pp)
