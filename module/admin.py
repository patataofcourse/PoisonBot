import discord
from discord.ext import commands
import os
import platform

from lib import roles

def setup(_bot):
    _bot.add_command(kill)
    _bot.add_command(errwipe)
    _bot.add_command(execcmd)
    _bot.add_command(aexec)
    _bot.add_command(spek)
    global bot
    bot = _bot

@commands.is_owner()
@commands.command(name="speak", usage="<sekrit shet>", description=":)", hidden=True, aliases=("s", "spek", "t", "talk")) 
async def spek(ctx, chid, *args):
    msg = " ".join(args).replace("{","<")
    if chid in ("this", "t"):
        await ctx.message.delete()
        await ctx.send(msg)
    else:
        await ctx.bot.get_channel(int(chid)).send(msg)

@commands.command(name="aexec",
                usage="<code>",
                description="Runs some async code.\nOwner only")
@commands.is_owner()
async def aexec(ctx, *args):
    code = " ".join(ctx.message.content.split(" ")[1:]).strip("`")
    # Make an async function with the code and `exec` it
    exec(
        f'async def __ex(ctx): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    await locals()['__ex'](ctx)
    
@commands.command(name="exec",
                    usage="<code>",
                    description="Evals some code.\n Owner only.")
@commands.is_owner()
async def execcmd(ctx, code):
    await ctx.send(eval(code))

@roles.is_helper()
@commands.command(name="kill", usage="", description="Kills the bot.", aliases=("ded","die"))
async def kill(ctx):
    await ctx.send("*dies cutely*")
    await ctx.bot.close()

@roles.is_helper()
@commands.command(name="errwipe", usage="", description="Deletes all /error files.", aliases=("ew",))
async def errwipe(ctx):
    if platform.system() not in ("Linux", "Windows", "Darwin"):
        await ctx.send("Yeah, you can't use that right now. Sorry!") #i think mac support should be in now
    for file in os.listdir("error"):
        if file == "just to make sure the folder exists":
            continue
        if platform.system() == "Windows":
            os.system(f"del error/{file}")
        else:
            os.system(f"rm error/{file}")
    await ctx.send("Errors wiped!")