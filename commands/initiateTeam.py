import configparser
import csv
import os
import string

from commands.base_command import BaseCommand
from utilities.utils import get_emoji


class initiateteam(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Enables people to create teams for the tournament"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        self.printable = set(string.printable)
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = []

        super().__init__(description, params)

    def clean_name(self, user_name):
        return ((''.join(filter(lambda x: x in self.printable, user_name))).encode('ascii', 'ignore')).decode("utf-8")

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

        try:
            playerTeam = message.mentions
            playerTeam = [str(player) for player in playerTeam]
        except Exception:
            await message.channel.send("Please enter a valid list of players")
            return

        if len(playerTeam) != len(params):
            await message.channel.send("Make sure that all players in team have unique discord id")
            return

        participants = []
        with open(os.path.join('storage_files', 'listParticipants.csv')) as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                if "brawlclubregulator" not in row[0].lower():
                    participants.append(row[0])

        for individual_player in playerTeam:
            if individual_player not in participants:
                await message.channel.send("One of the players is not registered for the tournament")
                return

        registered_users = []
        os_path = os.path.join('storage_files', 'listTeams.csv')
        if os.path.exists(os_path):
            with open(os_path) as f:
                reader = csv.reader(f, delimiter=",")
                for row in reader:
                    for individual_player in row:
                        registered_users.append(individual_player)

        for individual_player in playerTeam:
            individual_player = self.clean_name(individual_player)
            if individual_player in registered_users:
                await message.channel.send("One of the players is already registered in a team for the tournament")
                return

        if os.path.exists(os_path):
            with open(os_path, "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(playerTeam)
        else:
            with open(os_path, "w+") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(playerTeam)

        msg = get_emoji(":ok_hand:") + f" Your Team has been created!!!"
        await message.channel.send(msg)
