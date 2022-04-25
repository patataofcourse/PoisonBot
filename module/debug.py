import discord
from discord.ext import commands

def setup(bot):
    bot.add_command(debug)
    global module_errors
    global test_errors
    module_errors = bot.module_errors
    if module_errors == "": module_errors = "No errors! :D"
    test_errors = bot.test_errors
    if test_errors == "": test_errors = "No errors! :D"
    
@commands.command(name="debug",
             description = "Sends debug menu to a specific private channel only the owners can access. :eyes:",
             usage = "")
@commands.is_owner()
async def debug(ctx):
    await ctx.send("Debug menu sent!")
    embed = discord.Embed(title="Poison debug", color=0x901502)
    embed.add_field(name="Module errors", value=module_errors)
    embed.add_field(name="Test/WIP module errors", value=test_errors)
    await ctx.bot.get_channel(968160518042964079).send(embed=embed)