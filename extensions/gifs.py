import lightbulb
import comm
import hikari
import random
import requests
import json

plugin = lightbulb.Plugin('gifs', 'Basically UwU bot but worse')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

f = open("./data/gifs.json", "r", encoding = "utf-8")
urls = json.load(f)

@plugin.set_error_handler
async def gifs_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, ValueError):
        await event.context.respond("You did not provide a user (ID)")
    elif isinstance(exception, hikari.errors.NotFoundError):
        await event.context.respond("This user does not EXIST")

@plugin.command
@lightbulb.option("user", "The user to kill.", required=True)
@lightbulb.command("kill", "Kill 'em", aliases=["KILL"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def kill(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="FATALITY!", description="<@" + str(ctx.author.id) + "> killed " + u, color=comm.color())
    embed.set_image(random.choice(urls["kill"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to slap.", required=True)
@lightbulb.command("slap", "Slap 'em", aliases=["SLAP"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def slap(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="Splapp!", description="<@" + str(ctx.author.id) + "> slapped " + u, color=comm.color())
    embed.set_image(random.choice(urls["slap"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to bonk.", required=True)
@lightbulb.command("bonk", "bonk 'em", aliases=["BONK"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def bonk(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="BONK!", description="<@" + str(ctx.author.id) + "> bonked " + u, color=comm.color())
    embed.set_image(random.choice(urls["bonk"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to bonk and send to jail.", required=True)
@lightbulb.command("hbonk", "bonk 'em and send 'em to horny jail", aliases=["HBONK"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def hbonk(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="BONK!", description="<@" + str(ctx.author.id) + "> bonked <@" + u + "> and sent them to horny jail!", color=comm.color())
    embed.set_image(random.choice(urls["hbonk"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to boop.", required=True)
@lightbulb.command("boop", "Boop 'em", aliases=["BOOP"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def boop(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="boop!", description="<@" + str(ctx.author.id) + "> booped " + u, color=comm.color())
    embed.set_image(random.choice(urls["boop"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to pass the jonko to.", required=True)
@lightbulb.command("boof", "Pass it to 'em", aliases=["BOOF"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def boof(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="¿Quieres?", description="<@" + str(ctx.author.id) + "> passed it to " + u, color=comm.color())
    embed.set_image(random.choice(urls["boof"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to pat.", required=True)
@lightbulb.command("pat", "Pat 'em", aliases=["PAT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def pat(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="Pat pat!", description="<@" + str(ctx.author.id) + "> patted " + u, color=comm.color())
    embed.set_image(random.choice(urls["pat"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to hug.", required=True)
@lightbulb.command("hug", "Hug 'em", aliases=["HUG"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def hug(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="Hug!", description="<@" + str(ctx.author.id) + "> hugged " + u, color=comm.color())
    embed.set_image(random.choice(urls["hug"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to cuddle.", required=True)
@lightbulb.command("cuddle", "Cuddle with 'em", aliases=["CUDDLE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def cuddle(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="Cuddle!", description="<@" + str(ctx.author.id) + "> cuddled with " + u, color=comm.color())
    embed.set_image(random.choice(urls["cuddle"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to tickle.", required=True)
@lightbulb.command("tickle", "Tickle 'em", aliases=["TICKLE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def tickle(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="TICKLE MONSTER!", description="<@" + str(ctx.author.id) + "> tickled " + u, color=comm.color())
    embed.set_image(random.choice(urls["tickle"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to kiss.", required=True)
@lightbulb.command("kiss", "Kiss 'em", aliases=["smooch", "KISS", "SMOOCH"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def kiss(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="MMWAHH!", description="<@" + str(ctx.author.id) + "> smooched " + u, color=comm.color())
    embed.set_image(random.choice(urls["kiss"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to give a cookie.", required=True)
@lightbulb.command("give_cookie", "Give 'em a cookie", aliases=["GIVE_COOKIE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def give_cookie(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title=":cookie: COOKIES!!! :cookie:", description="<@" + str(ctx.author.id) + "> gave <@" + u + "> a cookie!", color=comm.color())
    embed.set_image(random.choice(urls["cookie"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to dap up.", required=True)
@lightbulb.command("handshake", "Give 'em a good handshake", aliases=["HANDSHAKE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def handshake(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="Dap me up", description="<@" + str(ctx.author.id) + "> shook <@" + u + ">'s hand.", color=comm.color())
    embed.set_image(random.choice(urls["handshake"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to spank.", required=True)
@lightbulb.command("spank", "Spank 'em", aliases=["SPANK"], nsfw=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def spank(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="Naughty", description="<@" + str(ctx.author.id) + "> spanked <@" + u + "> >w<", color=comm.color())

    file = open("data/operation/spank.txt", "r")
    f = file.read().replace("\r","").split("\n")
    file.close()

    try:
        r1 = json.loads(requests.request("GET", "https://nekos.life/api/v2/img/spank").text)["url"]
    except:
        r1 = ""

    if r1 in f:
        file = open("data/operation/spank.txt", "a")
        file.write('\n' + str(r1))
        file.close()
        embed.set_image(random.choice(urls["spank"]))
    else:
        embed.set_image(r1)

    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to feed.", required=True)
@lightbulb.command("feed", "Feed 'em", aliases=["FEED"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def feed(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="Say aah~~!", description="<@" + str(ctx.author.id) + "> fed " + u, color=comm.color())
    embed.set_image(random.choice(urls["feed"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to bark at.", required=False)
@lightbulb.command("bark", "Bark at 'em", aliases=["woof", "BARK", "WOOF"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def bark(ctx: lightbulb.Context):
    comm.log_com(ctx)
    desc = "<@" + str(ctx.author.id) + "> barked"
    if ctx.options.user != None:
        try:
            u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
        except:
            u = str(ctx.options.user)
        desc += " at " + u
    embed = hikari.Embed(title="WOOF WOOF!", description=desc, color=comm.color())
    embed.set_image(random.choice(urls["bark"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to wag at.", required=False)
@lightbulb.command("wag", "Wag at 'em", aliases=["WAG"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def wag(ctx: lightbulb.Context):
    comm.log_com(ctx)
    desc = "<@" + str(ctx.author.id) + "> wagged their tail"
    if ctx.options.user != None:
        try:
            u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
        except:
            u = str(ctx.options.user)
        desc += " at " + u
    embed = hikari.Embed(title="Wag!", description=desc, color=comm.color())
    embed.set_image(random.choice(urls["wag"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to smug.", required=False)
@lightbulb.command("smug", "Look smug at 'em", aliases=["SMUG"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def smug(ctx: lightbulb.Context):
    comm.log_com(ctx)
    desc = "<@" + str(ctx.author.id) + "> looked smug"
    if ctx.options.user != None:
        try:
            u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
        except:
            u = str(ctx.options.user)
        desc += " at " + u
    embed = hikari.Embed(title=">:33", description=desc, color=comm.color())
    embed.set_image(random.choice(urls["smug"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to wink.", required=False)
@lightbulb.command("wink", "Wink at 'em", aliases=["WINK"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def wink(ctx: lightbulb.Context):
    comm.log_com(ctx)
    desc = "<@" + str(ctx.author.id) + "> winked"
    if ctx.options.user != None:
        try:
            u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
        except:
            u = str(ctx.options.user)
        desc += " at " + u
    embed = hikari.Embed(title=";3", description=desc, color=comm.color())
    embed.set_image(random.choice(urls["wink"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to facepalm.", required=False)
@lightbulb.command("facepalm", "Facepalm at 'em", aliases=["FACEPALM"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def facepalm(ctx: lightbulb.Context):
    comm.log_com(ctx)
    desc = "<@" + str(ctx.author.id) + "> facepalmed"
    if ctx.options.user != None:
        try:
            u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
        except:
            u = str(ctx.options.user)
        desc += " at " + u
    embed = hikari.Embed(title="uggh.....", description=desc, color=comm.color())
    embed.set_image(random.choice(urls["facepalm"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to bite.", required=True)
@lightbulb.command("bite", "Bite 'em", aliases=["BITE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def feed(ctx: lightbulb.Context):
    comm.log_com(ctx)
    try:
        u = "<@" + str(comm.user_id_check(ctx.options.user)) + ">"
    except:
        u = str(ctx.options.user)
    embed = hikari.Embed(title="*CHOMP*", description="<@" + str(ctx.author.id) + "> bit " + u, color=comm.color())
    embed.set_image(random.choice(urls["bite"]))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("floof", "floofy :)", aliases=["FLOOF"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def floofy(ctx: lightbulb.Context):
    comm.log_com(ctx)
    response = requests.get("https://randomfox.ca/floof").json()
    embed = hikari.Embed(title = "Floofy!")
    embed.set_image(response["image"])
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("doggo", "pupper :)", aliases=["DOGGO"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def doggo(ctx: lightbulb.Context):
    comm.log_com(ctx)
    apis = ["https://random.dog/woof.json", "https://api.thedogapi.com/v1/images/search"]
    url = random.choice(apis)
    response = requests.get(url).json()
    embed = hikari.Embed(title = "Woof Woof!!")
    if apis[0] == url:
        embed.set_image(response["url"])
    elif apis[1] == url:
        embed.set_image(response[0]["url"])
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("ducky", "quack :)", aliases=["DUCKY"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def ducky(ctx: lightbulb.Context):
    comm.log_com(ctx)
    response = requests.get("https://random-d.uk/api/v2/random").json()
    embed = hikari.Embed(title = "Quackity Quack!!")
    embed.set_image(response["url"])
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("otter", "kapapapapa :>", aliases=["OTTER"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def otter(ctx: lightbulb.Context):
    comm.log_com(ctx)
    embed = hikari.Embed(title = "kapapapapa")
    embed.set_image(comm.url2uri("https://otter.bruhmomentlol.repl.co/random"))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)
