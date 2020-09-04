import brawlstats
import configparser
from utilities import database
import string
from discord import Permissions, errors
from discord.utils import get, find
import os
import discord
from commands.base_command import BaseCommand
from utilities.utils import get_emoji


class automaticRegisterUser(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Automatically Adds a User to Club's Database"
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
        brawl_database = database.SQL_Server()

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

        for member in list_members:

            user_name = (str(member))
            member_object = activeServers.get_member_named(user_name)
            user_name = (str(member_object.id))
            member_role = get(member_object.guild.roles, name="Member")
            unverified_role = [get(member_object.guild.roles, name="Unverified")]

            if member_object.bot:
                pass

            elif not brawl_database.information_present(user_name):
                member_name = member_object.display_name
                list_clubs = [line.rstrip() for line in open(os.path.join('config_files', 'tags.txt'))]
                variable_set = False

                for i in range(len(list_clubs)):
                    if variable_set:
                        break

                    club = brawl_client.get_club((list_clubs[i]).upper())
                    club_info = club.members
                    player_club = club.name

                    for member_club in club_info:
                        if member_name.lower() in (member_club.name.replace(" ", "")).lower():
                            player_tag = member_club.tag
                            player_name = member_club.name
                            variable_set = True

                if variable_set:

                    brawl_database.insert_user(user_name, player_tag)
                    brawl_database.save_database()
                    msg = get_emoji(
                        ":ok_hand:") + f" The User {player_tag} has been linked to {str(member)} in the database!"

                    name_club = (player_club).split()[-1]
                    name_role = f"{name_club} Member"
                    list_roles = []
                    for role in activeServers.roles:
                        list_roles.append(role.name)

                    if name_role not in list_roles:
                        role_permissions = Permissions(send_messages=False, read_messages=True)
                        await member_object.guild.create_role(name=name_role,
                                                              permissions=role_permissions,
                                                              hoist=True,
                                                              colour=discord.Colour.blue())

                    club_role = get(member_object.guild.roles, name=name_role)

                    await member_object.add_roles(club_role)
                    await member_object.add_roles(member_role)
                    await member_object.remove_roles(*unverified_role)

                    # Set nickname
                    printable = set(string.printable)
                    clean_name = ''.join(filter(lambda x: x in printable, player_name))

                    if member_object.name != clean_name or member_object.nick != clean_name:
                        try:
                            await member_object.edit(nick=clean_name)
                        except errors.Forbidden:
                            pass

                    await message.channel.send(msg)
