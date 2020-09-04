import brawlstats
import configparser
from utilities import database
import os
import discord
import math
import string
from discord import Permissions, errors
from discord.utils import get, find

from commands.base_command import BaseCommand
from utilities.utils import get_channel


class InitiateEvent(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Start the Bot Regulation Event"
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config_files', 'config.cfg'))
        self.interval_minutes = float(self.config.get('ConfigInfo', 'TIME_INTERVAL'))  # Set the interval for this event
        var = float(self.config.get('ConfigInfo', 'ALLOWED_TIME'))
        self.allowed_userWarning = math.ceil(var / self.interval_minutes)
        self.brawl_api = str(self.config.get('ConfigInfo', 'API_KEY'))
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = []

        super().__init__(description, params)

    # Override the run() method
    # It will be called once every {interval_minutes} minutes
    async def handle(self, params, message, client):
        activeServers = list(client.guilds)[0]
        list_members = activeServers.members
        message_author = str(message.author)
        brawl_database = database.SQL_Server()
        member_object = activeServers.get_member_named(message_author)

        role = find(lambda r: r.name == 'Moderator', activeServers.roles)
        role_owner = find(lambda r: r.name == 'Owner', activeServers.roles)

        if role not in member_object.roles:
            if role_owner not in member_object.roles:
                await message.channel.send(
                    "You are not authorized to execute this command")
                return

        print("Start Task")
        warning_channel = get_channel(client, "warnings")

        for member in list_members:

            member_n = (str(member))
            member_object = activeServers.get_member_named(member_n)
            member_role = [get(member_object.guild.roles, name="Member")]
            member = (str(member.id))

            if member_object.bot:
                pass

            elif brawl_database.return_userWarning(member) >= self.allowed_userWarning \
                    and find(lambda r: r.name == 'Member', activeServers.roles) in member_object.roles:
                msg = " removed from server since they did not insert player information in database"
                await warning_channel.send(member_object.mention + msg)
                await member_object.remove_roles(*member_role)

            elif member not in brawl_database.return_allUsers() \
                    and find(lambda r: r.name == 'Member', activeServers.roles) in member_object.roles:
                brawl_database.insert_user_warning(member)
                msg = " did not insert player information in database"
                await warning_channel.send(member_object.mention + msg)

            elif not brawl_database.information_present(member) \
                    and find(lambda r: r.name == 'Member', activeServers.roles) in member_object.roles:
                brawl_database.append_user_warning(member)
                msg = " did not insert player information in database"
                await warning_channel.send(member_object.mention + msg)

            elif find(lambda r: r.name == 'Member', activeServers.roles) in member_object.roles:
                brawl_client = brawlstats.Client(self.brawl_api)
                with open('tags.txt', 'r') as f:
                    brawl_tag = f.read().splitlines()

                try:
                    player_info = brawl_client.get_player((brawl_database.view_information_user(member)).upper())
                except Exception:
                    player_info = ""

                try:
                    player_club = player_info.club.tag
                except Exception:
                    player_club = "None"

                if player_club not in brawl_tag:
                    msg = "'s member role removed since they are not part of the club"
                    for role in member_object.roles:
                        if "everyone" not in role.name:
                            try:
                                # print("Remove roles")
                                await member_object.remove_roles(role)
                            except Exception as e:
                                print(role)
                                print(e, member)
                                pass

                    Nonmember_role = get(member_object.guild.roles, name="Non-Member")
                    await warning_channel.send(member_object.mention + msg)
                    await member_object.add_roles(Nonmember_role)

                else:
                    list_roles = []
                    for role in activeServers.roles:
                        list_roles.append(role.name)

                    try:
                        name_club = player_info.club.name.split()[-1]
                    except Exception:
                        continue
                    name_role = f"{name_club} Member"

                    if name_role not in list_roles:
                        role_permissions = Permissions(send_messages=False, read_messages=True)
                        await activeServers.create_role(name=name_role,
                                                        permissions=role_permissions,
                                                        hoist=True,
                                                        colour=discord.Colour.blue())

                    printable = set(string.printable)
                    clean_name = ''.join(filter(lambda x: x in printable, player_info.name))

                    if member_object.name != clean_name or member_object.nick != clean_name:
                        try:
                            await member_object.edit(nick=clean_name)
                        except errors.Forbidden:
                            pass

                    club_role = get(member_object.guild.roles, name=name_role)
                    member_role = get(member_object.guild.roles, name="Member")
                    unverified_role = [get(member_object.guild.roles, name="Unverified")]

                    await member_object.add_roles(club_role)
                    await member_object.add_roles(member_role)
                    await member_object.remove_roles(*unverified_role)
        await message.channel.send("The Regulation Task has been completed :)")
        return
