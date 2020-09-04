import configparser
import os

from discord import Embed

from commands.base_command import BaseCommand


class DisplayAvatar(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Display a user's Avatar"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = []

        super().__init__(description, params)

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
        ismentioned = True

        try:
            mentioned_user_name = str(message.mentions[0])
            mentioned_user = activeServers.get_member_named(mentioned_user_name)
        except Exception:
            ismentioned = False

        embed_msg = Embed(title='User Avatar', color=0x00ff00)
        if ismentioned:
            embed_msg.set_image(url=mentioned_user.avatar_url)
            embed_msg.set_footer(text=mentioned_user_name, icon_url = mentioned_user.avatar_url)
        else:
            embed_msg.set_image(url=member_object.avatar_url)
            embed_msg.set_footer(text=user_name, icon_url = member_object.avatar_url)
            
        await message.channel.send(embed=embed_msg)


