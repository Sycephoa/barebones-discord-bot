import discord
from discord import app_commands
from discord.ext import commands

### to switch to parent directory ###
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
### to switch to parent directory ###

from config import *
import functions as f

@app_commands.default_permissions(administrator=True)
class Test(commands.GroupCog):
    
    def __init__(self,client):
        self.client = client

    @app_commands.command(name="test",description="test")
    @app_commands.checks.has_permissions(administrator=True)
    async def setdebugchannel(self, inter: discord.Interaction):
        await inter.response.send_message(f'This works.',ephemeral=False)
        

async def setup(client):
    await client.add_cog(Test(client))