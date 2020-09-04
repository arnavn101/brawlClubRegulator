import os
import pickle

import configparser
from discord import Embed
from discord.utils import find

from commands.base_command import BaseCommand


class InitiateTournament(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Initiate a Club Tournament"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["tournament_name"]

        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        message_author = str(message.author)

        # Get member object
        activeServers = list(client.guilds)[0]
        member_object = activeServers.get_member_named(message_author)

        role = find(lambda r: r.name == 'Moderator', activeServers.roles)
        role_owner = find(lambda r: r.name == 'Owner', activeServers.roles)

        if role not in member_object.roles:
            if role_owner not in member_object.roles:
                await message.channel.send(
                    "You are not authorized to execute this command")
                return

        try:
            tournament_name = (" ".join(params[:]))
        except Exception:
            await message.channel.send(
                "Please enter a valid Tournament name")
            return

        vote_message = Embed(title=f'{tournament_name}', color=0x00ff00)
        vote_message.set_image(
            url="https://blog.brawlstars.com/uploaded-images/Brawl-Stars-World-Finals-announcement_Thumb_800x433.jpg")
        vote_message.set_footer(text=message_author, icon_url=member_object.avatar_url)

        sent_message = await message.channel.send(embed=vote_message)
        await sent_message.add_reaction("\U0001F44D")
        save_id = open(os.path.join("storage_files", "saved_id.pkl"), "wb")
        id_message = sent_message.id
        pickle.dump(id_message, save_id)
