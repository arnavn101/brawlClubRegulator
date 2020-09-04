from commands.base_command import BaseCommand
from discord.utils import find
import os


# This is a convenient command that automatically generates a helpful
# message showing all available commands
class AdminCommands(BaseCommand):

    def __init__(self):
        description = "List of Bot commands for Moderators"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
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

        list_memberCommands = [line.rstrip() for line in open(os.path.join('config_files', 'member_commands.txt'))]
        COMMAND_HANDLERS = {c.__name__.lower(): c()
                            for c in BaseCommand.__subclasses__()}

        msg = message.author.mention + "\n"
        boolean_handler = True

        # Displays all descriptions, sorted alphabetically by command name
        for cmd in sorted(COMMAND_HANDLERS.items()):
            for member_command in list_memberCommands:
                if member_command == cmd[1].name:
                    boolean_handler = False
                    break
            if boolean_handler:
                msg += "\n" + cmd[1].description
            boolean_handler = True

        await message.channel.send(msg)
