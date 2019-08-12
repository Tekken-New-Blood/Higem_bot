import discord
# from discord.ext import commands
import char_dict as chd
import csv
import re

frame_data=dict()
'''
csv is formatted like
Character,Command,Hit level,Damage,Start up frame,Block frame,Hit frame,Counter hit frame,Notes,Notation

{'Akuma': 
    {'rage11b32': 
        OrderedDict(
            [
                ('Hit level', 'm (Throw)'), 
                ('Damage', '55'), 
                ('Start up frame', '16 pc8~'), 
                ('Block frame', 'Throw(KND)'), 
                ('Hit frame', 'Throw(KND)'), 
                ('Counter hit frame', 'Throw(KND)'), 
                ('Notes', 'Rage Art'), 
                ('Notation', 'In Rage 1,1,f+3,2')
            ]
        ),
...
'''
with open('fdata.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        character = row.pop('Character')
        command = row.pop('Command')
        data = {command : dict(row)}
        if character in frame_data:
            frame_data[character].update(data)
        else:
            frame_data[character] = data

print(frame_data)

CHARS = set(frame_data.keys())
SWAP = {' ':   '',
        ',':   '',
        '/':   '',
        'd+':  'd',
        'f+':  'f',
        'u+':  'u',
        'b+':  'b',
        'n+':  'n',
        'ws+': 'ws',
        'fc+': 'fc',
        'cd+': 'cd',
        'ss+': 'ss',
        'ra+': 'ra',
        'rd+': 'rd',
        'wr+': 'wr',
        '(':   '',
        ')':   '',
        '[':   '',
        ']':   '',
        '?':   ''}

class Higem(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        ms = message.content.strip()
        mch = message.channel
        mid = str(mch.id) + '\n'
        syntax = "!CHAR COMMAND"
        name = ""
        notation = ""
        if ms.startswith('!') and len(ms) > 1:
            msg = ms[1:]
            name = msg.split(' ')[0].lower()
            if len(msg.split(' ')) > 1:
                full_notation = msg.split(name[-2:] + ' ')[1]
                notation = full_notation.lower()
                for i, j in SWAP.items():
                    notation = notation.replace(i, j)
            else:
                full_notation = ''
                notation = ''
            if name in [item for sublist in list(chd.CHAR_NAMES.values()) for item in sublist]:
                for key, val in chd.CHAR_NAMES.items():
                    if name in val:
                        name = key
            elif ''.join(msg.split(' ')[:2]).lower() in \
                [item for sublist in list(chd.CHAR_NAMES.values()) for item in sublist]:
                name = ''.join(msg.split(' ')[:2]).lower()
                for key, val in chd.CHAR_NAMES.items():
                    if name in val:
                        full_notation = msg.split(name[-2:] + ' ')[1]
                        notation = full_notation.lower()
                        for i, j in SWAP.items():
                            notation = notation.replace(i, j)
                        name = key

            if name in frame_data:
                if notation in frame_data[name]:
                    emb = discord.Embed(description='**Move: {}**'.format(notation), title='{}'.format(name))
                    print(frame_data[name][notation])
                    print(list(frame_data[name][notation].keys()))
                    for k in list(frame_data[name][notation].keys()):
                        v = frame_data[name][notation][k]
                        if v is not None and len(v) > 0:
                            emb.add_field(name=k, value=frame_data[name][notation][k])
                    print(emb)
                    await mch.send(embed=emb)
                else:
                    await mch.send("Can't find that move for Character: {}".format(name))
            else:
                await mch.send("Can't find Character with that name")


client = Higem()
fh = open('higemkey.conf', 'r')
higem_key = fh.readline().rstrip()
client.run(higem_key)