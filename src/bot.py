import discord
from discord.ext import commands
from .settings import prefix

# Cog Class Imports
from .cogs.admin import Admin
from .cogs.ping import Ping
from .cogs.roll import Roll

bot = commands.Bot(command_prefix=prefix)

# Adding Cogs
bot.add_cog(Admin(bot))
bot.add_cog(Ping(bot))
bot.add_cog(Roll(bot))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="D&D"))
    print('Bot Started')