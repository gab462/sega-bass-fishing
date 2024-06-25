import nextcord
import nextcord.ext.commands
import json
import random
import copy
import json_db


class BookClub(nextcord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with json_db.connect('db.json') as db:
            if 'chosen' not in db.keys():
                db['chosen'] = []
            if 'books' not in db.keys():
                db['books'] = {}


    @nextcord.slash_command(description='Define books')
    async def define_books(self, interaction,
                   input=nextcord.SlashOption(description='Books', required=True)):
        words = books.split(' ')
        pairs = zip(res[::2], res[1::2])
        keys = set(map(lambda x: x[0], pairs))
        mapping = dict(map(lambda key: (key, []), keys))

        for owner, book in pairs:
            mapping[owner].append(book)

        with json_db.connect('db.json') as db:
            db['books'] = mapping

        await interaction.response.send_message(str(mapping))


    @nextcord.slash_command(description='Define chosen')
    async def define_chosen(self, interaction,
                   name=nextcord.SlashOption(description='Name', required=True)):
        with json_db.connect('db.json') as db:
            db['chosen'].append(name)

        await interaction.response.send_message(f'{name} is now excluded from this round')


    @nextcord.slash_command(description='Get books')
    async def get_books(self, interaction):
        books = ''

        with json_db.connect('db.json') as db:
            books = json.dumps(db['books'])

        await interaction.response.send_message(books)


    @nextcord.slash_command(description='Get chosen')
    async def get_chosen(self, interaction):
        chosen = ''

        with json_db.connect('db.json') as db:
            chosen = json.dumps(db['chosen'])

        await interaction.response.send_message(chosen)


    @nextcord.slash_command(description='Draw next book')
    async def draw_book(self, interaction):
        collection = []
        chosen = []

        with json_db.connect('db.json') as db:
            collection = db['books'].items()
            chosen = db['chosen']

        chooseable = filter(lambda x: x[0] not in chosen, collection)
        flatten = lambda xss: [x for xs in xss for x in xs]
        choice = random.choice(flatten(map(lambda x: x[1], chooseable)))

        newly_chosen = filter(lambda x: choice in x[1], collection)
        newly_chosen = next(newly_chosen)
        newly_chosen = newly_chosen[0]

        new_collection = copy.deepcopy(dict(collection))
        new_collection[newly_chosen] = list(filter(lambda x: x != choice, dict(collection)[newly_chosen]))

        with json_db.connect('db.json') as db:
            if len(db['chosen']) + 1 >= len(db['books'].keys()):
                db['chosen'] = []
            else:
                db['chosen'].append(newly_chosen)

            db['books'] = new_collection

        await interaction.response.send_message(f'Livro escolhido: {choice}')
