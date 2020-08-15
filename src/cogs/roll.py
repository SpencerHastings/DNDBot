from discord.ext import commands
import dice

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, arg):
        try:
            await ctx.send(dice.roll(arg))
        except dice.DiceBaseException as e:
            print(e.pretty_print())