from commands.base_command import BaseCommand
from discord.utils import find
from subprocess import Popen, PIPE
import os


class RawServerCommand(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Run CLI commands on Server"

        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["working_directory", "command"]

        # Hard Code Path :)
        os.environ['PATH'] = "/home/discord/.local/bin:/usr/local/sbin:/usr/local/bin:" \
                             "/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
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

        role = find(lambda r: r.name == 'Moderator', activeServers.roles)
        role_owner = find(lambda r: r.name == 'Owner', activeServers.roles)

        if role not in member_object.roles:
            if role_owner not in member_object.roles:
                await message.channel.send(
                    "You are not authorized to execute this command")
                return

        try:
            user_directory = params[0]
            command_name = (" ".join(params[1:]))
        except Exception:
            await message.channel.send(
                "Please, provide a valid parameter")
            return

        try:
            process = Popen(command_name, cwd=user_directory,
                            stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)
            stdout, stderr = process.communicate()
            stdout = str(stdout.decode())
        except Exception:
            await message.channel.send(
                "Please, provide a valid command. Root/admin commands will not work due to security reasons")
            return

        try:
            embed_msg = 'Command Line Output\n\n'
            embed_msg += stdout
            await message.channel.send(embed_msg)
        except Exception:
            await message.channel.send(
                "Sorry, the response was too big for discord :(")
            return
