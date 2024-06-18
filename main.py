import nextcord.ext.commands
import re
import json
import urllib
from base import Base
from randomize import Randomize
from book_club import BookClub
from remind import Remind


def get_phrases(url):
    txt = ''

    with urllib.request.urlopen(url) as page:
        txt = page.read().decode('utf-8')

    txt = re.sub(r'[\r_]', '\n', txt)
    txt = txt.split('\n')
    txt = filter(bool, txt)
    txt = list(txt)
    txt = txt[4:]
    txt = zip(txt[::3], txt[1::3], txt[2::3])

    msgs = []

    for t in txt:
        date, phrase, description = t
        msgs.append('\n'.join(['# ' + phrase,
                               '**' + description + '**',
                               '_' + date + '_']))

    return msgs


def main():
    config = {}

    with open('env.json', 'r') as f:
        config = json.loads(f.read())

    bot = nextcord.ext.commands.Bot(default_guild_ids=config['guilds'])

    bot.add_cog(Base(bot))
    bot.add_cog(Randomize(bot, lambda: get_phrases(config['phrases'])))
    bot.add_cog(BookClub(bot))
    bot.add_cog(Remind(bot))

    bot.run(config['token'])


if __name__ == '__main__':
    main()
