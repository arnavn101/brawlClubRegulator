import configparser
import os
from collections import deque

from discord import Embed
from discord.utils import find

from commands.base_command import BaseCommand


class displayLogs(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Display Debug Logs"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["number_lines"]

        super().__init__(description, params)

    def returnLogLines(self, file_name, lines=1):
        with open(file_name) as fileObject:
            return list(deque(fileObject, lines))

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        user_name = str(message.author)
        activeServers = list(client.guilds)[0]
        member_object = activeServers.get_member_named(user_name)

        role = find(lambda r: r.name == 'Moderator', activeServers.roles)
        role_owner = find(lambda r: r.name == 'Owner', activeServers.roles)

        if role not in member_object.roles:
            if role_owner not in member_object.roles:
                await message.channel.send(
                    "You are not authorized to execute this command")
                return

        try:
            number_lines = int(params[0])
        except Exception:
            await message.channel.send(
                "Please, provide valid number of lines")
            return

        list_lines = self.returnLogLines("discord.log", number_lines)
        embed_msg = Embed(title='Log Information', color=0x00ff00)

        for i in range(len(list_lines)):
            embed_msg.add_field(name=f"Line {i + 1}", value=list_lines[i], inline=False)

        embed_msg.set_footer(text=user_name, icon_url=member_object.avatar_url)
        await message.channel.send(embed=embed_msg)
