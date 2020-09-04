import os
import pickle

import configparser
from utilities import database
from discord import Embed
from discord.utils import find

from commands.base_command import BaseCommand


class ReturnGameModeResults(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Return Results of Game Mode Voting"
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

        load_variables = open(os.path.join('storage_files', 'saved_id2.pkl'), 'rb')
        id_message = pickle.load(load_variables)
        vote_message = await message.channel.fetch_message(id_message)
        votes = [["Gem Grab"], ["Solo Showdown"], ["Duo Showdown"], ["Brawl Ball"], ["Hot Zone"], ["Bounty"],
                 ["Heist"], ["Siege"]]

        for index in range(len(vote_message.reactions)):
            number_reactions = await vote_message.reactions[index].users().flatten()
            votes[index].append(len(number_reactions))

        for i in range(len(votes)):
            votes[i][1] -= 1
            votes[i][1] = str(votes[i][1])

        votes.sort(key=lambda x: int(x[1]), reverse=True)

        vote_message = Embed(title=f'Results of the GameMode Voting', color=0x00ff00)
        vote_message.add_field(name=votes[0][0], value=votes[0][1], inline=False)
        vote_message.add_field(name=votes[1][0], value=votes[1][1], inline=False)
        vote_message.add_field(name=votes[2][0], value=votes[2][1], inline=False)
        vote_message.add_field(name=votes[3][0], value=votes[3][1], inline=False)
        vote_message.add_field(name=votes[4][0], value=votes[4][1], inline=False)
        vote_message.add_field(name=votes[5][0], value=votes[5][1], inline=False)
        vote_message.add_field(name=votes[6][0], value=votes[6][1], inline=False)
        vote_message.add_field(name=votes[7][0], value=votes[7][1], inline=False)
        vote_message.set_footer(text=message_author, icon_url=member_object.avatar_url)

        await message.channel.send(embed=vote_message)
