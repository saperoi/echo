import lightbulb
import hikari
import miru
import comm
import json
import requests
import re
import base64
import urllib.parse

plugin = lightbulb.Plugin('wiki', "jarvis look up 'bayes theorem' on wikipedia and go to figure 2 under interpretations.")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

def nonTextChecker(text) -> bool:
    flags = ["image", "group", "gallery>"]
    for x in flags:
        if x in text:
            return True
    return False

def query_view(url, ctx):
    class ChecksView(miru.View):
        async def view_check(self, mctx: miru.ViewContext) -> bool:
            return mctx.user.id == ctx.author.id
    view = ChecksView()
    
    class query_select(miru.TextSelect):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.title = self.values[0]
            self.view.siteres = url[3][url[1].index(self.values[0])]
            self.view.stop()
    view.add_item(query_select(placeholder="Query Results", options=[miru.SelectOption( label=search_result ) for search_result in url[1]]))
    return view

@plugin.command
@lightbulb.option("query", "The search terms")
@lightbulb.option("wiki", "Choose the wiki to get results from. This is the 'xxxx.fandom.com' part of the URL.")
@lightbulb.command("fandom", "Looks up on Fandom (hate them though)", aliases=["FANDOM"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def fandom(ctx: lightbulb.Context):
    comm.log_com(ctx)
    qurl = f"https://{ctx.options.wiki}.fandom.com/api.php?action=opensearch&search={urllib.parse.quote(ctx.options.query, safe='')}&limit=5&format=json"

    qurl = json.loads(requests.get(qurl).text)
    query_v = query_view(qurl, ctx)
    embed = hikari.Embed(title=ctx.options.wiki, description="```diff\n" + "\n".join([" + " + search_result + "\n" for search_result in qurl[1]]) + "```", color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    query_msg = await ctx.respond(embed, components=query_v)
    await query_v.start(query_msg)
    await query_v.wait()
    if hasattr(query_v, "exist"):
        query_v.stop()
    else:
        raise ValueError

    purl = f"https://{ctx.options.wiki}.fandom.com/api.php?action=parse&page={urllib.parse.quote(query_v.title, safe='')}&prop=wikitext&formatversion=2&format=json"
    unparsed_text = json.loads(requests.get(purl).text)["parse"]["wikitext"]
    
    unclosed = 0
    enclosed = []
    current = ""
    for x in range(len(unparsed_text)-1):
        if unparsed_text[x] + unparsed_text[x+1] == "{{" or unparsed_text[x-1] + unparsed_text[x] == "{{":
            unclosed += 1
            current += unparsed_text[x]
        elif unparsed_text[x] + unparsed_text[x+1] == "}}" or unparsed_text[x-1] + unparsed_text[x] == "}}":
            unclosed -= 1
            current += unparsed_text[x]
            if unclosed == 0:
                enclosed.append(current)
                current = ""
        elif unclosed > 0:
            current += unparsed_text[x]
    
    non_infobox = lambda x: bool([noni for noni in ["redirect"] if (noni in x.lower())])
    print(enclosed)
    maybebox = next((s for s in enclosed if '|' in s and '=' in s and not non_infobox(s)), None)[2:-2]
    if maybebox == None:
        await ctx.respond(f"Could not find a valid infobox! If you find it, DM it to <@{comm.owner_id[0]}>.")
        return

    maybebox = maybebox.split('|')
    embed = hikari.Embed(title=f"{ctx.options.wiki}:{query_v.title} - {maybebox[0]}", url=f"https://{ctx.options.wiki}.fandom.com/wiki/{urllib.parse.quote(query_v.title, safe='')}", color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    del maybebox[0]

    nonTextChecker = lambda x: bool([noni for noni in ["extratex", "group", "gallery", "hardness", "caption", ".png", "image", "link", "alt"] if (noni in x.lower())])

    for x in maybebox:
        try:
            if "=" not in x or nonTextChecker(x):
                continue
            x = x.split("=")
            x[1] = x[1].replace("<nowiki>", "").replace("</nowiki>", "")
            x[1] = re.sub(r"<([a-z]+)([^>]*>)[^>]*>", "", x[1]).replace("\n", "").strip()
            if x[1] == "":
                continue
            x[1] = x[1].replace("''", "*").replace("<br/>", "\n")
            embed.add_field(name=x[0].strip(), value=x[1])
        except:
            pass

    if embed.fields == []:
        embed.add_field(name="Could not find a valid infobox!", value=f"If you find it, DM it to <@{comm.owner_id[0]}>.")
    await ctx.respond(embed)
