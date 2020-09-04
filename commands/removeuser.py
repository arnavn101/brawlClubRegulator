import os

import configparser
from utilities import database
from discord.utils import find

from commands.base_command import BaseCommand
from utilities.utils import get_emoji


class RemoveUser(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Removes a User from Club's Database"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["discord_id"]

        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        user_name = message.mentions[0].id  # (" ".join(params[:]))
        user_name_str = str(message.mentions[0])
        message_author = str(message.author)
        brawl_database = database.SQL_Server()

        # Get member object
        activeServers = list(client.guilds)[0]
        member_object = activeServers.get_member_named(message_author)

        role = find(lambda r: r.name == 'Moderator', activeServers.roles)
        if role not in member_object.roles:
            await message.channel.send(
                "You are not authorized to execute this command")
            return

        # Delete user from the database
        delete_user = brawl_database.remove_user(user_name)

        if delete_user:
            msg = get_emoji(":ok_hand:") + f" The User {user_name_str} has been deleted from the database!"
            await message.channel.send(msg)
            return

        else:
            msg = f" The User does not exist within the database!"
            await message.channel.send(msg)
            return
