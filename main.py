import discord
from discord.ext import commands
from discord import app_commands

import os, re, sys, traceback, argparse

import functions as f
from config import *
import asyncio
from datetime import datetime as dt

#arg token
parser = argparse.ArgumentParser()
parser.add_argument('--token',required=False,help='an alternative bot token to the environment token')
args = parser.parse_args()

token = args.token or os.getenv(f'DISCORD_TOKEN_{APP_NAME}')
if not token:
    print(f"There is no DISCORD_TOKEN_{APP_NAME} environment variable set!")
    sys.exit(1)

intents = discord.Intents().default()
intents.message_content = True #required for prefix commands.
client = commands.Bot(command_prefix='#',intents=intents,help_command=None)

#load all cogs on startup.
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            #load extension and log
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'{colors.cyan}[cogs]{colors.resetAll} loading',filename)

@client.command()
async def reload(ctx, cogname:str=None):
    if ctx.author.id == DEV_USERID:
        cogsPrefix = f'{colors.cyan}[cogs]{colors.resetAll}'
        if cogname:
            await client.reload_extension(f'cogs.{cogname}')
            print(f'{cogsPrefix} reloaded {cogname}')
            await ctx.send("[Cogs] "+cogname+' was reloaded.')
        else:
            reloadNumbers = {"reloaded":0,"new":0,"lost":0}
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        await client.unload_extension(f'cogs.{filename[:-3]}')
                        await client.load_extension(f'cogs.{filename[:-3]}')
                        print(f'{cogsPrefix} reloaded {filename[:-3]}')
                        reloadNumbers["reloaded"]+=1
                    except commands.errors.ExtensionNotLoaded:
                        await client.load_extension(f'cogs.{filename[:-3]}')
                        print(f'{cogsPrefix} {filename[:-3]} was not loaded, but now is')
                        reloadNumbers["new"]+=1
                    except commands.errors.ExtensionNotFound:
                        print(f'{cogsPrefix} {filename[:-3]} was not loaded because not found')
                        reloadNumbers["lost"]+=1

            await ctx.send(f"[Cogs] All cogs were reloaded. ({ ', '.join([f'{key}: {reloadNumbers[key]}' for key in reloadNumbers]) })")

@client.command()
async def sync(ctx):
    if ctx.author.id == DEV_USERID:
        client.tree.copy_global_to(guild=ctx.guild)
        await client.tree.sync()
        await ctx.reply("Synced.")

@client.event
async def on_ready():
    print(f'{colors.lightGreen}We have logged in as {client.user} :){colors.resetAll}')
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your activity"))

@client.tree.error
async def on_inter_error(inter:discord.Interaction,error) -> None:
    if isinstance(error,app_commands.errors.MissingPermissions):
        await inter.response.send_message(f'You\'re missing permission to run this command.',ephemeral=True)
    else: #add your exception handling with elif before this line
        print(f'{colors.red}error in slash app{colors.resetAll}')
        print(print(traceback.format_exc()))
        print(f'{colors.red}end of error handling{colors.resetAll}')
    

#new run thingy cuz of cogs
async def main():
    async with client:
        await load_cogs()
        await client.start(token)
asyncio.run(main())