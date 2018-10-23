import discord
from discord.ext import commands
from discord.ext.commands import Bot
import time
from datetime import datetime
import asyncio
import inspect
import json
from contextlib import redirect_stdout
import io
import os
from os import listdir
from os.path import isfile, join
import sys, traceback
import textwrap

def get_prefix(bot, message):
    prefixes = ['-']
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)

cogs_dir = "cogs"
bot = commands.Bot(command_prefix=get_prefix, description='Rewrite Cog')
bot.launch_time = datetime.utcnow()
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')

def dev_check(id):
    with open('data/devs.json') as f:
        devs = json.load(f)
        if id in devs:
            return True
        return False

@bot.event 
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name='tmHack | -help'))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Activity(name='tmHack', type = discord.ActivityType.watching))
        await asyncio.sleep(30)       

@bot.event
async def on_ready():
    bot.loop.create_task(status_task()) 
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot._last_result = None
@bot.command(name='eval')
async def _eval(ctx, *, body):
    """Evaluates python code"""
    if not dev_check(ctx.author.id):
        return await ctx.send("You cannot use this because you are not a developer.")
    env = {
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': bot._last_result,
        'source': inspect.getsource
    }

    env.update(globals())
    body = cleanup_code(body)
    stdout = io.StringIO()
    err = out = None
    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
    def paginate(text: str):
        '''Simple generator that paginates text.'''
        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != '', pages))

    try:
        exec(to_compile, env)
    except Exception as e:
        err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        return await ctx.message.add_reaction('\u2049')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        if ret is None:
            if value:
                try:

                    out = await ctx.send(f'```py\n{value}\n```')
                except:
                    paginated_text = paginate(value)
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')
        else:
            bot._last_result = ret
            try:
                out = await ctx.send(f'```py\n{value}{ret}\n```')
            except:
                paginated_text = paginate(f"{value}{ret}")
                for page in paginated_text:
                    if page == paginated_text[-1]:
                        out = await ctx.send(f'```py\n{page}\n```')
                        break
                    await ctx.send(f'```py\n{page}\n```')

    if out:
        await ctx.message.add_reaction('\u2705')  # tick
    elif err:
        await ctx.message.add_reaction('\u2049')  # x
    else:
        await ctx.message.add_reaction('\u2705')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="welcome")
    embed = discord.Embed(title="Welcome " + f'{member.name}' + " to " + f'{member.guild}' + " !", description="Take a look on the #rules of this server and Start to chat with your friends here #general", color=0xeee657) 
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)

bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="tmHack[Official] bot", description="A cool multipurpose bot. List of Categories are:", color=0x007FFF)
    embed.add_field(name="Fun", value="greet | cookie | coinflip | face | fist | tableflip | quotes", inline=False)
    embed.add_field(name="Info", value="avatar | userinfo | serverinfo", inline=False)
    embed.add_field(name="Utility", value="code | intro | suggest | report | uptime | ping ", inline=False)
    embed.add_field(name="eval", value="Executes python code", inline=False)
    embed.set_footer(text="As the bot is under development, so there may be some bugs in commands.)")
    await ctx.send(embed=embed)

@bot.command(aliases=['fb'])
async def feedback(ctx, *, msg):
    member=ctx.author
    channel = discord.utils.get(member.guild.channels, name="logs")
    embed = discord.Embed(colour=ctx.author.colour)
    embed.add_field(name='User', value=ctx.author.name)
    embed.add_field(name='User ID', value=ctx.author.id, inline=True)
    embed.add_field(name='Server', value=ctx.guild.name, inline=True)
    embed.add_field(name='Server ID', value=ctx.guild.id, inline=True)
    embed.add_field(name='Message', value=msg)
    embed.add_field(name='Time', value=ctx.message.created_at)  
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_author(name=f'{ctx.message.author}'+" has submitted a feedback", icon_url=None or ctx.author.avatar_url)
    await channel.send(embed=embed)
    await ctx.send("Thank you!! Your feedback will be sent to the developer")
    await ctx.message.delete()

@bot.command(aliases=['rep'])
async def report(ctx,member: discord.Member=None,*,msg):
    channel = discord.utils.get(member.guild.channels, name="logs")
    if member is None:
        embed=discord.Embed(title="", description="You havent mentioned anyone to report!", color=0xff0000)          
        await ctx.send(embed=embed)
    else:  
        embed = discord.Embed(colour=ctx.author.colour)
        embed.add_field(name='Reported by - ', value=ctx.author.name)
        embed.add_field(name='Time', value=ctx.message.created_at)
        embed.add_field(name='Reason', value=msg)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=f'{ctx.message.author}'+" has been reported", icon_url=None or ctx.author.avatar_url)
        await channel.send(embed=embed)
        await ctx.send("Thank you!! Member had been reported")
        await ctx.message.delete()

@bot.command(aliases=['sug'])
async def suggest(ctx,*,msg):
    member=ctx.author
    channel = discord.utils.get(member.guild.channels, name="suggestions")
    embed = discord.Embed(colour=ctx.author.colour)
    embed.add_field(name='Suggested by - ', value=ctx.author.name)
    embed.add_field(name='Time', value=ctx.message.created_at)
    embed.add_field(name='Suggestion', value=msg)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_author(name=f'{ctx.message.author}'+" has submitted a suggestion", icon_url=None or ctx.author.avatar_url)
    await channel.send(embed=embed)
    await ctx.send("Thank you for your suggestion !!")
    await ctx.message.delete()

@bot.command()
async def intro(ctx):
    guild = ctx.guild
    embed = discord.Embed(colour=ctx.author.colour)
    embed.add_field(name="tmHack[Official]", value="tmHack is a simulation game that features international hacking attacks and defende. The third world war has started, but nations are not employing firepower anymore. A lot of hackers have been hired to enhance nation's IT power. Your mission is to attack the other hackers and their national servers. Those are the power and the wealth of each country. Use your knowledge and fight for your country!")
    embed.set_thumbnail(url=None or guild.icon_url)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed=discord.Embed(title=None, description=':ping_pong: Ping: {} ms'.format(bot.latency * 1000), color=0x2874A6)
    await ctx.send(embed=embed)
	
@bot.command()
async def ultraping(ctx):
        start = time.monotonic()
        msg = await ctx.send('Pinging...')
        millis = (time.monotonic() - start) * 1000
        heartbeat = ctx.bot.latency * 1000
        embed = discord.Embed(title=":ping_pong: Bot's Latency", description="The bot received your latency request.", color=0x2874A6)     
        embed.add_field(name="Heartbeat", value=f' {heartbeat:,.2f}ms.', inline=False)
        embed.add_field(name="ACK", value=f' {millis:,.2f}ms', inline=False)
        await msg.edit(embed=embed)

@bot.command()
async def hb(self, ctx):
    await ctx.send("Heartbeat ensures the other side is still there, if you don't respond to a heartbeat with a heartbeat ack, discord will assume the connection is dead and disconnect the websocket.\nLikewise, good libraries will disconnect if no heartbeat ack is received from Discord after sending a heartbeat.\nHeartbeat is like... once every 40 seconds or so. It depends on what the gateway suggests the heartbeat should benote the word *suggests* you can ping every 5 seconds if you wanted, but then discord will likely detect API abuse and reset your token\nhttps://cdn.discordapp.com/attachments/392215236612194305/475316704872890388/Selection_073.png\nhttps://media.discordapp.net/attachments/392215236612194305/475316717631963156/Selection_074.png%22")
            
@bot.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

from collections import namedtuple
import os
from typing import List
from subprocess import Popen

import discord
import random

from game import Game, GAME_OPTIONS, GameState

import pot

client = discord.Client()
games = {}

# Starts a new game if one hasn't been started yet, returning an error message
# if a game has already been started. Returns the messages the bot should say
def new_game(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        game.new_game()
        game.add_player(message.author)
        game.state = GameState.WAITING
        return ["A new game has been started by {}!".format(message.author.mention),
                "Message ?join to join the game."]
    else:
        messages = ["There is already a game in progress, "
                    "you can't start a new game."]
        if game.state == GameState.WAITING:
            messages.append("It still hasn't started yet, so you can still "
                            "message ?join to join that game.")
        return messages

# Has a user try to join a game about to begin, giving an error if they've
# already joined or the game can't be joined. Returns the list of messages the
# bot should say
def join_game(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["No game has been started yet for you to join.",
                "Message ?newgame to start a new game."]
    elif game.state != GameState.WAITING:
        return ["The game is already in progress, {}.".format(message.author.name),
                "You're not allowed to join right now."]
    elif game.add_player(message.author):
        return ["{} has joined the game!".format(message.author.mention),
                "Message ?join to join the game, "
                "or ?start to start the game."]
    else:
        return ["You've already joined the game {}!".format(message.author.mention)]

# Starts a game, so long as one hasn't already started, and there are enough
# players joined to play. Returns the messages the bot should say.
def start_game(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["Message ?newgame if you would like to start a new game."]
    elif game.state != GameState.WAITING:
        return ["The game has already started, {}.".format(message.author.mention),
                "It can't be started twice."]
    elif not game.is_player(message.author):
        return ["You are not a part of that game yet, {}.".format(message.author.mention),
                "Please message ?join if you are interested in playing."]
    elif len(game.players) < 2:
        return ["The game must have at least two players before "
                "it can be started."]
    else:
        return game.start()

# Deals the hands to the players, saying an error message if the hands have
# already been dealt, or the game hasn't started. Returns the messages the bot
# should say
def deal_hand(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["No game has been started for you to deal. "
                "Message ?newgame to start one."]
    elif game.state == GameState.WAITING:
        return ["You can't deal because the game hasn't started yet."]
    elif game.state != GameState.NO_HANDS:
        return ["The cards have already been dealt."]
    elif game.dealer.user != message.author:
        return ["You aren't the dealer, {}.".format(message.author.name),
                "Please wait for {} to !deal.".format(game.dealer.user.name)]
    else:
        return game.deal_hands()

# Handles a player calling a bet, giving an appropriate error message if the
# user is not the current player or betting hadn't started. Returns the list of
# messages the bot should say.
def call_bet(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["No game has been started yet. Message ?newgame to start one."]
    elif game.state == GameState.WAITING:
        return ["You can't call any bets because the game hasn't started yet."]
    elif not game.is_player(message.author):
        return ["You can't call, because you're not playing, "
                "{}.".format(message.author.name)]
    elif game.state == GameState.NO_HANDS:
        return ["You can't call any bets because the hands haven't been "
                "dealt yet."]
    elif game.current_player.user != message.author:
        return ["You can't call {}, because it's ".format(message.author.name),
                "{}'s turn.".format(game.current_player.user.name)]
    else:
        return game.call()

# Has a player check, giving an error message if the player cannot check.
# Returns the list of messages the bot should say.
def check(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["No game has been started yet. Message ?newgame to start one."]
    elif game.state == GameState.WAITING:
        return ["You can't check because the game hasn't started yet."]
    elif not game.is_player(message.author):
        return ["You can't check, because you're not playing, "
                "{}.".format(message.author.name)]
    elif game.state == GameState.NO_HANDS:
        return ["You can't check because the hands haven't been dealt yet."]
    elif game.current_player.user != message.author:
        return ["You can't check, {}, because it's ".format(message.author.name),
                "{}'s turn.".format(game.current_player.user.name)]
    elif game.current_player.cur_bet != game.cur_bet:
        return ["You can't check, {} because you need to ".format(message.author.name),
                "put in ${} to ".format(game.cur_bet - game.current_player.cur_bet),
                "call."]
    else:
        return game.check()

# Has a player raise a bet, giving an error message if they made an invalid
# raise, or if they cannot raise. Returns the list of messages the bot will say
def raise_bet(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["No game has been started yet. Message ?newgame to start one."]
    elif game.state == GameState.WAITING:
        return ["You can't raise because the game hasn't started yet."]
    elif not game.is_player(message.author):
        return ["You can't raise, because you're not playing, "
                "{}.".format(message.author.name)]
    elif game.state == GameState.NO_HANDS:
        return ["You can't raise because the hands haven't been dealt yet."]
    elif game.current_player.user != message.author:
        return ["You can't raise, {}, because it's ".format(message.author.name),
                "{}'s turn.".format(game.current_player.name)]

    tokens = message.content.split()
    if len(tokens) < 2:
        return ["Please follow ?raise with the amount that you would "
                "like to raise it by."]
    try:
        amount = int(tokens[1])
        if game.cur_bet >= game.current_player.max_bet:
            return ["You don't have enough money to raise the current bet "
                    "of ${}.".format(game.cur_bet)]
        elif game.cur_bet + amount > game.current_player.max_bet:
            return ["You don't have enough money to raise by ${}.".format(amount),
                    "The most you can raise it by is "
                    "${}.".format(game.current_player.max_bet - game.cur_bet)]
        return game.raise_bet(amount)
    except ValueError:
        return ["Please follow !raise with an integer. "
                "'{}' is not an integer.".format(tokens[1])]

# Has a player fold their hand, giving an error message if they cannot fold
# for some reason. Returns the list of messages the bot should say
def fold_hand(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["No game has been started yet. "
                "Message ?newgame to start one."]
    elif game.state == GameState.WAITING:
        return ["You can't fold yet because the game hasn't started yet."]
    elif not game.is_player(message.author):
        return ["You can't fold, because you're not playing, "
                "{}.".format(message.author.name)]
    elif game.state == GameState.NO_HANDS:
        return ["You can't fold yet because the hands haven't been dealt yet."]
    elif game.current_player.user != message.author:
        return ["You can't fold {}, because it's ".format(message.author.name),
                "{}'s turn.".format(game.current_player.name)]
    else:
        return game.fold()

# Returns a list of messages that the bot should say in order to tell the
# players the list of available commands.
def show_poker(game: Game, message: discord.Message) -> List[str]:
    longest_command = len(max(commands, key=len))
    poker_lines = []
    for command, info in sorted(commands.items()):
        spacing = ' ' * (longest_command - len(command) + 2)
        poker_lines.append(command + spacing + info[0])
    return ['```' + '\n'.join(poker_lines) + '```']

# Returns a list of messages that the bot should say in order to tell the
# players the list of settable options.
def show_options(game: Game, message: discord.Message) -> List[str]:
    longest_option = len(max(game.options, key=len))
    longest_value = max([len(str(val)) for key, val in game.options.items()])
    option_lines = []
    for option in GAME_OPTIONS:
        name_spaces = ' ' * (longest_option - len(option) + 2)
        val_spaces = ' ' * (longest_value - len(str(game.options[option])) + 2)
        option_lines.append(option + name_spaces + str(game.options[option])
                            + val_spaces + GAME_OPTIONS[option].description)
    return ['```' + '\n'.join(option_lines) + '```']

# Sets an option to player-specified value. Says an error message if the player
# tries to set a nonexistent option or if the option is set to an invalid value
# Returns the list of messages the bot should say.
def set_option(game: Game, message: discord.Message) -> List[str]:
    tokens = message.content.split()
    if len(tokens) == 2:
        return ["You must specify a new value after the name of an option "
                "when using the ?set command."]
    elif len(tokens) == 1:
        return ["You must specify an option and value to set when using "
                "the ?set command."]
    elif tokens[1] not in GAME_OPTIONS:
        return ["'{}' is not an option. Message ?options to see ".format(tokens[1]),
                "the list of options."]
    try:
        val = int(tokens[2])
        if val < 0:
            return ["Cannot set {} to a negative value!".format(tokens[1])]
        game.options[tokens[1]] = val
        return ["The {} is now set to {}.".format(tokens[1], tokens[2])]
    except ValueError:
        return ["{} must be set to an integer, and '{}'".format(tokens[1], tokens[2]),
                " is not a valid integer."]

# Returns a list of messages that the bot should say to tell the players of
# the current chip standings.
def chip_count(game: Game, message: discord.Message) -> List[str]:
    if game.state in (GameState.NO_GAME, GameState.WAITING):
        return ["You can't request a chip count because the game "
                "hasn't started yet."]
    return ["{} has ${}.".format(player.user.name, player.balance)
            for player in game.players]

# Handles a player going all-in, returning an error message if the player
# cannot go all-in for some reason. Returns the list of messages for the bot
# to say.
def all_in(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["No game has been started yet. Message ?newgame to start one."]
    elif game.state == GameState.WAITING:
        return ["You can't go all in because the game hasn't started yet."]
    elif not game.is_player(message.author):
        return ["You can't go all in, because you're not playing, "
                "{}.".format(message.author.name)]
    elif game.state == GameState.NO_HANDS:
        return ["You can't go all in because the hands haven't "
                "been dealt yet."]
    elif game.current_player.user != message.author:
        return ["You can't go all in, {}, because ".format(message.author.name),
                "it's {}'s turn.".format(game.current_player.user.name)]
    else:
        return game.all_in()

# Ends the game
def end_game(game: Game, message: discord.Message) -> List[str]:
	if(message.author.top_role.permissions.administrator):
		game.players = []
		if game.state == GameState.WAITING:
			game.state = GameState.NO_GAME
			return ["The game was ended before it even begun!"]
		elif game.state in (GameState.NO_HANDS, GameState.HANDS_DEALT):
			game.state = GameState.NO_GAME
			return ["Alright people, fun's over, game ended"]
		elif game.state in (GameState.FLOP_DEALT, GameState.TURN_DEALT, GameState.RIVER_DEALT):
			game.state = GameState.NO_GAME
			return ["Alright people, fun's over, someone interrupted the dealing"]
		else:
			return ["I have no idea what just happened, ",
					"but I think you just tried to end a game that wasn't even started! ",
					"That's almost as bad as folding like Antonio!"]
	else:
		return ["I'm sorry {}, I'm afraid I can't let you do that!".format(message.author.mention)]

def kill(game: Game, message: discord.Message) -> List[str]:
	if(message.author.top_role.permissions.administrator):
		game.players = []
		game.state = GameState.NO_GAME
		exit()
	else:
		return ["I'm sorry {}, I'm afraid I can't let you do that!".format(message.author.mention)]

def creator(game: Game, message: discord.Message) -> List[str]:
    longest_command = len(max(commands, key=len))
    poker_lines = []
    for command, info in sorted(commands.items()):
        spacing = ' ' * (longest_command - len(command) + 2)
        poker_lines.append(command + spacing + info[0])
    return ["MichaelTecnoGod#7231 for Raykon Studio TEAM"]
		
# DONT YOU EVER DARE TRY TO FIDDLE WITH THIS AGAIN UNLESS IT BREAKS!
def leave(game: Game, message: discord.Message) -> List[str]:
    if game.state == GameState.NO_GAME:
        return ["Theres no game to leave!"]
    else:
        usr = message.author.name
        print("{} LEAVE START".format(usr))
        i = 0
        while i < len(game.players):
            player = game.players[i]
            print("+CurrentUser {} Has name {}".format(player,player.user.name))
            if player.user.name == usr:
                print("++FoundMatch {}, GamePlayers pre-pop {}".format(player.user.name == usr, game.players))
                tmp = game.players.pop(i)
                print("+++Popped {}@{}, GamePlayers after-pop {}".format(tmp, tmp.user.name, game.players))
                if len(game.players) == 0:
                	print("++++No players in GamePlayers: {} Ending game".format(game.players))
                	game.players = []
                	game.state = GameState.NO_GAME
                	print("{} LEFT".format(usr))
                	return ["Congrats, you just killed a game you started for no reason!",
                	        "Have you no consideration for the cycles you just wasted?"]
                if len(game.players) > 1:
                    game.pot.handle_fold(player)
                    game.leave_hand(player)
                    print("++++More than one player in GamePlayers: {}\n++++Popped user location: {}".format(game.players, tmp))
                    try:
                        if game.turn_index > len(game.in_hand):
                            game.turn_index = len(game.in_hand)-1
                        if game.dealer_index > len(game.players):
                        	game.dealer_index = len(game.players)-1
                    except:
                        print("******************[!] EXCEPTION TRYING TO SET INDICES [!]******************")
                    return ["**{}** Dropped out!".format(usr),
                           "**{}** is dealer and its **{}'s** turn!\n".format(game.players[game.dealer_index].user.mention,
                           game.in_hand[game.turn_index].user.mention)]
                elif len(game.players) == 1:
                    print("++++One player, win by default: {}".format(game.players))
                    # There's only one player, so they win
                    if game.state == GameState.WAITING:
                        game.state = GameState.NO_GAME
                        return ["Woops! Looks like **{}** dosen't wanna play after all!".format(usr)]
                    else:
                        game.state = GameState.NO_GAME
                        return ["**{}** wins the game due to the forfeit of {}".format(game.players[0].user.mention, usr)]
            else:
                i+=1
        return ["You're not even in the game {}".format(message.author.mention)]

def botrestart(game: Game, message: discord.Message) -> List[str]:
	if(message.author.top_role.permissions.administrator):
		p = Popen("run.bat")
		kill(game, message)
	else:
		return ["I'm sorry {}, I'm afraid I can't let you do that!".format(message.author.mention)]


Command = namedtuple("Command", ["description", "action"])

# The commands avaliable to the players
commands = {
    '?newgame': Command('Starts a new game, allowing players to join.',
                        new_game),
    '?join':    Command('Lets you join a game that is about to begin',
                        join_game),
    '?start':   Command('Begins a game after all players have joined',
                        start_game),
    '?deal':    Command('Deals the hole cards to all the players',
                        deal_hand),
    '?call':    Command('Matches the current bet',
                        call_bet),
    '?raise':   Command('Increase the size of current bet',
                        raise_bet),
    '?check':   Command('Bet no money',
                        check),
    '?fold':    Command('Discard your hand and forfeit the pot',
                        fold_hand),
    '?poker':    Command('Show the list of commands',
                        show_poker),
    '?options': Command('Show the list of options and their current values',
                        show_options),
    '?set':     Command('Set the value of an option',
                        set_option),
    '?count':   Command('Shows how many chips each player has left',
                        chip_count),
    '?all-in':  Command('Bets the entirety of your remaining chips',
                        all_in),
    '?endgame': Command('End the game',
    					end_game),
    '?kill':    Command('Kill the bot!',
    					kill),
    '?leave':   Command('Leave the game',
    					leave),
    '?restart': Command('Restart the bot',
    					botrestart),
	'?creator': Command('See who developed me',
						creator),
}

@client.event
async def on_ready():
    print("All systems are Online!")
    print("Thank you for using Poker Bot!")
    session = random.randint(1000000000, 9999999999)
    print("Session id {}\n\n".format(session))

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    # Ignore empty messages
    if len(message.content.split()) == 0:
        return
    # Ignore private messages
    if message.channel.is_private:
        return

        game = games.setdefault(message.channel, Game())
        messages = commands[command][1](game, message)

        # The messages to send to the channel and the messages to send to the
        # players individually must be done seperately, so we check the messages
        # to the channel to see if hands were just dealt, and if so, we tell the
        # players what their hands are.
        if command == '?deal' and messages[0] == 'The hands have been dealt!':
            await game.tell_hands(client)

        await client.send_message(message.channel, '\n'.join(messages))

bot.run(os.environ.get("TOKEN"))
client.run(os.environ.get("TOKEN"))