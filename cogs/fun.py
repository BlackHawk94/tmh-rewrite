#!/usr/bin/env python
# -*- coding: utf-8 -*-
import discord
import random
import asyncio
import json
from discord.ext import commands
import aiohttp, os, traceback
import time

ball = ["As I see it, yes", "It is certain", "It is decidedly so", "Most likely", "Outlook good",
"Signs point to yes", "Without a doubt", "Yes", "Yes – definitely", "You may rely on it", "Reply hazy, try again",
"Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
"Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]


class fun:
    def __init__(self, bot):
        self.bot = bot
        self.infections = {  #Infections
        }
        
    
    @commands.command()
    async def hugg(self, ctx, *, user: discord.Member = None):
        if user != None:        
            if user.id == 435492397258899467:
                embed=discord.Embed(description="{} you hugged the Creator of this bot ".format(ctx.message.author.name), color=0xff0000)
                embed.set_image(url="https://i.imgur.com/r9aU2xv.gif")
                embed.set_footer(text = "Thanks for hugging my master :)")
                await ctx.send(embed=embed)
            elif user.id == self.bot.user.id:
                embed=discord.Embed(description="{} you hugged the bot!".format(ctx.message.author.name),color=0xff0000)
                embed.set_image(url="https://i.imgur.com/r9aU2xv.gif")
                embed.set_footer(text = "Thanks for hugging me, Zarena will remember you")
                await ctx.send(embed=embed)
            elif user.id == ctx.message.author.id:
                embed=discord.Embed(title="hugged themself", description="{} was hugged by {}  ".format(user.mention, user.mention), color=0xff0000)
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/NHS-Logo.svg/1200px-NHS-Logo.svg.png")
                embed.set_image(url="http://animegif.ru/up/photos/album/oct17/171021_8687.gif")
                embed.set_footer(text="You seems to be forever alone")
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(description="{} was hugged by {}  ".format(user.mention, ctx.message.author.name),color=0x00ff00)
                embed.set_image(url="https://data.whicdn.com/images/45718472/original.gif")
                embed.set_footer(text= "You both are ")
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description="You haven't mentioned anyone to hug!", color=0xff0000)
            embed.set_footer(text = "No one to hug!! Sad!")
            await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, member : discord.Member):
        """<member>: Be careful with this one."""
        await self.bot.say("*slaps {0} around a bit with a large, girthy trout*".format(member))

    @commands.command()
    async def hug(self, ctx, *, user: discord.Member = None):
        if user != None:        
            if  member.id == ctx.message.author.id:
                embed=discord.Embed(description="{} you hugged the Creator of this bot ".format(ctx.message.author.name), color=0xff0000)
                await ctx.send(embed=embed)
            elif user.id == self.bot.user.id:
                embed=discord.Embed(description="{} you hugged the bot!".format(ctx.message.author.name),color=0xff0000)
                await ctx.send(embed=embed)
            elif user.id == ctx.message.author.id:
                embed=discord.Embed(title="hugged themself", description="{} was hugged by {}  ".format(user.mention, user.mention), color=0xff0000)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(description="{} was hugged by {}  ".format(user.mention, ctx.message.author.name),color=0x00ff00)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description="You haven't mentioned anyone to hug!", color=0xff0000)
            await ctx.send(embed=embed)
# user.id == 435492397258899467:

    @commands.command()
    async def coinflip(self, ctx):
        '''Select Random'''
        choice = random.randint(1,2)
        if choice == 1:
            await ctx.send("Tails")
        else:
            await ctx.send("Heads")

    @commands.command()
    async def greet(self, ctx):
         await ctx.send(":smiley: :wave: Hello, there!")
    
    @commands.command(hidden=True)
    async def hi(self, ctx):
        await ctx.send("Hello !")
        await ctx.message.delete()
        
    @commands.command()
    async def cat(self, ctx):
        await ctx.send("https://moderncat-wpengine.netdna-ssl.com/sites/default/files/images/uploads/ScienceKittens.gif")
        
    @commands.command()
    async def cookie(self, ctx, *, member: discord.Member = None):
        if member is None:
            embed=discord.Embed(title="No one to give!", description="You havent mentioned anyone to give :cookie:!", color=0xff0000)
            embed.set_footer(text = "Good enjoy your own cookie")
            await ctx.send(embed=embed)
        elif member.id == 435492397258899467: 
            await ctx.send(ctx.message.author.mention + " Thank you for giving :cookie: to the Creator of this bot.")
            
        elif member.id == ctx.message.author.id:
            embed=discord.Embed(title="Good", description="You gave :cookie: to yourself enjoy", color=0xff0000)
            embed.set_footer(text="~~You are good~~")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="given!", description="{} was given :cookie: by {} ".format(member.mention, ctx.message.author.name),color=0x00ff00)
            await ctx.send(embed=embed)


    @commands.command(description="For when you wanna settle the score some other way",hidden=True)
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(["Examples" ,"like" , "this" ,"dope" ,"rewrite" ,"tutorial"]))


    @commands.command()
    async def kill(self, ctx, *, member: discord.Member = None):
        if member is None:
            embed=discord.Embed(title="No one to kill!", description="You havent mentioned anyone to kill!", color=0xff0000)
            embed.set_thumbnail(url="http://i.imgur.com/6YToyEF.png")
            embed.set_footer(text = "I thought you are smart")
            await ctx.send(embed=embed)
        elif member.id == 435492397258899467:
            await ctx.send(ctx.message.author.mention + " LOL you can't kill the Creator of this bot.")
        elif member.id == self.bot.user.id:
            embed=discord.Embed(description="You can't kill the bot",color=0xff0000)
            await ctx.send(embed=embed)
        elif member.id == ctx.message.author.id:
            embed=discord.Embed(title="Call this number", description="1-800-784-2433", color=0xff0000)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/NHS-Logo.svg/1200px-NHS-Logo.svg.png")
            embed.set_image(url="http://4.bp.blogspot.com/-FL6mKTZOk94/UBb_9EuAYNI/AAAAAAAAOco/JWsTlyInMeQ/s400/Jean+Reno.gif")
            embed.set_footer(text="~~You are good~~")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Killed!", description="{} Was killed by {} OOF ".format(member.mention, ctx.message.author.name),color=0x00ff00)
            embed.set_image(url="https://media.giphy.com/media/kOA5F569qO4RG/giphy.gif")
            embed.set_footer(text= "RIP")
            await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, *, member: discord.Member = None):
        if member is None:
            embed=discord.Embed(title="No one to slap!", description="You havent mentioned anyone to slap!", color=0xff0000)
            embed.set_thumbnail(url="http://i.imgur.com/6YToyEF.png")
            embed.set_footer(text = "I thought you are not enough stupid")
            await ctx.send(embed=embed)
        elif member.id == 435492397258899467:
            await ctx.send(ctx.message.author.mention + " Ofc, you cant slap Creator of this bot.")
        elif member.id == ctx.member.id:
            await ctx.send('I am smart enough to understand you tried to troll me... Believe me, the stupid here is you, not me!')

        elif member.id == ctx.message.author.id:
            embed=discord.Embed(title="Call this number", description="1-800-784-2433", color=0xff0000)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/NHS-Logo.svg/1200px-NHS-Logo.svg.png")
            embed.set_image(url="https://media.giphy.com/media/pVi6sMBJhJ0E8/giphy.gif")
            embed.set_footer(text="~~You are good~~")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="slapped!", description="{} Was slapped by {} OOF ".format(member.mention, ctx.message.author.name),color=0x00ff00)
            embed.set_image(url="https://media.giphy.com/media/jLeyZWgtwgr2U/giphy.gif")
            embed.set_footer(text= "RIP")
            await ctx.send(embed=embed)

    @commands.command(name="8", aliases=["8ball"],hidden=True)
    async def eightball(self, ctx, *, question : str):
        "When u dont know what is good"
        if question.endswith("?") and question != "?":
            await ctx.send("`" + random.choice(ball) + "`")
        else:
            await ctx.send("`That dosen't looks like a question`")
    
    @commands.command(pass_context=True, no_pm=True)
    async def stupid(self, ctx, user : discord.Member = None):
        """Check Whether Mentioned user is stupid"""
        if user != None:
            if ctx.message.author.id == 435492397258899467:
                await ctx.send(f'Oh, Creator! You\'re the intelligent person I\'ve ever seen! You definitely are right! {user.mention} is really stupid!')
            elif user.id == self.bot.user.id:
                await ctx.send('I am smart enough to understand you tried to troll me... Believe me, the stupid here is you, not me!')
            elif user.id == 435492397258899467:
                await ctx.send(ctx.message.author.mention + " Ofc, you are stupid, if you are saying stupid to Creator of this bot.")
            else:
                await (f'Hmm perhaps, I\'m not sure if {user.mention} is stupid, but I\'m sure YOU are!')
        else:
            await ctx.send(ctx.message.author.mention + " No Doubt, you are ofc Stupid, if you didn't mentioned anyone.")
    
    @commands.command()
    async def face(self, ctx):
        faces=["¯\_(ツ)_/¯", "̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\З= ( ▀ ͜͞ʖ▀) =Ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿", "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)", "ʕ•ᴥ•ʔ", "(▀̿Ĺ̯▀̿ ̿)", "(ง ͠° ͟ل͜ ͡°)ง", "༼ つ ◕_◕ ༽つ", "ಠ_ಠ", "(づ｡◕‿‿◕｡)づ", "̿'̿'\̵͇̿̿\З=( ͠° ͟ʖ ͡°)=Ε/̵͇̿̿/'̿̿ ̿ ̿ ̿ ̿ ̿", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ✧ﾟ･: *ヽ(◕ヮ◕ヽ)", "┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴", "( ͡°╭͜ʖ╮͡° )", "(͡ ͡° ͜ つ ͡͡°)", "(• ε •)", "(ง'̀-'́)ง", "(ಥ﹏ಥ)", "(ノಠ益ಠ)ノ彡┻━┻", "[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "(☞ﾟ∀ﾟ)☞", "| (• ◡•)| (❍ᴥ❍ʋ)", "(◕‿◕✿)", "(ᵔᴥᵔ)", "(¬‿¬)", "(☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)", "(づ￣ ³￣)づ", "ლ(ಠ益ಠლ)", "ಠ╭╮ಠ", "̿ ̿ ̿'̿'\̵͇̿̿\з=(•_•)=ε/̵͇̿̿/'̿'̿ ̿", "(;´༎ຶД༎ຶ`)", "༼ つ  ͡° ͜ʖ ͡° ༽つ", "(╯°□°）╯︵ ┻━┻"]
        face=random.choice(faces)
        await ctx.send(face)

    @commands.command()
    async def tableflip(self, ctx):
        x = await ctx.send(content="┬─┬ノ( º _ ºノ)")
        await asyncio.sleep(1)
        await x.edit(content='(°-°)\\ ┬─┬')
        await asyncio.sleep(1)
        await x.edit(content='(╯°□°)╯    ]')
        await asyncio.sleep(0.2)
        await x.edit(content='(╯°□°)╯  ︵  ┻━┻')
      
    
    @commands.command()
    async def joke(self, ctx):
        jokes=["not actually pinging server...", "hey bb", "what am I doing with my life",
                              "Some Dragon is a dank music bot tbh", "I'd like to thank the academy for this award",
                              "The NSA is watching 👀", "`<Insert clever joke here>`", "¯\_(ツ)_/¯", "(づ｡◕‿‿◕｡)づ",
                              "I want to believe...", "Hypesquad is a joke", "EJH2#0330 is my daddy", "Robino pls",
                              "Seth got arrested again...", "Maxie y u do dis", "aaaaaaaaaaaAAAAAAAAAA", "owo",
                              "uwu", "meme team best team", "made with dicksword dot pee why", "I'm running out of "
                                                                                               "ideas here",
                              "am I *dank* enough for u?", "this is why we can't have nice things. come on",
                              "You'll understand when you're older...", "\"why\", you might ask? I do not know...",
                              "I'm a little tea pot, short and stout", "I'm not crying, my eyeballs "
                                                                       "are sweating!",
                              "When will the pain end?", "Partnership when?", "Hey Robino, rewrite when?"]
        joke=random.choice(jokes)
        await ctx.send(joke)
    
    @commands.command()
    async def meme(self, ctx):
        """Pulls a random meme from r/me_irl"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.reddit.com/r/me_irl/random") as r:
                data = await r.json()
                await ctx.send(data[0]["data"]["children"][0]["data"]["url"])
     

    @commands.command()
    async def quotes(self, ctx):
        """*quotes
        A command that will return a random quotation.
        """
        self.session = aiohttp.ClientSession()
        params = {'method': 'getQuote', 'lang': 'en', 'format': 'json'}
        async with self.session.get('https://api.forismatic.com/api/1.0/', params=params) as response:
            data = await response.json()

            embed = discord.Embed(colour=discord.Colour.purple())
            embed.add_field(name=data['quoteText'], value=f"- {data['quoteAuthor']}")

            await ctx.send(embed=embed)
            
    @commands.command()
    async def repeat(self, ctx, amount: int, *, message):
        if amount <= 5:
            for i in range(amount):
                await ctx.send(message)     
        else:
            await ctx.send('Please use a number less than or equal to five.')
            
    @commands.command()
    async def reverse(self, ctx, *, message):
        message = message.split()
        await ctx.send(' '.join(reversed(message)))

    @commands.command(hidden=True)
    async def sendv(self, ctx, *, msg):
        channel = self.bot.get_channel(468517209325436932)
        await channel.send(msg)
        
    @commands.command(hidden=True)
    async def sendt(self, ctx, *, msg):
        channel = self.bot.get_channel(466630946746007583)
        await channel.send(msg)
     
    @commands.command()
    async def hack(self, ctx, user: discord.Member):
        """Hack someone's account! Try it!"""
        msg = await ctx.send(f"Hacking! Target: {user}")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files... [▓▓    ]")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files... [▓▓▓   ]")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files... [▓▓▓▓▓ ]")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files... [▓▓▓▓▓▓▓ ]")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files... [▓▓▓▓▓▓▓▓▓ ]")
        await asyncio.sleep(2)
        await msg.edit(content="Accessing Discord Files COMPLETE! [▓▓▓▓▓▓▓▓▓▓▓]")
        await asyncio.sleep(2)
        await msg.edit(content="Retrieving Login Info... [▓▓▓    ]")
        await asyncio.sleep(3)
        await msg.edit(content="Retrieving Login Info... [▓▓▓▓▓ ]")
        await asyncio.sleep(3)
        await msg.edit(content="Retrieving Login Info... [▓▓▓▓▓▓ ]")
        await asyncio.sleep(4)
        await msg.edit(content=f"An error has occurred hacking {user}'s account. Please try again later. ❌") 

    @commands.command()
    async def virus(self, ctx,user: discord.Member=None,*,hack=None):
        """Inject a virus into someones system."""
        name = ctx.message.author
        if not hack:
            hack = 'discord'
        else:
            hack = hack.replace(' ','-')
        channel = ctx.message.channel
        msg = await channel.send(content=f"``[▓▓▓                    ] / {hack}-virus.exe Packing files.``")
        await asyncio.sleep(1.5)
        await msg.edit(content=f"``[▓▓▓▓▓▓▓                ] - {hack}-virus.exe Packing files..``")
        await asyncio.sleep(0.3)
        await msg.edit(content=f"``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {hack}-virus.exe Packing files...``")
        await asyncio.sleep(1.2)
        await msg.edit(content=f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {hack}-virus.exe Initializing code.``")
        await asyncio.sleep(1)
        await msg.edit(content=f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {hack}-virus.exe Initializing code..``")
        await asyncio.sleep(1.5)
        await msg.edit(content=f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {hack}-virus.exe Finishing.``")
        await asyncio.sleep(1)
        await msg.edit(content=f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {hack}-virus.exe Finishing..``")
        await asyncio.sleep(1)
        await msg.edit(content=f"``Successfully downloaded {hack}-virus.exe``")
        await asyncio.sleep(2)
        await msg.edit(content="``Injecting virus.   |``")
        await asyncio.sleep(0.5)
        await msg.edit(content="``Injecting virus..  /``")
        await asyncio.sleep(0.5)
        await msg.edit(content="``Injecting virus... -``")
        await asyncio.sleep(0.5)
        await msg.edit(content="``Injecting virus....\``")
        await msg.delete()
       
        if user:
            await ctx.send('`{}-virus.exe` successfully injected into **{}**\'s system.'.format(hack,user.name))
            await ctx.send(content=f"**Alert!**\n``You may have been hacked. {hack}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``")
        else:
            await ctx.send('**{}** has hacked himself ¯\_(ツ)_/¯.'.format(name.name))
            await ctx.send(content=f"**Alert!**\n``You may have been hacked. {hack}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``")

    @commands.command()
    async def infect(self, ctx, user: discord.Member = None, emoji=None):
	    'Infects a user'
	    if (user is None) or (emoji is None):
		    return await ctx.send('Please provide a user and a emoji. Do `c!help infect` for more info')
			
	    emoji = self.bot.get_emoji(int(emoji.split(':')[2].strip('>'))) if '<:' in emoji or '<a:' in emoji else emoji 

	    def check(msg):
		    return ctx.guild.id == msg.guild.id and msg.author.id == user.id

	    async def infect_task(self):
		    await ctx.channel.send(((('`' + user.name) + '` has been infected with ') + str(emoji)) + ' for **one** hour')
		    start = time.monotonic()
		    while time.monotonic() - start < (60*60):
			    m = await self.bot.wait_for('message', check=check)
			    try:
				    await m.add_reaction(emoji)
			    except (discord.Forbidden, discord.HTTPException, discord.NotFound, discord.InvalidArgument):
				    pass
		    del self.infections[str(user.id) + ';' + str(ctx.guild.id)]

	    inf = self.infections.get((str(user.id) + ';') + str(ctx.guild.id), None)
	    if inf is not None:
		    return await ctx.send(('`' + user.name) + '` is already infected')
			
	    try:
		    await ctx.message.add_reaction(emoji)
	    except:
		    return await ctx.send('Emoji not found')
			
	    infection = self.bot.loop.create_task(infect_task(self))
	    self.infections.update({str(user.id) + ';' + str(ctx.guild.id): infection})

    @commands.command()
    async def heal(self, ctx, user: discord.Member = None):
	    'Heals a user from a infection'
	    if user is None:
		    await ctx.send('Please provide a user. Do `c!help heal` for more info')
		    return
	    if (user == ctx.author) and (ctx.author.id != 435492397258899467):
		    await ctx.send("You can't heal yourself")
		    return
	    inf = self.infections.get((str(user.id) + ';') + str(ctx.guild.id), None)
	    if inf is not None:
		    inf.cancel()
		    del self.infections[str(user.id) + ';' + str(ctx.guild.id)]
		    await ctx.send(('`' + user.name) + '` has been healed')
	    else:
		    await ctx.send(('`' + user.name) + '` was not infected')

    @commands.command()
    async def fist(self, ctx, user: discord.Member = None):
	    'Fists a user'
	    if user is None:
		    user = ctx.author
	    edits = 4
	    spaces = 12
	    time_to_wait = 0.4
	    msg = await ctx.send((user.mention + ('\t' * int(edits * spaces))) + ':left_facing_fist:')
	    for i in range(edits):
		    edits -= 1
		    await asyncio.sleep(time_to_wait)
		    await msg.edit(content=(user.mention + ('\t' * int(edits * spaces))) + ':left_facing_fist:')
		    if edits == 0:
			    await msg.edit(content=':boom: <----- This is you ' + user.mention)

def setup(bot):
    bot.add_cog(fun(bot))
