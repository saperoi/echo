# ｅｃｈｏ

Prefix: e//

[Invite link](https://discord.com/oauth2/authorize?client_id=1039988982253092926&scope=bot&permissions=275683601487)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y210CCTA)

# USING

If you wish to use this bot locally, there are a few packages you need to install. These are:  
- hikari  
- hikari-lightbulb      /lightbulb  
- hikari-miru           /miru  
- python-dotenv         /dotenv  
- requests  
- pillow                /PIL  

Then, in the terminal, you need to run:  
```
python3 bot.py <echo/ache>
```
ECHO is the official bot.  ACHE is the testing bot in the dedicated testing server.  

# COMMANDS

This lists the commands per module in the source.  

**bold** shows the command name, if preceded by *italics*  it's a subcommand, with the italics being the command group.  
(items inside the parentheses are your inputs/variables/options, what ever you want to call it.)  
(*italics inside these parentheses mean it's optional*)  
[*italics inside these brackets show the command aliases*]  

### Administration (admn.py)

**ban** (user, *reason*): Bans a user from the server  
**unban** (user): Unbans a user from the server  
**kick** (user, reason): Kicks a user from the server  
**purge** (amount) [*clear*]: Deletes up to 100 messages in the channel used in  
*warn* **add** (user, *reason*): Warn a user  
*warn* **rmv** (user, timestamp): Remove a warn from a user, uses timestamps as warn ID (use *warn* **lst** to see)  
*warn* **lst** (user): Lists a user's warns   

### Economy (econ.py)

**balance** (*user*) [*bal*]: See a user's bank and wallet balance  
**deposit** (amount) [*dep*]: Deposit an amount into your bank (10% of net worth must remain in wallet)  
**withdraw** (amount) [*wd*, *with*]: Withdraw money into your wallet  
**gamble** (amount): Gamble your money, you might win!  
**leaderboard** (*page*) [*lb*]: See the leaderboard's richest people in the server  
**work**: Go to work (1hr cooldown)  
**daily**: Get your daily bonus (24hr cooldown)  
**weekly**: Get your weekly bonus (7d cooldown)  
**rob** (user): Rob someone for their money (1hr cooldown)  
**pay** (user, amount): Give someone your money  

### GIFs and Images (gifs.py)

**kill** (user): Kill a user  
**slap** (user): Slap a user  
**bonk** (user): Bonk a user  
**hbonk** (user): Horny bonk a user  
**boop** (user): Boop a user  
**boof** (user): Pass the boof to a user  
**bark** (user): Bark at a user  
**pat** (user): Headpat a user  
**wag** (user): Wag your tail at a user  
**hug** (user): Hug a user  
**floof**: Send a random fox  
**doggo**: Send a random dog  
**ducky**: Send a random duck  

### Information (info.py)

**ping**: Check the bot's latency  
**check**: Check if the bot can respond  
**uid**: Get the current user id  
**sid**: Get the current server id  
**avatar** (*user*) [*av*]: Get the avatar of a particular Discord user  
**userinfo** (*user*) [*whois*]: Get information about a particular Discord user  
**serverinfo** (*server*): Get information about a particular Discord server  

### Items and Inventory (item.py)

**shop** (*page*) [*store*, *market*]: See the available items to buy and their prices  
**buy** (item): Buy an item  
**inv** (*page*) [*inventory*]: Check your items  
**use** (item, *user*): Use an item (on a user if needed)  

### Luck and RNG (luck.py)

**dice** (amount, sides, *bonus*) [*roll*]: Roll a dice (example: /roll 1 d6 -2)  
**coin** [*flip*]: Flip a coin  
**8ball** (question): Ask the magic 8-ball something  
**rps** (hand): Play RPS against the random bot  
*rtg* **dndalign** (who): Align someone on the chaotic-lawful evil-good scales  
*rtg* **twunkscale** (who): Put someone on the twink-bear-hunk scale  
*rtg* **futchscale** (who): Put someone on the femme-butch scale  
*rtg* **smash_or_pass** (who) [*sop*]: Smash or pass someone  
*rtg* **susmeter** (who): Measure how sus someone is  

### Miscellaneous (misc.py)

**urban** (word): Look up a word's definition on Urban Dictionary  
**dict** (word): Look up a word's definition  
**xkcd** (*comic*): Pull a (random) XKCD comic  
**echo** (sentence) [*parrot*]: Repeat a sentence back  
**emojify** (sentence) [*emoji_echo*]: Replace letters with emoji's  
**cookie** [*cookie_count*, *cookies*]: Shows how many commands have been used since implementation.  

### Image Manipulation (pict.py)

**show_color** (color): Display a 256x256px image of a particular color  

### Games (play.py)

**weapon** (*sentence*): Generate a random weapon (place § where you want it to appear)  
**ninemaze** [*9maze*]: Small original RPG  
**chess**: Play chess against a really bad robot  

### Roles (role.py)

**role** (user, role): Add or remove a role from a user if they don't or do have it (switch)  
*role* **add** (user, role): Add a role to a user  
*role* **rmv** (user, role): Remove a role from a user  
*role* **in** (role): Lists all users that have a certain role  
*role* **list**: List all the roles in the server  
*role* **info** (role): Gets information about a role  
*role* **purge_role_members** (role to remove, role to look in) [*prm*]: Remove a certain role from members with a different role  
*role* **add_role_members** (role to add, role to add in) [*arm*]: Add a cartain role to members with a different role  

### Tags (tags.py)

*tag*: Regular server tags  
*g_tag*: Global tags added by the developer  

*(t)* **ena**: Enable tags  
*(t)* **dis**: Disable tags  
*(t/g)* **rec** (name): Send a tag  
*(t)* **crt** (name, content): Create a tag  
*(t)* **dlt** (name): Delete a tag  
*(t/g)* **lst**: Lists all tags  
