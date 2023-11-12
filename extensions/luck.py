import lightbulb
import comm
import math
import random
import itertools

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
@lightbulb.command("dice", "Rolls a dice", aliases=["roll"])
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
        await event.context.respond("You did not provide enough arguments.\nThe command is structured like so: \t\t" + ctx.prefix + "dice <n> <dx>\n*<n>* is the amount of dice you want to roll.\t\t\t*<dx>* is the amount of faces on the die.")

@plugin.command
@lightbulb.add_cooldown(5, 1, lightbulb.UserBucket)
@lightbulb.set_help("Flips a coin, 1 in 6K chance of landing on its side.")
@lightbulb.command("coin", "Flips an American nickel", aliases=["flip"])
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
@lightbulb.command("8ball", "See the fortune")
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

@eightball.set_error_handler
async def eightball_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("You did not ask me a question!")

@plugin.command
@lightbulb.option("shoe", "Your hand", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("You can only throw 'rock', 'paper', or 'scissors'")
@lightbulb.command("rps", "ROCK, PAPER, SCISSORS")
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
@lightbulb.command("rtg", "Random text generator")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def rtg(ctx: lightbulb.Context):
    comm.log_com(ctx)

@rtg.child
@lightbulb.option("who", "Who to determine the classpect of", type=str, required=True)
@lightbulb.set_help("HOMESTUCK SBURB Classpects")
@lightbulb.command("classpect", "HOMESTUCK SBURB Classpects")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def classpect(ctx: lightbulb.Context):
    comm.log_com(ctx)
    classes =  ["Knight", "Prince", "Thief", "Mage", "Witch", "Maid", "Page", "Bard", "Rogue", "Seer", "Heir", "Sylph"]
    aspects = ["Space", "Time", "Mind", "Heart", "Hope", "Rage", "Breath", "Blood", "Life", "Doom", "Light", "Void"]
    classp = list(itertools.product(classes,aspects))
    random.seed(comm.texthasher(ctx.options.who))
    classp = random.choice(classp)
    classpects = classp[0] + " of " + classp[1]
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I am a " + classpects)
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " is a " + classpects)
    else:
        await comm.send_msg(ctx, ctx.options.who + " is a " + classpects)

@rtg.child
@lightbulb.option("who", "Who to put on the twunkscale", type=str, required=True)
@lightbulb.set_help("Rates on the Twink-Hunk-Bear Scale")
@lightbulb.command("twunkscale", "Rates on the Twink-Hunk-Bear Scale")
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
@lightbulb.option("who", "Who to put on the futchscale", type=str, required=True)
@lightbulb.set_help("Rates on the Femme-Butch Scale")
@lightbulb.command("futchscale", "Rates on the Femme-Butch Scale")
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
@lightbulb.option("who", "Who to S/P", type=str, required=True)
@lightbulb.set_help("Pass, Smass or Smash someone")
@lightbulb.command("smash_or_pass", "Pass, Smass or Smash someone", aliases=["sop"])
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
@lightbulb.option("who", "Who to measure", type=str, required=True)
@lightbulb.set_help("Measure someone's sussiness")
@lightbulb.command("susmeter", "Measure someone's sussiness")
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
@lightbulb.option("who", "Who to measure", type=str, required=True)
@lightbulb.set_help("Measure someone's waifuness")
@lightbulb.command("ratewaifu", "Measure someone's waifuness")
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
@lightbulb.option("who", "Who to measure", type=str, required=True)
@lightbulb.set_help("Measure someone's PP")
@lightbulb.command("ppmeter", "Measure someone's PP")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def ppmeter(ctx: lightbulb.Context):
    comm.log_com(ctx)
    pp = "c" + "".join("=" for _ in range(random.randint(0,15))) + "3"
    if ctx.options.who in ["you", "You", "YOU"]:
        await ctx.respond("I have a: " + pp)
    elif ctx.options.who in ["me", "Me", "I", "ME"]:
        await ctx.respond(ctx.author.mention + " has a: " + pp)
    else:
        await comm.send_msg(ctx, ctx.options.who + " has a: " + pp)
