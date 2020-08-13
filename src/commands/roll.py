from discord.ext import commands
import dice

@commands.command()
async def roll(ctx, arg):
    try:
        await ctx.send(dice.roll(arg))
    except dice.DiceBaseException as e:
        print(e.pretty_print())
    