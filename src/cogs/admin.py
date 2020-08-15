from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Bot Master')
    async def stop(self, ctx):
        await ctx.send('Stopping')
        print('Stopping')
        await self.bot.logout()