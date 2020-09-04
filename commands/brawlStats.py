import brawlstats
import configparser
from utilities import database
from discord import Embed
import os

from commands.base_command import BaseCommand


class BrawlStats(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Info from Club Database"
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
        user_name = str(message.mentions[0].id)
        message_author = str(message.author)
        brawl_client = brawlstats.Client(self.brawl_api)
        brawl_database = database.SQL_Server()

        activeServers = list(client.guilds)[0]
        member_object = activeServers.get_member_named(message_author)

        if not brawl_database.information_present(user_name):
            await message.channel.send(
                                      "The User did not insert player tag")
            return

        brawl_tag = brawl_database.view_information_user(user_name)
        player_info = brawl_client.get_player(brawl_tag.upper())

        embed_msg = Embed(title='Brawl Stars Statistics', color=0x00ff00)
        embed_msg.add_field(name="Player Name", value=player_info.name, inline=False)
        embed_msg.add_field(name="Player Club", value=player_info.club.name, inline=False)
        embed_msg.add_field(name="Player Trophies", value=player_info.trophies, inline=False)
        embed_msg.add_field(name="Player PP Points", value=player_info.power_play_points, inline=False)

        embed_msg.add_field(name="3v3 Victories", value=player_info.x3vs3_victories, inline=False)
        embed_msg.add_field(name="Duo Victories", value=player_info.duo_victories, inline=False)
        embed_msg.add_field(name="Solo Victories", value=player_info.solo_victories, inline=False)
        embed_msg.add_field(name="Robo Rumble Time", value=player_info.best_robo_rumble_time, inline=False)
        embed_msg.add_field(name="Big Brawler Time", value=player_info.best_time_as_big_brawler, inline=False)

        embed_msg.set_footer(text=user_name, icon_url=member_object.avatar_url)

        await message.channel.send(embed=embed_msg)
