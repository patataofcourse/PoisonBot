# Help command

import discord
from discord.ext import commands

from lib import roles


def setup(bot):
    bot.add_command(hlp)


def usg(c):  # makes usage if it's a group and usage = ""
    if type(c) == commands.Group:
        u = "("
        for cmd in c.commands:
            u += cmd.name + "/"
        u = u.rstrip("/") + ")"
        return u
    else:
        return ""


def find_command(cmds, names):
    found = None
    n = ""
    for command in cmds:
        if names[0] == command.name or (command.aliases != None and names[0] in command.aliases):
            n = command.name + " "
            if len(names) == 1:
                found = command
            elif type(command) == commands.Group:
                found, plus = find_command(command.commands, names[1:])
                n += plus
            else:
                return None, " ".join(names)
            break
    return found, n.rstrip()


@commands.command(name="help", description="The help command. You are using it.", usage="<command>")
async def hlp(ctx, *args):
    if args == ():
        standard = ""
        helper = ""
        owner = ""
        for command in ctx.bot.commands:
            if command.hidden and ctx.channel.type != "private":
                continue
            hpc = ""  # Highest priority check. Priority is: is_owner
            for check in command.checks:
                if "is_owner" in str(check):
                    hpc = "owner"
                    break
                elif "is_helper" in str(check):
                    hpc = "helper"
            if command.usage == None or command.usage == "":
                command.usage = usg(command)
            if hpc == "owner":
                owner += f"**{ctx.bot.command_prefix}" + \
                    command.name + "** " + command.usage + "\n"
            elif hpc == "helper":
                helper += f"**{ctx.bot.command_prefix}" + \
                    command.name + "** " + command.usage + "\n"
            else:
                standard += f"**{ctx.bot.command_prefix}" + \
                    command.name + "** " + command.usage + "\n"
        embed = discord.Embed(
            title="Poison help", description=f"Use {ctx.bot.command_prefix}help <command> for more info on the command", color=0x901502)
        embed.add_field(name="Standard commands:",
                        value=standard, inline=False)

        @roles.is_helper()
        @commands.command(name="s")
        async def test_cmd(ctx):
            pass

        try:
            test_cmd.checks[0](ctx)
        except Exception as e:
            is_helper = False
        else:
            is_helper = True

        if is_helper and helper != "":
            embed.add_field(name="Helper commands:", value=helper, inline=False)

        @commands.is_owner()
        @commands.command(name="s")
        async def test_cmd(ctx):
            pass

        try:
            await test_cmd.checks[0](ctx)
        except:
            is_owner = False
        else:
            is_owner = True

        if is_owner and owner != "":
            embed.add_field(name="Owner commands:", value=owner, inline=False)
        await ctx.send(embed=embed)
    else:
        command, name = find_command(ctx.bot.commands, args)
        if command != None:
            if command.help == None or command.help == "":
                if type(command) == commands.Group:
                    command.help = f"Check **{ctx.bot.command_prefix}help {name} <subcommand>** for more info!"
                else:
                    command.help = ""
            if command.usage == None or command.usage == "":
                command.usage = usg(command)
            if command.aliases == None:
                command.aliases = []
            embed = discord.Embed(
                title=f"{ctx.bot.command_prefix}{name}", description=command.description, color=0x901502)
            embed.add_field(
                name="Usage:", value=f"**{ctx.bot.command_prefix}{name} ** {command.usage}\n\n{command.help}", inline=False)
            if len(command.aliases) != 0:
                embed.add_field(name="Aliases:", value=ctx.bot.command_prefix+(" ".join(name.split(" ")[:-1])+" ").lstrip()+(
                    '\n'+ctx.bot.command_prefix+(" ".join(name.split(" ")[1:])+" ").lstrip()).join(command.aliases), inline=False)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send(f"Command `{' '.join(args)}` doesn't exist!")
