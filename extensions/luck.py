import lightbulb
import comm
import math
import random

plugin = lightbulb.Plugin('luck', 'Test fate')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.option("bonus", "+/- bonus to add/subtract", type=int, required=False)
@lightbulb.option("dX", "Type of dice (e.g. 6 for d6, 20 for d20)")
@lightbulb.option("amount", "Amount of dice", type=int)
@lightbulb.set_help("Rolls a set amount of dice with some amount of sides. Example command: a//dice 2 d6 (the d is optional)")
@lightbulb.command("dice", "Rolls a dice")
@lightbulb.implements(lightbulb.PrefixCommand)
async def dice(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if list(str(ctx.options.dX))[0] == "d":
        dx = int(str(ctx.options.dX)[1:])
    else:
        dx = int(ctx.options.dX)
    rolls = []
    sum = 0
    for r in range(ctx.options.amount):
        _g = (random.randint(1, dx))
        sum += _g
        rolls.append(_g)
    mm = "You rolled " + str(ctx.options.amount) + " d" + str(dx) + " for a sum of **" + str(sum) + "**, with the following rolls: **" + str(rolls) + "**"
    if ctx.options.bonus != None:
        mm += "\nWith the bonus of " + str(ctx.options.bonus) + ", the resulting total is: **" + str(sum+ctx.options.bonus) +"**"
    await comm.send_msg(ctx,mm)

@dice.set_error_handler
async def dice_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("You did not provide enough arguments.\nThe command is structured like so: \t\t" + ctx.prefix + "dice <n> <dx>\n*<n>* is the amount of dice you want to roll.\t\t\t*<dx>* is the amount of faces on the die.")

@plugin.command
@lightbulb.add_cooldown(5, 1, lightbulb.UserBucket)
@lightbulb.set_help("Flips a coin, 1 in 6K chance of landing on its side.")
@lightbulb.command("coin", "Flips an American nickel")
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
    await comm.send_msg(ctx,random.choice(["Yes", "No", "Maybe :wink:", "I Honestly Have No Idea :neutral_face:", "Highly Unlikely", "Very Likely"]))

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
