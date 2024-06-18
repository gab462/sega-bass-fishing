import nextcord
import nextcord.ext.commands
import re
import asyncio
import datetime
import zoneinfo


class Remind(nextcord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @nextcord.slash_command(description='Remind after specified time')
    async def remind(self,
                     interaction: nextcord.Interaction,
                     after_time: str = nextcord.SlashOption(description='Time', required=True),
                     role: nextcord.Role = nextcord.SlashOption(description='Role to mention', required=False)):
        after = {}

        for t in ['d', 'h', 'm', 's']:
            after[t] = re.findall(fr'[0-9]+{t}', after_time)

        try:
            for t in after:
                if len(after[t]) == 0:
                    after[t] = 0
                else:
                    after[t] = int(after[t][0][:-1])

            delta = datetime.timedelta(days=after['d'],
                                       hours=after['h'],
                                       minutes=after['m'],
                                       seconds=after['s'])

            mention = role.mention if role else interaction.user.mention

            channel = interaction.channel

            await interaction.response.send_message(f'Reminder registered in {delta}')

            await asyncio.sleep(delta.total_seconds())

            await channel.send(f'Time over {mention} ({delta} passed)')
        except Exception as e:
            await interaction.response.send_message(f'Error: {e}')


    @nextcord.slash_command(description='Schedule reminder')
    async def schedule(self,
                       interaction: nextcord.Interaction,
                       when: str = nextcord.SlashOption(description='When (dd/mm hh)', required=True),
                       role: nextcord.Role = nextcord.SlashOption(description='Role to mention', required=False)):
        try:
            date, hour = when.split(' ')
            day, month = date.split('/')

            now = datetime.datetime.now(zoneinfo.ZoneInfo('America/Sao_Paulo'))
            dt = datetime.datetime.fromisoformat(f'{now.year}-{month}-{day}T{hour}:00:00-03:00')

            delta = dt - now

            mention = role.mention if role else interaction.user.mention

            channel = interaction.channel

            await interaction.response.send_message(f'Reminder registered in {delta}')

            await asyncio.sleep(delta.total_seconds())

            await channel.send(f'Time over {mention} ({delta} passed)')
        except Exception as e:
            await interaction.response.send_message(f'Error: {e}')
