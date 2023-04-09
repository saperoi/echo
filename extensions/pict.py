import lightbulb
import hikari
import comm
from PIL import Image
import base64
import io
from PIL import Image


# https://stackoverflow.com/questions/60676893/converting-pil-pillow-image-to-data-url
def pillow_image_to_base64_string(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

plugin = lightbulb.Plugin('pict', "Because esmBot doesn't work")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.option("color", "The color you want to display", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help("Supported formats: RRR BBB GGG, RBG (hex!) (websafe), RGBA (hex!) (websafe), RRBBGG, RRBBGGAA, #RRBBGG, #RRBBGGAA, 0xRRBBGG, 0xRRBBGGAA")
@lightbulb.command("show_color", "Show a color code")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
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
    data_url = 'data:image/jpeg;base64,' + pillow_image_to_base64_string(img)
    img.close()
    embed = hikari.Embed(title=str(c), color=c)
    embed.set_image(data_url)
    await ctx.respond(embed)
