import discord
from discord.ext import commands
import aiohttp
import sys
import time
import functools
import datetime
import pytz


class utility:
    def __init__(self, bot):
	    self.bot = bot


    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
       if member is None:
          embed=discord.Embed(title="No mention!", description="Please mention a user to view his profile!", color=0xff0000)
          await ctx.send(embed=embed)
       else:
          embed = discord.Embed(title=f"{member}'s profile picture", color=0xeee657)
          embed.set_image(url=member.avatar_url)
          await ctx.send(embed=embed)

    @commands.command()
    async def code(self, ctx, *, msg):
           """Write text in code format."""
           await ctx.message.delete()
           await ctx.send("```" + msg.replace("`", "") + "```")

       
    @commands.command()
    async def echo(self, ctx, *, content:str):
           await ctx.send(content)
           await ctx.message.delete()
		
    
    @commands.command(aliases=['platform'],hidden=True)
    async def plat(self,ctx):
           await ctx.send('Running on ' + sys.platform)
	

    @commands.command(name='pingme')
    async def pingme(self, ctx):
        embed=discord.Embed(description =    ctx.author.mention,colour =    discord.Colour.red())
        await ctx.send(embed=embed)
	
    @commands.command()
    async def datetime(self, ctx, tz=None):
        """Get the current date and time for a time zone or UTC."""
        now = datetime.datetime.now(tz=pytz.UTC)
        all_tz = 'https://github.com/Techarpan/garena/blob/master/data/timezones.json'
        if tz:
            try:
                now = now.astimezone(pytz.timezone(tz))
            except:
                em = discord.Embed(color=discord.Color.red())
                em.title = "Invalid timezone"
                em.description = f'Please take a look at the [list]({all_tz}) of timezones.'
                return await ctx.send(embed=em)
        await ctx.send(f'It is currently {now:%A, %B %d, %Y} at {now:%I:%M:%S %p}.')

    @commands.group(invoke_without_command=True)
    async def isit(self, ctx):
        '''A command group to see the number of days until a holiday'''
        await ctx.send(f'`{ctx.prefix}isit halloween` Find the number of days until this spooky holiday!\n`{ctx.prefix}isit christmas` Are you naughty or nice?\n`{ctx.prefix}isit newyear` When is next year coming already?')

    @commands.group(invoke_without_command=True)
    async def whenis(self, ctx):
        '''A command group to see the number of days until a holiday'''
        await ctx.send(f'`{ctx.prefix}whenis whalloween` Find the number of days until this spooky holiday!')


    @isit.command()
    async def halloween(self, ctx):
        now = datetime.datetime.now()
        h = datetime.datetime(now.year, 10, 31)
        if now.month > 10:
            h = datetime.datetime(now.year + 1, 10, 31)
        until = h - now
        if now.month == 10 and now.day == 31:
            await ctx.send('It is Halloween! :jack_o_lantern: :ghost:')
        else:
            if until.days + 1 == 1:
                return await ctx.send('No, tomorrow is Halloween!')
            await ctx.send(f'No, there are {until.days + 1} more days until Halloween.')

    @isit.command()
    async def christmas(self, ctx):
        '''Is it Christmas?'''
        now = datetime.datetime.now()
        c = datetime.datetime(now.year, 12, 25)
        if now.month == 12 and now.day > 25:
            c = datetime.datetime((now.year + 1), 12, 25)
        until = c - now
        if now.month == 12 and now.day == 25:
            await ctx.send('Merry Christmas! :christmas_tree: :snowman2:')
        else:
            if until.days + 1 == 1:
                return await ctx.send('No, tomorrow is Christmas!')
            await ctx.send(f'No, there are {until.days + 1} more days until Christmas.')

    @isit.command()
    async def newyear(self, ctx):
        '''When is the new year?'''
        now = datetime.datetime.now()
        ny = datetime.datetime(now.year + 1, 1, 1)
        until = ny - now
        if now.month == 1 and now.day == 1:
            await ctx.send('It\'s New Years today! :tada:')
        else:
            if until.days + 1 == 1:
                return await ctx.send('No, tomorrow is New Year\'s Day!')
            await ctx.send(f'No, there are {until.days + 1} days left until New Year\'s Day.')


    @whenis.command(aliases=['hallo','hw'])
    async def whalloween(self, ctx):
        now = datetime.datetime.now()
        h = datetime.datetime(now.year, 10, 31)
        if now.month > 10:
            h = datetime.datetime(now.year + 1, 10, 31)
        until = h - now
        if now.month == 10 and now.day == 31:
            await ctx.send('It is Halloween! :jack_o_lantern: :ghost:')
        else:
            if until.days + 1 == 1:
                await ctx.send("Halloween is on 31st of October")
                return await ctx.send('One more day remaining for halloween!')
            await ctx.send("Halloween is on 31st of October")
            await ctx.send(f'That is {until.days + 1} days remaining for Halloween.')


def setup(bot):
    bot.add_cog(utility(bot))
