import nextcord
import nextcord.ext.commands
import nextcord.ext.tasks
import re
import asyncio
import datetime
import zoneinfo
import json_db


class Remind(nextcord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with json_db.connect('db.json') as db:
            if 'scheduled' not in db.keys():
                db['scheduled'] = []


    @nextcord.ext.commands.Cog.listener()
    async def on_ready(self):
        self.today.start()
        self.remind_scheduled.start()


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


    @nextcord.slash_command(description='Schedule event')
    async def schedule(self,
                       interaction: nextcord.Interaction,
                       title: str = nextcord.SlashOption(description='Name of the event', required=True),
                       when: str = nextcord.SlashOption(description='When (dd/mm HH:MM)', required=True),
                       role: nextcord.Role = nextcord.SlashOption(description='Role to mention', required=False)):
        try:
            date, time = when.split(' ')
            day, month = date.split('/')

            now = datetime.datetime.now(zoneinfo.ZoneInfo('America/Sao_Paulo'))

            dt = datetime.datetime.fromisoformat(f'{now.year}-{month}-{day}T{time}:00-03:00')

            mention = role.mention if role else interaction.user.mention

            channel = interaction.channel.id

            with json_db.connect('db.json') as db:
                db['scheduled'].append({
                    'title': title,
                    'time': f'{now.year}-{month}-{day}T{time}:00:00-03:00',
                    'mention': mention,
                    'channel': channel
                })

            await interaction.response.send_message(f'Event scheduled for {dt}')
        except Exception as e:
            await interaction.response.send_message(f'Error: {e}')


    @nextcord.slash_command(description='Scheduled events')
    async def get_scheduled(self, interaction):
        scheduled = []

        with json_db.connect('db.json') as db:
            scheduled = db['scheduled']

        events = [f'**{event["title"]}** - {event["time"]}'
                  for event in scheduled
                  if event['channel'] == interaction.channel.id]

        if len(events) > 0:
            message = '\n'.join(events)
        else:
            message = 'No events'

        await interaction.response.send_message(message)


    @nextcord.ext.tasks.loop(time=[datetime.time(hour=12)])
    async def today(self):
        now = datetime.datetime.now(zoneinfo.ZoneInfo('America/Sao_Paulo'))

        scheduled = []

        with json_db.connect('db.json') as db:
            scheduled = db['scheduled']

        for event in scheduled:
            delta = datetime.datetime.fromisoformat(event['time']) - now

            if delta.total_seconds() / 3600 < 24:
                channel = self.bot.get_channel(event['channel'])

                await channel.send(f'{event["mention"]} - Later today: **{event["title"]}** ({event["time"]})')


    @nextcord.ext.tasks.loop(hours=1)
    async def remind_scheduled(self):
        now = datetime.datetime.now(zoneinfo.ZoneInfo('America/Sao_Paulo'))

        scheduled = []

        with json_db.connect('db.json') as db:
            scheduled = db['scheduled']

        async def await_scheduled(event):
            delta = datetime.datetime.fromisoformat(event['time']) - now

            channel = self.bot.get_channel(event['channel'])

            await channel.send(f'**{event["title"]}** starting in {delta} {event["mention"]}!')

            await asyncio.sleep(delta.total_seconds())

            await channel.send(f'{event["mention"]} **{event["title"]}** starting!')

            with json_db.connect('db.json') as db:
                db['scheduled'] = [e for e in db['scheduled'] if e['time'] != event['time']]

        await asyncio.gather(*[
            await_scheduled(event)
            for event in scheduled
            if (datetime.datetime.fromisoformat(event['time']) - now).total_seconds() < 3600
        ])
