from commands.base_command import BaseCommand
import os


# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Commands(BaseCommand):

    def __init__(self):
        description = "List of Bot commands for members"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):

        list_memberCommands = [line.rstrip() for line in open(os.path.join('config_files', 'member_commands.txt'))]
        COMMAND_HANDLERS = {c.__name__.lower(): c()
                            for c in BaseCommand.__subclasses__()}

        msg = message.author.mention + "\n"

        # Displays all descriptions, sorted alphabetically by command name
        for cmd in sorted(COMMAND_HANDLERS.items()):
            for member_command in list_memberCommands:
                if member_command == cmd[1].name:
                    msg += "\n" + cmd[1].description

        await message.channel.send(msg)
