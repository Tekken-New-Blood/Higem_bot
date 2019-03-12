import discord
import pandas as pd
import random
import difflib
from discord.ext import commands
import char_dict as chd
import sovets
import reasons

bot = commands.Bot(description='~~Умный бот для умных людей~~', command_prefix=('.higa ', '.higem ', '.framedata ', '.framebot '))

# names for pretty printing
HELPNAMES = ''
for i, j in chd.CHAR_NAMES.items():
    HELPNAMES += i + ' ' + str(j).replace("'", '') + '\n'


def get_channels():
    f = open('framedata_channels.txt', 'r')
    lines = f.readlines()
    f.close()
    return lines


# --------------------- COMMANDS ---------------------

# Mark the framedata servers
@bot.command()
@commands.has_permissions(manage_messages=True)
async def channel(ctx, chan):
    """Adds and removes a channel from a list of bot channels (in which the bot will not autodelete messages)."""
    chan_id = int(''.join(d for d in chan if d.isdigit()))
    for i in ctx.message.guild.channels:
        if i.id == chan_id:
            lines = get_channels()
# Open the file again and write to it
            f = open('framedata_channels.txt', 'w')
            str_id = str(i.id) + '\n'
            if str_id in lines:
                for line in lines:
                     if line != str_id:
                         f.write(line)
                await ctx.message.channel.send('Removed {} from bot channels'.format(i.mention))
            else:
                for line in lines:
                    f.write(line)
                f.write(str_id)
                await ctx.message.channel.send('Added {} to bot channels'.format(i.mention))
            f.close()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def channels(ctx):
    """Prints a list of channels in which the bot will not delete messages."""
    lines = get_channels()
    guild_channels = [x.mention for x in ctx.message.guild.channels for y in lines if str(x.id)+'\n' == y]
    await ctx.message.channel.send('The bot will not delete messages in following channels:\n'+'\n'.join(guild_channels))

@bot.command()
async def framebot(ctx):
    """Get the lates framedata bot link."""
    await ctx.send("Latest framedata bot can be found here:\nhttps://github.com/WAZAAAAA0/TekkenBot/releases")


@bot.command()
async def characters(ctx):
    """Prints a list of commands for each character."""
    await ctx.send(HELPNAMES)


@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.message.add_reaction('🙅')
    if isinstance(error, commands.MissingPermissions):
        pass


@bot.command(hidden=True)
@commands.cooldown(1, 90, commands.BucketType.user)
async def sovet(ctx):
    """Prints a random quote."""
    if ctx.message.guild.id == 193009632141246464:
        await ctx.send(random.choice(sovets.soveti), tts=True)
        await ctx.message.delete()

@bot.command(hidden=True)
@commands.cooldown(1, 90, commands.BucketType.user)
async def reason(ctx):
    """Prints a random quote."""
    if ctx.message.guild.id == 193009632141246464:
        await ctx.send(random.choice(reasons.REASONS), tts=True)
        await ctx.message.delete()


# --------------------- LISTS AND OTHER SHIT ---------------------
# Constant Variables
DELETE_TIME = 35
# Shortcuts for cleaning messages
DF = pd.read_csv('fdata.csv')
CHARS = set(DF['Character'].values)
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

# Move properties names to bring up a list of specific group
move_properties = {'Homing':      ['homing', 'track', 'tracking'],
                   'Power Crush': ['pc', 'powercrush', 'power-crush', 'power_crush', 'armor'],
                   'Tail Spin':   ['tailspin', 'spin', 's!', 'bound', 'ts', 's'],
                   'Wall Bounce': ['wallbounce', 'wall_bounce', 'wall-bounce', 'wb', 'wb!', 'bounce'],
                   'Rage Art':    ['ra', 'rageart', 'rage_art', 'rage-art'],
                   'Rage Drive':  ['rd', 'ragedrive', 'rage_drive', 'rage-drive'],
                   'Rage':        ['rage', 'ragemoves', 'rage_moves', 'rage-moves'],
                   'Punish':      ['punish', 'punishes', 'punishment']}

# Guides for !char guide
guides = {'Devil Jin':    ['https://youtu.be/xDgVkFq--Gc','https://www.youtube.com/watch?v=mAZ7OQ3z1qo'],
          'Anna':         ['https://www.youtube.com/watch?v=1_hUwGD2nPE','https://youtu.be/p7l6zqSzGH4?t=1417'],
          'Lei':          ['https://www.youtube.com/watch?v=KV3N61WP_Ek','https://youtu.be/QTHDC56ngmA'],
          'Armor King':   ['https://www.youtube.com/watch?v=ZBV-Mess3b8', 'https://www.youtube.com/watch?v=enlbeiclJQI'],
          'Marduk':       ['https://youtu.be/L-WfJ4yUaHc?list=PLSCxY9aJNnYp-UIPRHp9epAMR0zFBHyN4', 'https://youtu.be/y53M8AC9KU8'],
          'Julia':        ['https://www.youtube.com/watch?v=1_hUwGD2nPE', 'https://youtu.be/p7l6zqSzGH4?t=1417'],
          'Steve':        ['https://www.youtube.com/watch?v=MuUkgR9KecE','https://www.youtube.com/watch?v=SNudXDKWN-g'],
          'Eddy':         ['https://www.youtube.com/watch?v=BuE3GmmuSBo','https://www.youtube.com/watch?v=2pQ6IjWBk2w'],
          'Claudio':      ['https://www.youtube.com/watch?v=YMb6H9oD7XM','https://www.youtube.com/watch?v=BCPRWkxtSCE'],
          'Bob':          ['https://www.youtube.com/watch?v=QZw-0TU_PH4','https://www.youtube.com/watch?v=XgXxz9ZN3F8'],
          'Katarina':     ['https://www.youtube.com/watch?v=G_umBhQCyJA','https://www.youtube.com/watch?v=3W2tBHrxwjo'],
          'Asuka':        ['https://www.youtube.com/watch?v=YqyzRADB9CE','https://www.youtube.com/watch?v=KTl94pi8xLs'],
          'Lee':          ['https://www.youtube.com/watch?v=QxX5gldkDSg','https://www.youtube.com/watch?v=8-5aQfvK7p0'],
          'Heihachi':     ['https://www.youtube.com/watch?v=eHFtkh0mzzw','https://www.youtube.com/watch?v=EaiHRt8UUk0'],
          'Eliza':        ['https://www.youtube.com/watch?v=TtvShmYhNn4','https://www.youtube.com/watch?v=dVLeuuromFc'],
          'Kuma':         ['https://www.youtube.com/watch?v=tByVRu0qjqY','https://www.youtube.com/watch?v=lxwsy-0o7Bo'],
          'Lili':         ['https://www.youtube.com/watch?v=zY1gGHOXOGs','https://www.youtube.com/watch?v=ADcdfz3GUrk'],
          'Jack 7':       ['https://www.youtube.com/watch?v=7uc52tQ-Qn0','https://www.youtube.com/watch?v=XrHGayfz9dI'],
          'Dragunov':     ['https://www.youtube.com/watch?v=7sQv0KCYSaw','https://www.youtube.com/watch?v=RgwWQGvCbO8'],
          'Law':          ['https://www.youtube.com/watch?v=SOmfwwnhM80','https://www.youtube.com/watch?v=9FP2ndLpH30'],
          'Geese':        ['https://www.youtube.com/watch?v=WczkCFJFEME','https://www.youtube.com/watch?v=B_1xQUS7eiI'],
          'Master Raven': ['https://www.youtube.com/watch?v=HubfZnBXVpc','https://www.youtube.com/watch?v=a4scOA3Hwi8'],
          'Xiaoyu':       ['https://www.youtube.com/watch?v=5dF9RhySqmE','https://www.youtube.com/watch?v=h9Ixxlqfc04'],
          'Noctis':       ['https://www.youtube.com/watch?v=NHvWmKzPEmk','https://www.youtube.com/watch?v=WXIrahDASKA'],
          'Yoshimitsu':   ['https://www.youtube.com/watch?v=-hn1PMPwiDo','https://www.youtube.com/watch?v=ESlDCG7xHKE'],
          'Gigas':        ['https://www.youtube.com/watch?v=LTJEBOcXIRs','https://www.youtube.com/watch?v=a7ophIS3PRc'],
          'Bryan':        ['https://www.youtube.com/watch?v=zgigE4g7pkI','https://www.youtube.com/watch?v=_BNxWujs0V4'],
          'King':         ['https://www.youtube.com/watch?v=kwTYzKDmpcI','https://www.youtube.com/watch?v=XDfTov0vQ2w'],
          'Jin':          ['https://www.youtube.com/watch?v=PIRPREfNtSQ','https://www.youtube.com/watch?v=yfyfgap67Jc'],
          'Miguel':       ['https://www.youtube.com/watch?v=6lIaMOLe9B0','https://www.youtube.com/watch?v=QR1bfimS-iM'],
          'Feng':         ['https://www.youtube.com/watch?v=ec_LdFclpDQ','https://www.youtube.com/watch?v=rfhaQbMro3k'],
          'Josie':        ['https://www.youtube.com/watch?v=b5cr0JWK4LM','https://www.youtube.com/watch?v=tdtf982cxns'],
          'Kazuya':       ['https://www.youtube.com/watch?v=AuPxvHy0OPs','https://www.youtube.com/watch?v=q1n4Ch0zGWk'],
          'Kazumi':       ['https://www.youtube.com/watch?v=V9Ovs4aN9-o','https://www.youtube.com/watch?v=STo_1OFHJOc'],
          'Paul':         ['https://www.youtube.com/watch?v=znmVjRCgXxw','https://www.youtube.com/watch?v=BE_VrID4AbU'],
          'Alisa':        ['https://www.youtube.com/watch?v=-tvRq7D1vkc','https://www.youtube.com/watch?v=DunHsZOFm0U'],
          'Lucky Chloe':  ['https://www.youtube.com/watch?v=0hDftqiLCz8','https://www.youtube.com/watch?v=Z5EEaA-MD4o'],
          'Akuma':        ['https://www.youtube.com/watch?v=Ipp9rrVq2PI','https://www.youtube.com/watch?v=rHp4yU22J5s'],
          'Nina':         ['https://www.youtube.com/watch?v=fR6p-TclG5A','https://www.youtube.com/watch?v=doo0RVaJRtY'],
          'Shaheen':      ['https://www.youtube.com/watch?v=rCpWVb8CVLM','https://www.youtube.com/watch?v=F8Aceh6XgaI'],
          'Leo':          ['https://www.youtube.com/watch?v=-M8hTnhwFv8','https://www.youtube.com/watch?v=ltb2SjfZJIk'],
          'Hwoarang':     ['https://www.youtube.com/watch?v=3ML7ID4yiI8','https://www.youtube.com/watch?v=wlqKsox_lzA'],
          'Lars':         ['https://www.youtube.com/watch?v=G64fakZfqWI','https://www.youtube.com/watch?v=nSDTGdjMjPY']}

# --------------------- THE BOT ITSELF ---------------------


@bot.listen()
async def on_message(message):
    ms = message.content.strip()
    mch = message.channel
    mid = str(mch.id) + '\n'

    # is_command = ms.startswith('!')
    # not_empty = len(ms) > 1
    # valid_name_format = ms[1:].split(' ')[0][0].isalpha()
    # no_other_commands = not ms.startswith('!join') and not ms.startswith('!play') and not ms.startswith('!skip')
    # valid_input = is_command and not_empty and valid_name_format and no_other_commands

    if ms.startswith('!') and len(ms) > 1 and ms[1:].split(' ')[0][0].isalpha() and not ms.startswith('!join') \
            and not ms.startswith('!play') and not ms.startswith('!skip'):
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
# Moves with properties
        if notation in [item for sublist in list(move_properties.values()) for item in sublist]:
            for key,val in move_properties.items():
                if notation in val:
                    notation = key
                    doubles = []
                    emb = discord.Embed(description='', title='{}\'s {} moves.'.format(name, notation))
                    for i in DF.loc[(DF['Character'] == name) & (DF['Notes'].str.contains(notation))].values:
                        if i[9] not in doubles:
                            doubles.append(i[9])
                            emb.add_field(name=i[9], value='Attack Level - {}\n Damage - {}\n Startup - {}\n '
                                                           'On Block - {}\n On Hit - {}\n On CH - {}\n Prop. - {}'
                                          .format(i[2], i[3], i[4], i[5], i[6], i[7], i[8]))

                    if len(DF.loc[(DF['Character'] == name) & (DF['Notes'].str.contains(notation))].values) == 0:
                        # Send a message
                        if mid in get_channels():
                            await mch.send('{} has no {} moves :('.format(name,notation))
                        else:
                            await mch.send('{} has no {} moves :('.format(name, notation), delete_after=DELETE_TIME)

                    else:
                        # Send a message
                        if mid in get_channels():
                            await mch.send(embed=emb)
                        else:
                            await mch.send(embed=emb, delete_after=DELETE_TIME)
# lei stances
        elif name == 'Lei' and notation == 'stances':
            stances = ['**SNK** - Snake Stance',
                       '**sSNA** - Sitting Snake Stance',
                       '**DRG** - Dragon Stance',
                       '**PAN** - Panther Stance',
                       '**DRU** - Drunken Stance',
                       '**CRA** - Crane Stance',
                       '**TGR** - Tiger Stance',
                       '**PHX** - Phoenix Stance',
                       '**BT** - Back turned Stance',
                       '**KND** - Knockdown Stance: face up, feet towards the opponent, entered by __d+3+4__',
                       '**FCD** - Facedown Stance: face down feet towards, entered by __d+1+2__',
                       '**SLD** - Slide Stance: face down, feet away, entered by __d+1+4__',
                       '**PLD** - Playdead Stance: face up, feet away, entered by __d+2+3__']

            emb = discord.Embed(description='Full names for Lei stances', title='Lei stances')
            for i in stances:
                stance = i.split('**')
                if stance[1] == 'KND':
                    emb.add_field(name='\u200b', value='\u200b')
                    emb.add_field(name='\u200b', value='\u200b')
                emb.add_field(name=stance[1], value=stance[2].split('- ')[1])
            # Send a message
            if mid in get_channels():
                await mch.send(embed=emb)
            else:
                await mch.send(embed=emb, delete_after=DELETE_TIME)
# Guides
        elif notation == 'guide':
            if message.guild.id == 193009632141246464:
                # Send a message
                if mid in get_channels():
                    await mch.send(guides[name][1])
                else:
                    await mch.send(guides[name][1], delete_after=DELETE_TIME)
            else:
                # Send a message
                if mid in get_channels():
                    await mch.send(guides[name][0])
                else:
                    await mch.send(guides[name][0], delete_after=DELETE_TIME)


# Search for the char and move
        else:
            try:
                m = DF.loc[(DF['Character'] == name) & (DF['Command'] == notation)].values[0]
                h = ['Hit Level', 'Damage', 'Startup', 'On Block', 'On Hit', 'On CH', 'Notes']
                for i in range(len(m)):
                    if pd.isnull(m[i]):
                        m[i] = '-'
# Search for the char
                emb = discord.Embed(description='**Move: {}**'.format(m[9]), title='{}'.format(name))
                for i in range(len(m[2:-1])):
                    emb.add_field(name=h[i], value=m[2:-1][i])
                # Send a message
                if mid in get_channels():
                    await mch.send(embed=emb)
                else:
                    await mch.send(embed=emb, delete_after=DELETE_TIME)
            except Exception as e:
                if name not in CHARS:
                    guess_c = difflib.get_close_matches(name.capitalize(), CHARS, n=2, cutoff=0.6)
                    # Send a message
                    if mid in get_channels():
                        await mch.send('Character not found: **{}**.'.format(name))
                    else:
                        await mch.send('Character not found: **{}**.'.format(name), delete_after=DELETE_TIME)
                    if guess_c:
                        # Send a message
                        if mid in get_channels():
                            await mch.send('Maybe you meant this character(s)?: **{}**'
                                           .format('**, **'.join(guess_c)))
                        else:
                            await mch.send('Maybe you meant this character(s)?: **{}**'
                                           .format('**, **'.join(guess_c)), delete_after=DELETE_TIME)
# Search for the move
                else:
                    try:
                        moves = DF.loc[DF['Character'] == name]['Notation'].values
                        guess_m = difflib.get_close_matches(full_notation, moves, n=5, cutoff=0.5)
                        # Send a message
                        if mid in get_channels():
                            await mch.send('Move not found for {}: **{}**.'.format(name, full_notation))
                        else:
                            await mch.send('Move not found for {}: **{}**.'.format(name, full_notation), delete_after=DELETE_TIME)
                        if guess_m:
                            # Send a message
                            if mid in get_channels():
                                await mch.send('Maybe you meant:\n**{}**'.format('**; **\n'.join(guess_m)))
                            else:
                                await mch.send('Maybe you meant:\n**{}**'.format('**; **\n'.join(guess_m)), delete_after=DELETE_TIME)
                        else:
                            moves = DF.loc[DF['Character'] == name]['Command'].values
                            guess_m = difflib.get_close_matches(notation, moves, n=5, cutoff=0.5)
                            if guess_m:
                                # Send a message
                                if mid in get_channels():
                                    await mch.send('Maybe you meant: **{}**'.format('**; **'.join(guess_m)))
                                else:
                                    await mch.send('Maybe you meant: **{}**'.format('**; **'.join(guess_m)), delete_after=DELETE_TIME)

                    except Exception as e:
                        print(e)
        if mid not in get_channels():
            await message.delete()

bot.run("NDE2NjQzNTE1MDg3MzIzMTU3.DdHSWA.sV9BLs5rJ0QCnJiSRjPBoZ7-WO8")
