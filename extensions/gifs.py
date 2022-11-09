import lightbulb
import comm
import hikari
import random
import requests

plugin = lightbulb.Plugin('gifs', 'Basically UwU bot but worse')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.set_error_handler
async def gifs_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.option("user", "The user to kill.", required=True)
@lightbulb.command("kill", "Kill 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def kill(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    embed = hikari.Embed(title="FATALITY!", description="<@" + str(ctx.author.id) + "> killed <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.gkill))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to slap.", required=True)
@lightbulb.command("slap", "Slap 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def slap(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    embed = hikari.Embed(title="Splapp!", description="<@" + str(ctx.author.id) + "> slapped <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.gslap))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to bonk.", required=True)
@lightbulb.command("bonk", "bonk 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def example(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    embed = hikari.Embed(title="BONK!", description="<@" + str(ctx.author.id) + "> bonked <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.gbonk))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to boop.", required=True)
@lightbulb.command("boop", "Boop 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def boop(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    embed = hikari.Embed(title="boop!", description="<@" + str(ctx.author.id) + "> booped <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.gboop))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to pass the jonko to.", required=True)
@lightbulb.command("boof", "Pass it to 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def boof(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    embed = hikari.Embed(title="¿Quieres?", description="<@" + str(ctx.author.id) + "> passed it to <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.gboof))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to bark at.", required=True)
@lightbulb.command("bark", "Bark at 'em", aliases=["woof"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def bark(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    embed = hikari.Embed(title="WOOF WOOF!", description="<@" + str(ctx.author.id) + "> barked at <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.gbark))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to pat.", required=True)
@lightbulb.command("pat", "Pat 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def pat(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    embed = hikari.Embed(title="Pat pat!", description="<@" + str(ctx.author.id) + "> patted <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.gpat))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to wag at.", required=True)
@lightbulb.command("wag", "Wag at 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def wag(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    comm.g = ["", "", ""]
    embed = hikari.Embed(title="Wag!", description="<@" + str(ctx.author.id) + "> wagged their tail at <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.gwag))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to hug.", required=True)
@lightbulb.command("hug", "Hug 'em")
@lightbulb.implements(lightbulb.PrefixCommand)
async def hug(ctx: lightbulb.Context):
    comm.log_com(ctx)
    u = comm.user_id_check(ctx.options.user)
    embed = hikari.Embed(title="Hug!", description="<@" + str(ctx.author.id) + "> hugged <@" + str(u) + ">", color=random.randint(0x0, 0xffffff))
    embed.set_image(random.choice(comm.ghug))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("floof", "floofy :)")
@lightbulb.implements(lightbulb.PrefixCommand)
async def floofy(ctx: lightbulb.Context):
    comm.log_com(ctx)
    response = requests.get("https://randomfox.ca/floof").json()
    embed = hikari.Embed(title = "Floofy!")
    embed.set_image(response["image"])
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("doggo", "pupper :)")
@lightbulb.implements(lightbulb.PrefixCommand)
async def doggo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    response = requests.get("https://random.dog/woof.json").json()
    embed = hikari.Embed(title = "Woof Woof!!")
    embed.set_image(response["url"])
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("ducky", "quack :)")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ducky(ctx: lightbulb.Context):
    comm.log_com(ctx)
    response = requests.get("https://random-d.uk/api/v2/random").json()
    embed = hikari.Embed(title = "Quackity Quack!!")
    embed.set_image(response["url"])
    await ctx.respond(embed)
