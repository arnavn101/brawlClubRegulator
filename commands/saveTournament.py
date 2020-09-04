import csv
import os
import pickle

import brawlstats
import configparser
from utilities import database
import string
from discord.utils import find

from commands.base_command import BaseCommand


class SaveTournament(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Save a Club Tournament's participants"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        self.printable = set(string.printable)
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["channel_message"]

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
        brawl_database = database.SQL_Server()
        mentioned_channel = message.channel_mentions[0]

        # Get member object
        brawl_client = brawlstats.Client(self.brawl_api)
        activeServers = list(client.guilds)[0]
        list_members = activeServers.members
        member_object = activeServers.get_member_named(message_author)

        role = find(lambda r: r.name == 'Moderator', activeServers.roles)
        role_owner = find(lambda r: r.name == 'Owner', activeServers.roles)

        if role not in member_object.roles:
            if role_owner not in member_object.roles:
                await message.channel.send(
                    "You are not authorized to execute this command")
                return

        load_variables = open(os.path.join('storage_files', 'saved_id.pkl'), 'rb')
        id_message = pickle.load(load_variables)
        vote_message = await mentioned_channel.fetch_message(id_message)
        participants = []
        participantsIds = []
        list_reactions = await (vote_message.reactions[0]).users().flatten()

        for individual_participant in list_reactions:
            participantsIds.append([str(individual_participant.id)])
            participants.append([str(individual_participant)])

        for index in range(len(participants)):
            if brawl_database.information_present(participantsIds[index][0]):
                player_info = (brawl_client.get_player(brawl_database.view_information_user(participantsIds[index][0])))
                participants[index].append(player_info.name)
                participants[index].append(str(player_info.trophies))
            else:
                participants[index].append(participants[index][0])
                participants[index].append("UnKnown")

        with open(os.path.join("storage_files", "listParticipants.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(participants)

        await message.channel.send(f"{len(participants) - 1} people have signed up for the tournament!!!")
