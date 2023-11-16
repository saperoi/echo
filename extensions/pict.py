import lightbulb
import hikari
import comm
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import random
import math

plugin = lightbulb.Plugin('pict', "Because esmBot doesn't work")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.option("color", "The color you want to display", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("Supported formats: RRR BBB GGG, RBG (hex!) (websafe), RGBA (hex!) (websafe), RRBBGG, RRBBGGAA, #RRBBGG, #RRBBGGAA, 0xRRBBGG, 0xRRBBGGAA")
@lightbulb.command("show_color", "Show a color code", aliases=["color", "SHOW_COLOR", "COLOR"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def show_color(ctx: lightbulb.Context):
    comm.log_com(ctx)
    co = ctx.options.color
    try:
        if len(co.split(' ')) == 3:
            print("yes")
            a = co.split(' ')
            r, g, b = (int(a[0]), int(a[1]), int(a[2]))
            c = (r, g, b)
            img = Image.new('RGB', (256,256), c)
        elif len(co) == 3:
            c = int((str(co)[0] + str(co)[0]), 16), int((str(co)[1] + str(co)[1]), 16), int((str(co)[2] + str(co)[2]), 16)
            img = Image.new('RGB', (256,256), c)
        elif len(co) == 6:
            c = (int(co[:2], 16), int(co[2:][:2], 16), int(co[-2:], 16))
            img = Image.new('RGB', (256,256), c)
        elif len(co) == 7 and co[0] == "#":
            c = (int(co[1:][:2], 16), int(co[1:][2:][:2], 16), int(co[1:][-2:], 16))
            img = Image.new('RGB', (256,256), c)
        elif len(co) == 8 and co[1] == "x":
            c = (int(co[2:][:2], 16), int(co[2:][2:][:2], 16), int(co[2:][-2:], 16))
            img = Image.new('RGB', (256,256), c)
        else:
            raise Exception
    except:
        await ctx.respond("You provided an incorrect color code.")
        return
    data_url = 'data:image/png;base64,' + comm.pillow_image_to_base64_string(img)
    img.close()
    embed = hikari.Embed(title=str(c), color=c)
    embed.set_image(data_url)
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)


"""  
https://github.com/nyancrimew/SAINT
This code is licensed under the MIT License.
The full version of this license can be found at /used_licenses/SAINT_LICENSE
"""
class WHAT_AM_I_DOING(ImageFilter.BuiltinFilter):
    name = "god stop me please"
    filterargs = (5, 5), 250, 0, (
        1,  10,  5,  6,  1, 
        1,  5, 50,  55,  1, 
        1,  1,  69,  1,  0, 
        1,  3,  1,  1,  1, 
        6,  30,  30,  5,  20, 
    )

@plugin.command
@lightbulb.option("user", "The user to deepfry.", type=hikari.User, required=False)
@lightbulb.command("nuke", "Deepfry an image real bad", aliases=["deepfry", "NUKE", "DEEPFRY"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def nuke(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                img = comm.url2pil(str(ctx.author.default_avatar_url))
            else:
                img = comm.url2pil(str(ctx.author.avatar_url))
        else:
            img = comm.url2pil(str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0]))
            if img.size[0]*img.size[1] > 1024*1024:
                await ctx.respond("Your image is too big (bigger than the amount of pixels in a 1024x1024 image). Please use a smaller image.")
                return
    else:
        if ctx.options.user.avatar_url == None:
            img = comm.url2pil(str(ctx.options.user.default_avatar_url))
        else:
            img = comm.url2pil(str(ctx.options.user.avatar_url))
    img = img.convert('RGBA')
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.DETAIL)
    img = img.filter(WHAT_AM_I_DOING)
    img = ImageEnhance.Color(img).enhance(2)
    img = ImageEnhance.Contrast(img).enhance(2)
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    data_url = 'data:image/png;base64,' + comm.pillow_image_to_base64_string(img)
    img.close()
    embed = hikari.Embed(title=":boom:", color=comm.color())
    embed.set_image(data_url)
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)
"""
End of licensed code
"""

def colorfy(img, hexd):
    img = img.convert('RGBA')
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b, a = img.getpixel((x, y))
            lum = math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
            m = lambda h: round((lum*h)/255)
            img.putpixel((x,y), (m(hexd[0]), m(hexd[1]), m(hexd[2]), a))
    return img

@plugin.command
@lightbulb.option("color", "The color you want to display", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "The user to Blurplify.", type=hikari.User, required=False)
@lightbulb.set_help("Supported formats: RRR BBB GGG, RBG (hex!) (websafe), RGBA (hex!) (websafe), RRBBGG, RRBBGGAA, #RRBBGG, #RRBBGGAA, 0xRRBBGG, 0xRRBBGGAA")
@lightbulb.command("colorify", "Recolor an image!", aliases=["COLORIFY"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def colorify(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                img = comm.url2pil(str(ctx.author.default_avatar_url))
            else:
                img = comm.url2pil(str(ctx.author.avatar_url))
        else:
            img = comm.url2pil(str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0]))
            if img.size[0]*img.size[1] > 1024*1024:
                await ctx.respond("Your image is too big (bigger than the amount of pixels in a 1024x1024 image). Please use a smaller image.")
                return
    else:
        if ctx.options.user.avatar_url == None:
            img = comm.url2pil(str(ctx.options.user.default_avatar_url))
        else:
            img = comm.url2pil(str(ctx.options.user.avatar_url))
    print(img)
    co = ctx.options.color
    try:
        if len(co.split(' ')) == 3:
            print("yes")
            a = co.split(' ')
            r, g, b = (int(a[0]), int(a[1]), int(a[2]))
            c = (r, g, b)
        elif len(co) == 3:
            c = int((str(co)[0] + str(co)[0]), 16), int((str(co)[1] + str(co)[1]), 16), int((str(co)[2] + str(co)[2]), 16)
        elif len(co) == 6:
            c = (int(co[:2], 16), int(co[2:][:2], 16), int(co[-2:], 16))
        elif len(co) == 7 and co[0] == "#":
            c = (int(co[1:][:2], 16), int(co[1:][2:][:2], 16), int(co[1:][-2:], 16))
        elif len(co) == 8 and co[1] == "x":
            c = (int(co[2:][:2], 16), int(co[2:][2:][:2], 16), int(co[2:][-2:], 16))
        else:
            raise Exception
    except:
        await ctx.respond("You provided an incorrect color code.")
    print(c)
    img = colorfy(img, c)
    data_url = 'data:image/png;base64,' + comm.pillow_image_to_base64_string(img)
    img.close()
    embed = hikari.Embed(title="COLORED!!", color=c)
    embed.set_image(data_url)
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to Blurplify.", type=hikari.User, required=False)
@lightbulb.command("blurple", "Blurplify your avatar", aliases=["BLURPLE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def blurple(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                img = comm.url2pil(str(ctx.author.default_avatar_url))
            else:
                img = comm.url2pil(str(ctx.author.avatar_url))
        else:
            img = comm.url2pil(str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0]))
            if img.size[0]*img.size[1] > 1024*1024:
                await ctx.respond("Your image is too big (bigger than the amount of pixels in a 1024x1024 image). Please use a smaller image.")
                return
    else:
        if ctx.options.user.avatar_url == None:
            img = comm.url2pil(str(ctx.options.user.default_avatar_url))
        else:
            img = comm.url2pil(str(ctx.options.user.avatar_url))
    img = colorfy(img, (114,137,218))
    data_url = 'data:image/png;base64,' + comm.pillow_image_to_base64_string(img)
    img.close()
    embed = hikari.Embed(title="Blurple!!", color=(114,137,218))
    embed.set_image(data_url)
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to ourplify.", type=hikari.User, required=False)
@lightbulb.command("ourple", "Ourplify your avatar", aliases=["OURPLE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def ourple(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                img = comm.url2pil(str(ctx.author.default_avatar_url))
            else:
                img = comm.url2pil(str(ctx.author.avatar_url))
        else:
            img = comm.url2pil(str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0]))
            if img.size[0]*img.size[1] > 1024*1024:
                await ctx.respond("Your image is too big (bigger than the amount of pixels in a 1024x1024 image). Please use a smaller image.")
                return
    else:
        if ctx.options.user.avatar_url == None:
            img = comm.url2pil(str(ctx.options.user.default_avatar_url))
        else:
            img = comm.url2pil(str(ctx.options.user.avatar_url))
    img = colorfy(img, (228,31,180))
    data_url = 'data:image/png;base64,' + comm.pillow_image_to_base64_string(img)
    img.close()
    embed = hikari.Embed(title="Ourple!!", color=(228,31,180))
    embed.set_image(data_url)
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to sepia.", type=hikari.User, required=False)
@lightbulb.command("sepia", "Sepia your avatar", aliases=["SEPIA"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def sepia(ctx: lightbulb.Context):
    comm.log_com(ctx)
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                img = comm.url2pil(str(ctx.author.default_avatar_url))
            else:
                img = comm.url2pil(str(ctx.author.avatar_url))
        else:
            img = comm.url2pil(str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0]))
            if img.size[0]*img.size[1] > 1024*1024:
                await ctx.respond("Your image is too big (bigger than the amount of pixels in a 1024x1024 image). Please use a smaller image.")
                return
    else:
        if ctx.options.user.avatar_url == None:
            img = comm.url2pil(str(ctx.options.user.default_avatar_url))
        else:
            img = comm.url2pil(str(ctx.options.user.avatar_url))
    img = img.convert('RGBA')
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b, a = img.getpixel((x, y))
            m = lambda h: 255 if round(h) > 255 else round(h)
            img.putpixel((x,y), (m((r * .393) + (g *.769) + (b * .189)), m((r * .349) + (g *.686) + (b * .168)), m((r * .272) + (g *.534) + (b * .131)), a))
    data_url = 'data:image/png;base64,' + comm.pillow_image_to_base64_string(img)
    img.close()
    embed = hikari.Embed(title="Sepia!!", color=0x704214)
    embed.set_image(data_url)
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)
    
"""
API AVATAR FUCKERY
"""

@plugin.command
@lightbulb.option("user", "The user to waste.", type=hikari.User, required=False)
@lightbulb.command("wasted", "Wastedeeznuts", aliases=["WASTED"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def wasted(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://some-random-api.com/canvas/overlay/wasted?avatar="
    embed = hikari.Embed(title="WASTED", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to trigger.", type=hikari.User, required=False)
@lightbulb.command("triggered", "I will not enter a description so you will get triggered", aliases=["TRIGGERED"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def triggered(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://some-random-api.com/canvas/overlay/triggered?avatar="
    embed = hikari.Embed(title="TRIGGERED", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to pass.", type=hikari.User, required=False)
@lightbulb.command("passed", "Mission passed", aliases=["PASSED"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def passed(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://some-random-api.com/canvas/overlay/passed?avatar="
    embed = hikari.Embed(title="MISSION PASSED", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to jail.", type=hikari.User, required=False)
@lightbulb.command("jail", "Go to horny jail", aliases=["JAIL"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def jail(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://some-random-api.com/canvas/overlay/jail?avatar="
    embed = hikari.Embed(title="[[BONK!]]", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to glass.", type=hikari.User, required=False)
@lightbulb.command("glass", "Give your avatar a glass effect overlay", aliases=["GLASS"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def glass(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://some-random-api.com/canvas/overlay/glass?avatar="
    embed = hikari.Embed(title="glass!!", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to make fruity.", type=hikari.User, required=False)
@lightbulb.command("gay", "Give your avatar a rainbow overlay", aliases=["rainbow", "GAY", "RAINBOW"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def gay(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://some-random-api.com/canvas/overlay/gay?avatar="
    embed = hikari.Embed(title=":rainbow:", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to make a comrade.", type=hikari.User, required=False)
@lightbulb.command("comrade", "Yes", aliases=["COMRADE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def comrade(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://some-random-api.com/canvas/overlay/comrade?avatar="
    embed = hikari.Embed(title="SOYUZ NERUSHIMI RESPUNLIK SVOBODNYKH", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to Blurplify.", type=hikari.User, required=False)
@lightbulb.command("horny_license", "Horny card", aliases=["HORNY_LICENSE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def horny_license(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://some-random-api.com/canvas/misc/horny?avatar="
    embed = hikari.Embed(title="I have a license", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "The user to pet.", type=hikari.User, required=False)
@lightbulb.command("petpet", "Pet a user, and turn them into a gif!", aliases=["PETPET"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def petpet(ctx: lightbulb.Context):
    comm.log_com(ctx)
    url = "https://suffxr.discloud.app/gif/petpet?image_url="
    embed = hikari.Embed(title="-w-", color=comm.color())
    if ctx.options.user == None:
        if ctx.event.message.attachments == [] or "image" not in " ".join([a.media_type for a in ctx.event.message.attachments]):
            if ctx.author.avatar_url == None:
                embed.set_image(comm.url2uri(url + str(ctx.author.default_avatar_url)))
            else:
                embed.set_image(comm.url2uri(url + str(ctx.author.avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str([a.url for a in ctx.event.message.attachments if "image" in a.media_type][0])))
    else:
        if ctx.options.user.avatar_url == None:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.default_avatar_url)))
        else:
            embed.set_image(comm.url2uri(url + str(ctx.options.user.avatar_url)))
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)
