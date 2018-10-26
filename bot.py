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
        await bot.change_presence(activity=discord.Game(name='tmHack | Hacking...'))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name='tmHack | Upgrading...'))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name='tmHack | Stay Anonymous..'))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name='tmHack | -help'))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Activity(name='tmHack', type = discord.ActivityType.watching))
        await asyncio.sleep(30)

@bot.event
async def rename():
    while True:
        await bot.user.name.edit('[tmHack]Bot')
        await asyncio.sleep(20)
        await bot.user.name.edit('[tmHack]Official')
        await asyncio.sleep(20)
        await bot.user.name.edit('[tmHack]Beta Test')
        await asyncio.sleep(20)

@bot.event
async def on_ready():
    bot.loop.create_task(status_task()) 
    bot.loop.create_task(rename())
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
    embed.add_field(name="Poker", value="?help", inline=False)
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

bot.run(os.environ.get("TOKEN"))
