#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.stderr = open('log.txt', 'w') #log

import argparse
import discord
from discord.ext import commands
import os
import tokens

#default values before parse
token = tokens.poison
prefix = "p!"
activity = "minecra"

#argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="use the path given as the root directory for the bot (defaults to current directory)")
parser.add_argument("-d", "--debug", help="use the notpatatsu bot and d+ prefix for debugging purposes", action="store_true")
parser.add_argument("-P", "--prefix", help=f"change the bot's prefix (defaults to '{prefix}')")
parser.add_argument("-s", "--status", help="change the bot's status at bootup (defaults to 'online')")
parser.add_argument("-a", "--activity", help="change the bot's activity status (defaults to 'with fire')")
parser.add_argument("-A", "--activity-type", help="change the bot's activity status type (Playing, Streaming, etc.) (defaults to 'playing')")
args = parser.parse_args()

if args.path != None:
    os.chdir(args.path)
if args.debug:
    token = tokens.debug
    prefix = "d+"
if args.prefix != None:
    prefix = args.prefix
if args.status != None:
    args.status = args.status.lower()
status = { "online": discord.Status.online,
           "idle": discord.Status.idle,
           "dnd": discord.Status.dnd, "do_not_disturb": discord.Status.dnd, "do not disturb": discord.Status.dnd,
           "invisible": discord.Status.invisible, "offline": discord.Status.invisible
         }.get(args.status, discord.Status.online)
if args.activity != None:
    activity = args.activity
if args.activity_type != None:
    activity_type = args.activity_type.lower()
activity_type = { "playing": discord.ActivityType.playing,
                  "streaming": discord.ActivityType.streaming,
                  "listening": discord.ActivityType.listening
                }.get(args.activity_type, discord.ActivityType.playing)

#load bot
bot = commands.Bot(prefix, intents=discord.Intents.default(), owner_ids=(705031051734679574, 329357113480708106)) #tree, patat
bot.command_prefix = prefix
bot.remove_command("help") #default help command

#Setup modules
bot.module_errors = ""
for file in os.listdir("module"):
    if file == "__pycache__" or file == "debug.py":
        continue
    try:
        bot.load_extension("module." + file.split(".py")[0]) #split(".py") feels wrong but like... it doesn't rly matter
    except Exception as e:
        bot.module_errors += str(e)+ "\n\n"
bot.module_errors = bot.module_errors.rstrip()

#Setup WIP modules
bot.test_errors = ""
for file in os.listdir("test"):
    if file == "__pycache__":
        continue
    try:
        #TODO: Make them be hidden and helper-only
        bot.load_extension("test." + file.split(".py")[0]) 
    except Exception as e:
        bot.test_errors += str(e)+ "\n\n"
bot.test_errors = bot.test_errors.rstrip()

bot.load_extension("module.debug")

#Finally, load the bot!
@bot.event
async def on_ready():
    print("Bot successfully loaded")
    await bot.change_presence(activity=discord.Activity(name=activity, type=activity_type), status=status)

bot.run(token)