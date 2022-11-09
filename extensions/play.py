import lightbulb
import hikari
import comm
import random

plugin = lightbulb.Plugin('play', 'Me when I play a role:')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.option("phrase", "write '§' where the item needs to come.", modifier=lightbulb.OptionModifier.CONSUME_REST, type=str, required=False)
@lightbulb.command("weapon", "Generates a random weapon")
@lightbulb.implements(lightbulb.PrefixCommand)
async def weapon(ctx: lightbulb.Context):
    comm.log_com(ctx)
    n, mat = comm.rndm_mat()
    rar = comm.rndm_rar(n)
    weap = random.choice(comm.weapons)
    res = rar + " " + mat + " " + weap
    if ctx.options.phrase == None:
        await ctx.respond(res)
    elif "§" in ctx.options.phrase:
        await comm.send_msg(ctx, ctx.options.phrase.replace("§", res))
    else:
        await comm.send_msg(ctx, ctx.options.phrase + " " + res)
