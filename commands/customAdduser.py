import discord
import os

import brawlstats
import configparser
from utilities import database
from discord import Permissions, errors
from discord.utils import get, find
import string
from commands.base_command import BaseCommand
from utilities.utils import get_emoji


class CustomRegisterUser(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Allows Mods to Add a User to Club's Database"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["player_tag", "discord_id"]

        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        user_name = str(message.mentions[0].id)
        message_author = str(message.author)
        brawl_database = database.SQL_Server()

        # Get member object
        brawl_client = brawlstats.Client(self.brawl_api)
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
            player_tag = str(params[0])
            if player_tag[:1] != "#":
                raise Exception("Incorrect Player Tag. Be sure to add #")
            specific_user = brawl_client.get_profile(player_tag)
        except Exception:
            await message.channel.send(
                                      "Please, provide valid player tag")
            return

        if user_name in brawl_database.return_allUsers() and brawl_database.information_present(user_name):
            await message.channel.send(
                                      "The User has already been linked to an account")
            return

        if player_tag.upper() in brawl_database.return_allPlayers():
            await message.channel.send(
                                      "The Tag has already been linked to other user")
            return

        brawl_database.insert_user(user_name, player_tag)
        brawl_database.save_database()
        msg = get_emoji(":ok_hand:") + f" The User {player_tag} has been linked to {str(message.mentions[0])} in the database!"

        member_object = activeServers.get_member_named(str(message.mentions[0]))
        name_club = specific_user.club.name.split()[-1]
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
        member_role = get(member_object.guild.roles, name="Member")
        unverified_role = [get(member_object.guild.roles, name="Unverified")]

        await member_object.add_roles(club_role)
        await member_object.add_roles(member_role)
        await member_object.remove_roles(*unverified_role)

        # Set nickname
        printable = set(string.printable)
        clean_name = ''.join(filter(lambda x: x in printable, specific_user.name))

        if member_object.name != clean_name or member_object.nick != clean_name:
            try:
                await member_object.edit(nick=clean_name)
            except errors.Forbidden:
                pass

        await message.channel.send(msg)
