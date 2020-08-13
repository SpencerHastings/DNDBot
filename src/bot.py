import discord
from discord.ext import commands
from .settings import prefix
from .commands.ping import ping
from .commands.roll import roll

bot = commands.Bot(command_prefix=prefix)

@bot.command()
@commands.has_role('Bot Master')
async def stop(ctx):
    await ctx.send('Stopping')
    print('Stopping')
    await bot.logout()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="D&D"))
    print('Bot Started')

bot.add_command(ping)
bot.add_command(roll)