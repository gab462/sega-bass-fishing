import nextcord
import nextcord.ext.commands
import random


class Randomize(nextcord.ext.commands.Cog):
    def __init__(self, bot, phrase_function):
        self.bot = bot
        self.get_phrases = phrase_function


    @nextcord.slash_command(description='Roll from 1 to number (default 10)')
    async def roll(self, interaction,
                   number: int = nextcord.SlashOption(description='Number', required=False, default=10)):
        try:
            await interaction.response.send_message(random.randint(1, number))
        except Exception as e:
            await interaction.response.send_message(f'Error: {e}')


    @nextcord.slash_command(description='Get random phrase')
    async def phrase(self, interaction):
        chosen = random.choice(self.get_phrases())

        await interaction.response.send_message(chosen)
