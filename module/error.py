import discord
from discord.ext import commands
import traceback

def setup(_bot):
    _bot.on_command_error = bot_error
    global bot
    bot = _bot

async def bot_error(ctx, error):
    try:
        async def send(_ctx, message):
            if _ctx.command != None and _ctx.command.name == "play":
                await _ctx.message.author.send(message) 
            else:
                await _ctx.send(message)
        if type(error) == commands.errors.NotOwner:
            await send(ctx, "This command can only be used by the bot owner!")
        elif type(error) == commands.CommandNotFound:
            pass
        elif type(error) == commands.errors.MissingRequiredArgument:
            await send(ctx, f"The correct usage for that command is: `{ctx.bot.command_prefix}{ctx.command.name} {ctx.command.usage}`")
        elif type(error) == commands.errors.CheckFailure:
            await send(ctx, "Oops! You can't use this. Sorry.")
        elif type(error) == commands.errors.CommandOnCooldown:
            await send(ctx, f"Command is on cooldown! Try again in {int(error.retry_after)+1} seconds!") #how to round up instead of down: add 1! :ventidab:
        else:
            await send(ctx, f"An error happened! Contact patata for more details.```Error type: {' '.join(str(type(error.original)).split(' ')[1:]).strip('>')}\nError code: {hex(ctx.message.id)}```")
            errfile = open("error/"+hex(ctx.message.id), "w")
            errfile.write("".join(traceback.format_exception(type(error.original), error.original, error.original.__traceback__)))
            errfile.close()
            try:
                await ctx.bot.get_channel(968160518042964079).send(str(hex(ctx.message.id)) + "```" +
                    "".join(traceback.format_exception(type(error.original), error.original, error.original.__traceback__)) + "```")
            except Exception as e:
                errfile = open("error/"+hex(ctx.message.id), "a")
                errfile.write("".join(traceback.format_exception(type(e), e, e.__traceback__)))
                errfile.close()
                await ctx.bot.get_channel(968160518042964079).send(f"{str(hex(ctx.message.id))}\nCouldn't send, check the error logs")
    except Exception as e:
        errfile = open("error/"+hex(ctx.message.id), "a")
        errfile.write("".join(traceback.format_exception(type(e), e, e.__traceback__)))
        errfile.close()
        print("".join(traceback.format_exception(type(e), e, e.__traceback__)))
        await ctx.send("Not only was there an error, there was also an error in sending the report.\nNotify this to patata ASAP, please.")