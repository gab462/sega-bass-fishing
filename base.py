import nextcord
import nextcord.ext.commands
import os.path


class Base(nextcord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not os.path.isfile('db.json'):
            with open('db.json', 'w+') as f:
                f.write(json.dumps({}))


    @nextcord.ext.commands.Cog.listener()
    async def on_ready(self):
        print('Refreshing application commands...')
        await self.bot.sync_all_application_commands()
        print(f'Logged in as {self.bot.user}')


    @nextcord.slash_command(description='Responds with pong')
    async def ping(self, interaction):
        await interaction.response.send_message('Pong!')
