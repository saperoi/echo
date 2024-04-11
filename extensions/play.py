import lightbulb
import hikari
import comm
import random
import miru
import sqlite3
import chess
import time
import requests
import asyncio

plugin = lightbulb.Plugin('play', 'Me when I play a role:')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

conmisc = sqlite3.connect("./db/misc.db")
curmisc = conmisc.cursor()

def maze_table_check(s):
    curmisc.execute("CREATE TABLE IF NOT EXISTS ninemaze(sid INTEGER PRIMARY KEY, skulls INTEGER)")
    curmisc.execute("SELECT * FROM ninemaze WHERE sid=?", (int(s),) )
    if curmisc.fetchall() == []:
        curmisc.execute("INSERT INTO ninemaze VALUES (?, ?)", (int(s), 0) )
    conmisc.commit()

@plugin.command
@lightbulb.option("phrase", "write '§' where the item needs to come.", modifier=lightbulb.OptionModifier.CONSUME_REST, type = str, required = False)
@lightbulb.option("count", "how many items to generate", type=int, required=False, min_value=1, max_value=100, default=1)
@lightbulb.command("weapon", "Generates a random weapon", aliases=["WEAPON"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def weapon(ctx: lightbulb.Context):
    comm.log_com(ctx)
    gen_list = []
    for _ in range(ctx.options.count):
        rarity = comm.random_rarity()
        material = comm.random_material(rarity)
        weapon = comm.random_item_type(rarity)
        result = "[" + rarity + "] " + material + " " + weapon
        gen_list.append(result)
    result = "\n".join(gen_list)
    if ctx.options.phrase == None:
        await comm.send_msg(ctx,result)
    elif "§" in ctx.options.phrase:
        p = ctx.options.phrase.split("§")
        msg = ""
        for i in range(ctx.options.phrase.count("§")):
            msg += p[i]
            msg += gen_list[i % ctx.options.count]
        if len(p) > 1:
            msg += p[-1]
        await comm.send_msg(ctx, msg)
    else:
        await comm.send_msg(ctx, ctx.options.phrase + " " + result)

"""
4/13 at trap, enc or heal. 1/13 for chest
after chest: 4/9 trap or enc, 1/9 heal

YOU:
100 hp, 2d12 dmg

encs:
5/10 slime, 4/10 goblin, 1/10 you?
after you: 1/2 slime, 1/2 goblin

slime:
10 hp, 2d5 dmg
flee: 1/2 success, 1/2 10 encasement damge. if die: transformation bad end

goblin:
20 hp, 1d18+3 dmg
flee: 1/3 success, 2/3 grab and 2d5 damage. if die: taken to a secret room and kept there for unknown purposes

you???
1d70 hp, 2d10 dmg (but 1/2 chance of actually damaging, increases the mroe you attack)
DAMAGES YOURSELF AND YOURSELF.
FLEE IMPOSSIBLE
Spare 7 times??

traps:
wire: 1d8 dmg, you trip
"""

@plugin.command
@lightbulb.command("ninemaze", "A small original game where you try to find a treasure.", aliases=["9maze", "NINEMAZE", "9MAZE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def ninemaze(ctx: lightbulb.Context):
    comm.log_com(ctx)

    hp = 100
    heals = 3
    found_treasure = False
    encountered_yourself = False
    room = 0
    exited = False

    up = [0,1,2,3,4,5]
    down = [3,4,5,6,7,8]
    left = [1,2,4,5,7,8]
    right = [0,1,3,4,6,7]
    exit = [0]

    await ctx.respond("Ninemaze!")

    class move_up(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="North")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = 3
            self.view.direction = "North"
            self.view.stop()
    class move_down(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="South")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = -3
            self.view.direction = "South"
            self.view.stop()
    class move_left(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="West")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = -1
            self.view.direction = "West"
            self.view.stop()
    class move_right(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="East")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = 1
            self.view.direction = "East"
            self.view.stop()
    class exit_maze(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.SUCCESS, label="LEAVE")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = -1
            self.view.direction = "LEAVE"
            self.view.stop()
    def room_buttons(i, leave_unlock):
        class ChecksView(miru.View):
            async def view_check(self, mctx: miru.ViewContext) -> bool:
                return mctx.user.id == ctx.author.id
        view = ChecksView()
        if i in up:
            view.add_item(move_up())
        if i in down:
            view.add_item(move_down())
        if i in left:
            view.add_item(move_left())
        if i in right:
            view.add_item(move_right())
        if i in exit and leave_unlock:
            view.add_item(exit_maze())
        return view

    class fight_attack(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Attack")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.action = "attack"
            self.view.stop()
    class fight_flee(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Flee")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.action = "flee"
            self.view.stop()
    class fight_heal(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Heal")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.action = "heal"
            self.view.stop()
    class fight_spare(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Spare")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.action = "spare"
            self.view.stop()
    def fight_system():
        class ChecksView(miru.View):
            async def view_check(self, mctx: miru.ViewContext) -> bool:
                return mctx.user.id == ctx.author.id
        view = ChecksView()
        view.add_item(fight_attack())
        view.add_item(fight_flee())
        view.add_item(fight_heal())
        view.add_item(fight_spare())
        return view

    while (exited == False):
        if room == -1:
            embed = hikari.Embed(title="[[you win!]]", description="Amazing job! You have left the infamous 9-maze in one piece? Great job even! You now go home, 1000 gold pieces richer.", color=comm.color())
            embed.set_footer("Ordered by: " + str(ctx.author))
            await ctx.edit_last_response(embed, components=None)
            exited = True
            break
        if hp < 0:
            if encounter == "trap":
                desc = "You died right then and there when you fell into that. Your body slowly starts decomposing as the slimes and goblins carry your corpse into a hidden spot of the maze. ***Your skull joins the others on the pile.***"
            elif encounter == "slime":
                desc = "The slimes you fought start surrounding your nearly-dead body. It starts to... melt? It liquifies into a non-newtonian cyan substance, as your mind starts to change. ***This is where you belong and where you will stay for eternity.***"
            elif encounter == "goblin":
                desc = "you lost against goblins lmaooo look yat your loser ass getting carried away and put on a death throne. stoooopid"
            elif encounter == "you":
                desc = "You were defeated by 'yourself', or at least a döppelganger. It leaves the maze and you are left to rot inside. ***Nobody is aware of what has happened, and they are all nonethewiser.***"

            maze_table_check(ctx.guild_id)
            curmisc.execute("SELECT skulls FROM ninemaze WHERE sid=?", (int(ctx.guild_id),) )
            server_skull_count, = curmisc.fetchone()
            server_skull_count += 1
            curmisc.execute("UPDATE ninemaze SET skulls=? WHERE sid=?", (server_skull_count, ctx.guild_id))
            conmisc.commit()
            curmisc.execute("SELECT skulls FROM ninemaze WHERE sid=?", (0,) )
            global_skull_count, = curmisc.fetchone()
            global_skull_count += 1
            curmisc.execute("UPDATE ninemaze SET skulls=? WHERE sid=?", (global_skull_count, 0))
            conmisc.commit()

            desc += "\n\nServer Skull Count: " + str(server_skull_count)
            desc += "\nGlobal Skull Count: " + str(global_skull_count)

            embed = hikari.Embed(title="[[bad end]]", description=desc, color=comm.color())
            embed.set_footer("Ordered by: " + str(ctx.author))
            await ctx.edit_last_response(embed, components=None)
            break

        # MOVEMENT
        room_move = room_buttons(room, found_treasure)
        embed = hikari.Embed(title="[[movement]]", description="To what room would you like to move?\n\tYour HP: " + str(hp), color=comm.color())
        embed.set_footer("Ordered by: " + str(ctx.author))
        room_movement = await ctx.edit_last_response(embed, components=room_move)
        await room_move.start(room_movement)
        await room_move.wait()
        if hasattr(room_move, "exist"):
            room += room_move.cardinal
        else:
            await ctx.respond("Did not receive an answer in time!")
            break

        if found_treasure == False:
            event = random.randint(1,15)
            if 1 <= event <= 4:
                event = "trap"
            elif 5 <= event <= 8:
                event = "encounter"
            elif 9 <= event <= 12:
                event = "heal"
            elif 13 <= event <= 15:
                event = "treasure"
        elif found_treasure == True:
            event = random.randint(1,5)
            if 1 <= event <= 2:
                event = "trap"
            elif 3 <= event <= 4:
                event = "encounter"
            elif event == 5:
                event = "heal"

        if event == "trap":
            encounter = "trap"
            trap = random.randint(1,8)
            hp -= trap
            traps = ["You got stuck in a tripwire and fell on the floor. ", "You stepped on some spikes! Ouch! "]
            embed = hikari.Embed(title="[[trapped]]", description=random.choice(traps) + "You took " + str(trap) + " damage. Your HP is now " + str(hp), color=comm.color())
            embed.set_footer("Ordered by: " + str(ctx.author))
            await ctx.edit_last_response(embed, components=None)

        elif event == "heal":
            heal = max(5, random.randint(1,6) + random.randint(1,6))
            hp += heal
            if hp > 100:
                hp = 100
            embed = hikari.Embed(title="[[healed]]", description="You got healed magically by the maze! Your HP is now " + str(hp), color=comm.color())
            embed.set_footer("Ordered by: " + str(ctx.author))
            await ctx.edit_last_response(embed, components=None)
        elif event == "treasure":
            embed = hikari.Embed(title="[[TREASURE]]", description="You have found the secret treasure chest hidden in this maze. You now have to find the exit again so you can leave!", color=comm.color())
            embed.set_footer("Ordered by: " + str(ctx.author))
            found_treasure = True
            await ctx.edit_last_response(embed, components=None)

        elif event == "encounter":
            encounter = random.randint(1,10)
            if encounter == 10 and encountered_yourself == False:
                encounter = "you"
                encountered_yourself = True
            elif 1 <= encounter <= 5:
                encounter = "slime"
            elif 6 <= encounter <= 10:
                encounter = "goblin"

            if encounter == "slime":
                fight_finish = False
                hp_enemy = 10 + random.randint(1,10)
                fled = 0
                desc = "You encountered some slimes! They've surrounded you!\n"
                while fight_finish == False:
                    if hp < 0:
                        embed = hikari.Embed(title="[[slime]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        await ctx.edit_last_response(embed, components=None)
                        fight_finish = True
                    elif hp_enemy <= 0 or fled == 1:
                        desc += "You escaped from the slimes! Well done!\nRemaining HP: " + str(hp)
                        embed = hikari.Embed(title="[[slime]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        await ctx.edit_last_response(embed, components=None)
                        fight_finish = True
                    elif hp_enemy > 0:
                        desc += "What would you like to do?\n\tYour HP: " + str(hp) + "\t\t Enemy HP: " + str(hp_enemy)
                        fight_system_comp = fight_system()
                        embed = hikari.Embed(title="[[slime]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        fight_embed = await ctx.edit_last_response(embed, components=fight_system_comp)
                        await fight_system_comp.start(fight_embed)
                        await fight_system_comp.wait()
                        if hasattr(fight_system_comp, "exist"):
                            desc = ""
                            if fight_system_comp.action == "attack":
                                damage_dealt = random.randint(1,12) + random.randint(1,12)
                                hp_enemy -= damage_dealt
                                desc += "You charged at the slimes and dealt " + str(damage_dealt) + "HP worth of damage!\n"
                                if hp_enemy > 0:
                                    damage_recieved = random.randint(1,5) + random.randint(1,5)
                                    hp -= damage_recieved
                                    desc += "The slimes attacked you for " + str(damage_recieved) + "HP!\n"
                            elif fight_system_comp.action == "flee":
                                fled = random.randint(1,2)
                                if fled == 1:
                                    desc += "You managed to flee from the slimes and can move on to the next room!\n"
                                elif fled == 2:
                                    desc += "The slimes caught you. They attempted to encase you but you broke free. However, you took 10 damage from this.\n"
                                    hp -= 10
                            elif fight_system_comp.action == "heal":
                                if heals > 0:
                                    heals -= 1
                                    hpRestored = max(5, random.randint(1,10) + random.randint(1,10))
                                    hp += hpRestored
                                    desc += "You took the opportunity to heal yourself for " + str(hpRestored) + "HP! You feel fresher, and are filled with determination.\n"
                                else:
                                    desc += "You tried to heal but you have no potions left!\n"
                                damage_recieved = random.randint(1,5) + random.randint(1,5)
                                hp -= damage_recieved
                                desc += "The slimes attacked you for " + str(damage_recieved) + "HP!\n"
                            elif fight_system_comp.action == "spare":
                                desc += "You tried sparing the slimes. This doesn't work!\nThe slimes didn't attack you however.\n"
                        else:
                            await ctx.respond("Did not receive an answer in time!")
                            break

            elif encounter == "goblin":
                fight_finish = False
                hp_enemy = 20 + random.randint(1,10)
                fled = 0
                desc = "A pack of goblins surprise you! They've surrounded you!\n"
                damage_surprise = random.randint(1,18)
                desc += "They jump you and deal " + str(damage_surprise) + "HP worth of damage!\n"
                hp -= damage_surprise
                while fight_finish == False:
                    if hp < 0:
                        embed = hikari.Embed(title="[[goblin]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        await ctx.edit_last_response(embed, components=None)
                        fight_finish = True
                    elif hp_enemy <= 0 or fled == 1:
                        desc += "You escaped from the goblins! Well done!\nRemaining HP: " + str(hp)
                        embed = hikari.Embed(title="[[goblin]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        await ctx.edit_last_response(embed, components=None)
                        fight_finish = True
                    elif hp_enemy > 0:
                        desc += "What would you like to do?\n\tYour HP: " + str(hp) + "\t\t Enemy HP: " + str(hp_enemy)
                        fight_system_comp = fight_system()
                        embed = hikari.Embed(title="[[goblin]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        fight_embed = await ctx.edit_last_response(embed, components=fight_system_comp)
                        await fight_system_comp.start(fight_embed)
                        await fight_system_comp.wait()
                        if hasattr(fight_system_comp, "exist"):
                            desc = ""
                            if fight_system_comp.action == "attack":
                                damage_dealt = random.randint(1,12) + random.randint(1,12)
                                hp_enemy -= damage_dealt
                                desc += "You charged at the goblins and dealt " + str(damage_dealt) + "HP worth of damage!\n"
                                if hp_enemy > 0:
                                    damage_recieved = random.randint(1,18) + 3
                                    hp -= damage_recieved
                                    desc += "The goblins attacked you for " + str(damage_recieved) + "HP!\n"
                            elif fight_system_comp.action == "flee":
                                fled = random.randint(1,3)
                                if fled == 1:
                                    desc += "You managed to flee from the goblins and can move on to the next room!\n"
                                elif fled == 2 or fled == 3:
                                    damage_recieved = random.randint(10,18)
                                    desc += "The goblins caught you. They stomp you and deal " + str(damage_recieved) + " damage.\n"
                                    hp -= damage_recieved
                            elif fight_system_comp.action == "heal":
                                if heals > 0:
                                    heals -= 1
                                    hpRestored = max(5, random.randint(1,10) + random.randint(1,10))
                                    hp += hpRestored
                                    desc += "You took the opportunity to heal yourself for " + str(hpRestored) + "HP! You feel fresher, and are filled with determination.\n"
                                else:
                                    desc += "You tried to heal but you have no potions left!\n"
                                damage_recieved = random.randint(1,18) + 3
                                hp -= damage_recieved
                                desc += "The goblins attacked you for " + str(damage_recieved) + "HP!\n"
                            elif fight_system_comp.action == "spare":
                                damage_recieved = random.randint(1,18) + 6
                                desc += "You tried sparing the goblins. They take offense!\nThey beat you up for " + str(damage_recieved) + " damage!\n"
                                hp -= damage_recieved
                        else:
                            await ctx.respond("Did not receive an answer in time!")
                            break

            elif encounter == "you":
                fight_finish = False
                hp_enemy = 20 + random.randint(1,10)
                desc = "You turn the corner and see.... yourself?!\n"
                spare_count = 0
                while fight_finish == False:
                    if hp < 0:
                        embed = hikari.Embed(title="[[yourself]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        await ctx.edit_last_response(embed, components=None)
                        fight_finish = True
                    elif hp_enemy <= 0:
                        desc += "You managed to slay.. yourself? ***You will never remain the same***\nRemaining HP: " + str(hp)
                        embed = hikari.Embed(title="[[yourself]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        await ctx.edit_last_response(embed, components=None)
                        fight_finish = True
                    elif spare_count == 7:
                        desc += "You have accepted peace with yourself. You can move on!\nRemaining HP: " + str(hp)
                        embed = hikari.Embed(title="[[yourself]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        await ctx.edit_last_response(embed, components=None)
                        fight_finish = True
                    elif hp_enemy > 0:
                        desc += "What would you like to do?\n\tYour HP: " + str(hp) + "\t\t Enemy HP: " + str(hp_enemy)
                        fight_system_comp = fight_system()
                        embed = hikari.Embed(title="[[yourself]]", description=desc, color=comm.color())
                        embed.set_footer("Ordered by: " + str(ctx.author))
                        fight_embed = await ctx.edit_last_response(embed, components=fight_system_comp)
                        await fight_system_comp.start(fight_embed)
                        await fight_system_comp.wait()
                        if hasattr(fight_system_comp, "exist"):
                            desc = ""
                            if fight_system_comp.action == "attack":
                                damage_dealt = random.randint(1,12) + random.randint(1,12)
                                hp_enemy -= damage_dealt
                                desc += "You charged at yourself and dealt " + str(damage_dealt) + "HP worth of damage!\n"
                                if hp_enemy > 0:
                                    hp -= damage_dealt
                                    desc += "You also recieved that amount of damage?! What is going on..?\n"
                            elif fight_system_comp.action == "flee":
                                desc += "You cannot flee! The walls have closed and no entrances nor exists can be found!"
                            elif fight_system_comp.action == "heal":
                                if heals > 0:
                                    heals -= 1
                                    hpRestored = max(5, random.randint(1,10) + random.randint(1,10))
                                    hp += hpRestored
                                    desc += "You took the opportunity to heal yourself for " + str(hpRestored) + "HP! You feel fresher, and are filled with determination.\n"
                                else:
                                    desc += "You tried to heal but you have no potions left!\n"
                                damage_recieved = random.randint(1,10) + 1
                                hp -= damage_recieved
                                desc += "You got damaged for " + str(damage_recieved) + "HP!\n"
                            elif fight_system_comp.action == "spare":
                                damage_recieved = random.randint(1,10) + 1
                                desc += "You tried accepting yourself! You feel something change. However, you recieve " + str(damage_recieved) + " damage due to... ??\n"
                                hp -= damage_recieved
                                spare_count += 1
                        else:
                            await ctx.respond("Did not receive an answer in time!")
                            break
        asyncio.sleep(3)

@plugin.command
@lightbulb.set_help("You play a bad chess bot. It priorititzes en passent, checkmate, then check, then capture, then stalemate and then move. It has a depth of one!")
@lightbulb.command("chess", "Play a fun game of chess against a very bad bot!", aliases=["CHESS"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def chessBot(ctx: lightbulb.Context):
    comm.log_com(ctx)
    side = random.choice(["white", "black"])
    game_finish = False
    board = chess.Board()

    await ctx.respond("Chess!")

    def move_view(moves):
        class ChecksView(miru.View):
            async def view_check(self, mctx: miru.ViewContext) -> bool:
                return mctx.user.id == ctx.author.id
        view = ChecksView()
        big_moves = []
        move_list = []
        for i in range(len(moves)):
            move_list.append( miru.SelectOption( label=board.san(moves[i]) ) )
            if len(move_list) == 25:
                big_moves.append(move_list)
                move_list = []
        if move_list != []:
            big_moves.append(move_list)
        for k in big_moves:
            class move_select(miru.TextSelect):
                def __init__(self, *args, **kwargs) -> None:
                    super().__init__(*args, **kwargs)
                async def callback(self, ctx: miru.ViewContext) -> None:
                    self.view.exist = True
                    self.view.move = self.values[0]
                    self.view.stop()
            view.add_item(move_select(placeholder="Move to Play", options=k))
        return view

    while game_finish == False:
        async def player_move():
            moves = list(board.legal_moves)
            chess_view = move_view(moves)
            embed = hikari.Embed(title="[[chess board]]", description="```\n" + str(board) + "\n```", color=comm.color())
            embed.set_image("https://backscattering.de/web-boardimage/board.png?orientation=" + side + "&fen=" + board.fen().split(" ")[0])
            embed.set_footer("Ordered by: " + str(ctx.author))
            chess_msg = await ctx.edit_last_response(embed, components=chess_view)
            await chess_view.start(chess_msg)
            await chess_view.wait()
            if hasattr(chess_view, "exist"):
                board.push_san(chess_view.move)
            else:
                raise ValueError

        async def computer_move():
            moves = list(board.legal_moves)

            checkmate = []
            promote = []
            check = []
            capture = []
            for i in moves:
                if "#" in board.san(i):
                    checkmate.append(i)
                if "=" in board.san(i):
                    promote.append(i)
                if "+" in board.san(i):
                    capture.append(i)
                if "x" in board.san(i):
                    capture.append(i)

            embed = hikari.Embed(title="[[chess board]]", description="```\n" + str(board) + "\n```", color=comm.color())
            embed.set_image("https://backscattering.de/web-boardimage/board.png?orientation=" + side + "&fen=" + board.fen().split(" ")[0])
            embed.set_footer("Ordered by: " + str(ctx.author))
            await ctx.edit_last_response(embed, components=None)

            if checkmate != []:
                board.push(random.choice(checkmate))
            elif promote != []:
                board.push(random.choice(promote))
            elif check != []:
                board.push(random.choice(check))
            elif capture != []:
                board.push(random.choice(capture))
            else:
                board.push(random.choice(moves))

        if (board.turn == chess.WHITE and side == "white") or (board.turn == chess.BLACK and side == "black"):
            try:
                await player_move()
            except:
                await ctx.respond("Did not receive an answer in time!")
                break

        elif (board.turn == chess.WHITE and side == "black") or (board.turn == chess.BLACK and side == "white"):
            await computer_move()

@chessBot.set_error_handler
async def chessBot_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    pass

@plugin.command
@lightbulb.set_help("Standard Wordle rules.")
@lightbulb.command("wordle", "Play a neat game of Wordle!", aliases=["WORDLE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def wordle(ctx: lightbulb.Context):
    comm.log_com(ctx)
    alpha = dictionary = open("./data/wordle_alpha.txt", "r", encoding = "utf-8").read().splitlines()
    gamma = alpha
    secret = random.choice(alpha)
    starttime = time.time()

    embed_desc = ""
    embed = hikari.Embed(title="[[WORDLE | GUESS 1/6]]", description=embed_desc, color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

    def nCopies(n, copy):
        res = []
        for _ in range(n):
            res.append(copy)
        return res

    async def await_answer(iss = ""):
        await ctx.edit_last_response(iss + " What is your guess?")
        event = await ctx.app.event_manager.wait_for(hikari.GuildMessageCreateEvent, predicate=lambda e: e.message.author == ctx.author, timeout=30)
        try:
            answer = await ctx.app.rest.fetch_message(event.message.channel_id, event.message.id)
            answer = answer.content
        except:
            await ctx.respond("Didn't recieve response in time")
            raise Exception
        return answer

    async def getGuess(guesslist):
        flagChar = False
        flagLen = False
        flagDict = False
        flagDeja = False
        word = await await_answer()

        while False in [flagChar, flagLen, flagDict, flagDeja]:
            flagChar = False
            flagLen = False
            flagDict = False
            flagDeja = False
            word = word.lower()

            # flagLen

            if len(word) == 5:
                flagLen = True
            else:
                l = list(word)
                flagLen = False
                if len(word) > 5:
                    word = await await_answer("Guess is too long, please try again.")
                if len(word) < 5:
                    word = await await_answer("Guess is too short, please try again.")
                pass

            # flagChar

            if not word.isalpha():
                flagChar = False
                word = await await_answer("Guess contains invalid characters, please try again.")
                pass
            else:
                flagChar = True

            # flagDict

            if word in gamma:
                flagDict = True
            else:
                flagDict = False
                word = await await_answer("Invalid guess, please try again.")
                pass

            # flagDeja

            if guesslist == []:
                flagDeja = True
            else:
                tempflagdeja = False
                for i in range(len(guesslist)):
                    if word == guesslist[i]:
                        tempflagdeja = True
                if tempflagdeja == False:
                    flagDeja = True
                else:
                    flagDeja = False
                    word = await await_answer("Already guessed this word.")
                    pass

        return word

    def getVerdict(guess, seca):
        sec = seca
        guessl = list(guess)
        verdict = []
        arrverdict = []

        sect = sec
        secl = list(sect)
        tempverdict = nCopies(len(sect), "")
        greens = nCopies(len(sect), False)

        for j in range(len(sect)):
            if guessl[j] == secl[j]:
                tempverdict[j] = "G"
                secl[j] = "-"
                greens[j] = True
        for j in range(len(sect)):
            if greens[j] == True:
                continue
            elif guessl[j] in sect:
                for k in range(len(sect)):
                    if guessl[j] == secl[k]:
                        tempverdict[j] = "y"
                        secl[k] = "-"
                        sect = "".join(secl)
                        secl = list(sect)
        for j in range(len(tempverdict)):
            if tempverdict[j] == "":
                tempverdict[j] = "-"
        arrverdict.append("".join(tempverdict))
        tempverdict = "".join(tempverdict)
        verdict.append(tempverdict)
        verdict = " ".join(verdict)
        return verdict, arrverdict

    def guessEmoji(guess):
        s = list(guess)
        for i in range(len(s)):
            s[i] = ":regional_indicator_" + s[i].lower() + ":"
        return "".join(s)
    def verdictEmoji(verdict):
        s = list(verdict)
        for i in range(len(s)):
            if s[i] == "-":
                s[i] = ":black_large_square:"
            elif s[i] == "y":
                s[i] = ":yellow_square:"
            elif s[i] == "G":
                s[i] = ":green_square:"
        return "".join(s)

    sec = secret
    starttime = time.time()
    lasttime = starttime
    i = 1

    lastguess = ("", "")
    guesslist = []
    emojis = []
    while i <= 6:
        word = await getGuess(guesslist)
        if word == None:
            return
        word = word.lower()
        guesslist.append(word)
        word = list(word)

        verdict, arrverdict = getVerdict(word, sec)
        lastguess = (word, verdict)
        embed_desc += guessEmoji(word) + "\n" + verdictEmoji(verdict) + "\n"
        emojis.append(verdictEmoji(verdict))

        vflag = False

        if verdict == "GGGGG":
            sec = "-----"

        if sec == "-----":
            vflag = True

        i+=1
        embed = hikari.Embed(title="[[WORDLE | GUESS " + str(i if i != 7 else 6) + "/6]]", description=embed_desc, color=comm.color())
        embed.set_footer("Ordered by: " + str(ctx.author))
        await ctx.edit_last_response(embed)
        if vflag == True:
            guesscount = i-1
            i = 7
    if vflag == False:
        timespent = round((time.time() - lasttime), 2)
        msg = "You lost :( The word was: " + secret + "\n"
        embed_title = "[[WORDLE: LOSS]]"
    elif vflag == True:
        msg = "You won! The word was: " + secret
        timespent = round((time.time() - starttime), 2)
        msg += "\nYou guessed it in " + str(guesscount) + " guesses, and took " + str(timespent) + " seconds.\n"
        embed_title = "[[WORDLE: WIN]]"
    msg += "\n".join(emojis)
    embed = hikari.Embed(title=embed_title, description=msg, color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@wordle.set_error_handler
async def wordle_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    pass


@plugin.command
@lightbulb.set_help("You have .")
@lightbulb.command("pushthebox", "Play a game where you have to push a box around!", aliases=["ptb", "PUSHTHEBOX", "PTB"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def pushthebox(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await ctx.respond("Push The Box!")
    """
    0  1  2  3  4  5  6  7  8
    9  10 11 12 13 14 15 16 17
    18 19 20 21 22 23 24 25 26
    27 28 29 30 31 32 33 34 35
    36 37 38 39 40 41 42 43 44
    45 46 47 48 49 50 51 52 53
    54 55 56 57 58 59 60 61 62
    """
    win = False
    goal = random.choice([10, 11, 12, 14, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50, 51, 52])
    box = [20, 21, 22, 23, 24, 29, 30, 31, 32, 33, 38, 39, 40, 41, 42]
    try:
        box.remove(goal)
    except:
        pass
    box = random.choice(box)
    player = [10, 11, 12, 14, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50, 51, 52]
    player.remove(box)
    player = random.choice(player)
    rim = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 18, 26, 27, 35, 36, 44, 45, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62]
    def desc(b, p, win):
        grid = [":black_large_square:" for _ in range(63)]
        for i in rim:
            grid[i] = ":red_square:"
        grid[goal] = ":negative_squared_cross_mark:"
        grid[b] = ":brown_square:"
        grid[p] = ":white_square_button:"
        if win == True:
            grid[goal] = ":triangular_flag_on_post:"
        d = ""
        for i in range(len(grid)):
            if i % 9 == 0:
                d += "\n"
            d += grid[i]
        return d

    class move_up(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="North")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = -9
            self.view.direction = "North"
            self.view.stop()
    class move_down(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="South")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = +9
            self.view.direction = "South"
            self.view.stop()
    class move_left(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="West")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = -1
            self.view.direction = "West"
            self.view.stop()
    class move_right(miru.Button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(style=hikari.ButtonStyle.PRIMARY, label="East")
        async def callback(self, ctx: miru.ViewContext) -> None:
            self.view.exist = True
            self.view.cardinal = 1
            self.view.direction = "East"
            self.view.stop()
    def move_buttons(i):
        class ChecksView(miru.View):
            async def view_check(self, mctx: miru.ViewContext) -> bool:
                return mctx.user.id == ctx.author.id
        view = ChecksView()
        northbound = [10, 11, 12, 13, 14, 15, 16]
        southbound = [46, 47, 48, 49, 50, 51, 52]
        westbound = [10, 19, 28, 37, 46]
        eastbound = [16, 25, 34, 43, 52]
        if i not in northbound and (i-9) != goal and (False if (i-9 == box and box-9 in rim) else True):
            view.add_item(move_up())
        if i not in southbound and (i+9) != goal and (False if (i+9 == box and box+9 in rim) else True):
            view.add_item(move_down())
        if i not in westbound and (i-1) != goal and (False if (i-1 == box and box-1 in rim) else True):
            view.add_item(move_left())
        if i not in eastbound and (i+1) != goal and (False if (i+1 == box and box+1 in rim) else True):
            view.add_item(move_right())
        return view

    game_finish = False
    while game_finish == False:
        if win == True:
            game_finish = True
            embed = hikari.Embed(title="[[push the box | WIN]]", description=desc(box, player, win), color=comm.color())
            embed.set_footer("Ordered by: " + str(ctx.author))
            await ctx.edit_last_response(embed, components=None)
            return
        embed = hikari.Embed(title="[[push the box]]", description=desc(box, player, win), color=comm.color())
        embed.set_footer("Ordered by: " + str(ctx.author))
        move_view = move_buttons(player)
        movement = await ctx.edit_last_response(embed, components=move_view)
        await move_view.start(movement)
        await move_view.wait()
        if hasattr(move_view, "exist"):
            if player + move_view.cardinal == box:
                box += move_view.cardinal
            player += move_view.cardinal
            if box == goal:
                win = True
        else:
            raise ValueError

@pushthebox.set_error_handler
async def pushthebox_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    pass

dictionary = open("./data/dict.txt", "r", encoding = "utf-8").read().splitlines()

@plugin.command
@lightbulb.set_help("Regular hangman")
@lightbulb.command("hangman", "Play a neat game of Hangman!", aliases=["HANGMAN"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def hangman(ctx: lightbulb.Context):
    comm.log_com(ctx)
    word = random.choice(dictionary)
    workword = ["-" for i in range(len(word))]
    hangdraw = [
"""```
.....
.....
.....
.....
.....
.....
.....
```""",

"""```
.....
.....
.....
.....
.....
.....
-----
```""",

"""```
.....
|....
|....
|....
|....
|....
-----
```""",

"""```
.___.
|....
|....
|....
|....
|....
-----
```""",

"""```
.___.
|/...
|....
|....
|....
|....
-----
```""",

"""```
.___.
|/.|.
|....
|....
|....
|....
-----
```""",

"""```
.___.
|/.|.
|..O.
|....
|....
|....
-----
```""",

"""```
.___.
|/.|.
|..O.
|..|.
|....
|....
-----
```""",

"""```
.___.
|/.|.
|..O.
|..|.
|./..
|....
-----
```""",

"""```
.___.
|/.|.
|..O.
|..|.
|./.\\
|....
-----
```""",

"""```
.___.
|/.|.
|..O.
|./|.
|./.\\
|....
-----
```""",

"""```
.___.
|/.|.
|..O.
|./|\\
|./.\\
|....
-----
```"""]
    used_letters = []
    bad_letters = []
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    starttime = time.time()

    async def await_answer(iss = ""):
        await ctx.edit_last_response(iss + " What is your guess?")
        event = await ctx.app.event_manager.wait_for(hikari.GuildMessageCreateEvent, predicate=lambda e: e.message.author == ctx.author, timeout=30)
        try:
            answer = await ctx.app.rest.fetch_message(event.message.channel_id, event.message.id)
            answer = answer.content
        except:
            await ctx.respond("Didn't recieve response in time")
            raise Exception
        return answer

    async def getGuess(used):
        letter = await await_answer()
        letter = letter.lower()
        flagAlphabet = False
        while flagAlphabet == False:
            if letter not in alphabet:
                letter = await await_answer("This isn't a letter! Please try again!")
            elif letter in used_letters:
                letter = await await_answer("This letter was used, try again!")
            else:
                return letter

    embed = hikari.Embed(title="[[HANGMAN]]", description="", color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

    complete = False
    while complete == False:
        desc = hangdraw[len(bad_letters)] + "\n" + "".join(workword) + "\nUsed Letters: " + "".join(used_letters)
        embed = hikari.Embed(title="[[HANGMAN]]", description=desc, color=comm.color())
        embed.set_footer("Ordered by: " + str(ctx.author))
        await ctx.edit_last_response(embed)
        if "".join(workword) == word:
            complete = True
            success = True
            break
        letter = await getGuess(used_letters)
        used_letters.append(letter)
        if letter not in word:
            bad_letters.append(letter)
        else:
            for i in range(len(word)):
                if word[i] == letter:
                    workword[i] = letter

        if len(bad_letters) >= len(hangdraw):
            complete = True
            success = False

    if success == False:
        msg = "You lost :( The word was: " + word + "\n"
        embed_title = "[[HANGMAN: LOSS]]"
    elif success == True:
        msg = "You won! The word was: " + word
        timespent = round((time.time() - starttime), 2)
        msg += "\nYou guessed it in " + str(len(used_letters)) + " guesses, and took " + str(timespent) + " seconds.\n"
        embed_title = "[[HANGMAN: WIN]]"
    embed = hikari.Embed(title=embed_title, description=msg, color=comm.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@hangman.set_error_handler
async def hangman_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    pass
