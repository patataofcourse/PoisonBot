import discord
from discord.ext import commands

def is_helper():
    def check(ctx):
        return (ctx.message.author.id in ctx.bot.owner_ids or ctx.message.author.id in [])
    return commands.check(check)