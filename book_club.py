import nextcord
import nextcord.ext.commands
import json
import random
import copy


class BookClub(nextcord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @nextcord.slash_command(description='Define books')
    async def define_books(self, interaction,
                   input=nextcord.SlashOption(description='Books', required=True)):
        words = books.split(' ')
        pairs = zip(res[::2], res[1::2])
        keys = set(map(lambda x: x[0], pairs))
        mapping = dict(map(lambda key: (key, []), keys))

        for owner, book in pairs:
            mapping[owner].append(book)

        with open('books.json', 'w+') as f:
            f.write(json.dumps(mapping))

        await interaction.response.send_message(str(mapping))


    @nextcord.slash_command(description='Define chosen')
    async def define_chosen(self, interaction,
                   name=nextcord.SlashOption(description='Name', required=True)):
        with open('chosen.txt', 'a+'):
            f.write(name + '\n')

        await interaction.response.send_message(f'{name} is now excluded from this round')


    @nextcord.slash_command(description='Get books')
    async def get_books(self, interaction):
        books = ''
        with open('books.json', 'r') as f:
            books = f.read()

        await interaction.response.send_message(books)


    @nextcord.slash_command(description='Get chosen')
    async def get_chosen(self, interaction):
        chosen = ''
        with open('chosen.txt', 'r') as f:
            chosen = f.read()

        await interaction.response.send_message(chosen)


    @nextcord.slash_command(description='Draw next book')
    async def draw_book(self, interaction):
        collection = []
        chosen = []

        with open('books.json', 'r') as f:
            collection = json.loads(f.read()).items()

        with open('chosen.txt', 'r') as f:
            chosen = f.read().split('\n')

        chooseable = filter(lambda x: x[0] not in chosen, collection)
        flatten = lambda xss: [x for xs in xss for x in xs]
        choice = random.choice(flatten(map(lambda x: x[1], chooseable)))

        newly_chosen = filter(lambda x: choice in x[1], collection)
        newly_chosen = next(newly_chosen)
        newly_chosen = newly_chosen[0]

        new_collection = copy.deepcopy(dict(collection))
        new_collection[newly_chosen] = list(filter(lambda x: x != choice, dict(collection)[newly_chosen]))

        if len(list(filter(bool, chosen))) + 1 >= len(list(map(lambda x: x[0], collection))):
            with open('chosen.txt', 'w+') as f:
                f.write('')
        else:
            with open('chosen.txt', 'a+') as f:
                f.write(f'\n{newly_chosen}\n')

        with open('books.json', 'w') as f:
            f.write(json.dumps(new_collection))

        await interaction.response.send_message(f'Livro escolhido: {choice}')
