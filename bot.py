# bot.py
# The code for the bot
import pandas as pd
import cfg
import utils
import socket
import re
import time
import _thread
from time import sleep
import difflib
import char_dict as chd


def main():
    # Load framedata from csv
    df = pd.read_csv('fdata.csv')
    chars = set(df['Character'].values)
    swap = {' ': '',
            ',': '',
            '/': '',
            'd+': 'd',
            'f+': 'f',
            'u+': 'u',
            'b+': 'b',
            'n+': 'n',
            'ws+': 'ws',
            'fc+': 'fc',
            'cd+': 'cd',
            'wr+': 'wr',
            'ra+': 'ra',
            'rd+': 'rd',
            'ss+': 'ss',
            '(': '',
            ')': ''}
    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send('PASS {}\r\n'.format(cfg.PASS).encode('utf-8'))
    s.send('NICK {}\r\n'.format(cfg.NICK).encode('utf-8'))
    for i in range(len(cfg.CHAN)):
        s.send('JOIN #{}\r\n'.format(cfg.CHAN[i]).encode('utf-8'))

    chat_msg = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')
    for i in range(len(cfg.CHAN)):
        utils.chat(s, "Hi everyone! This is a CIS T7 framedata bot. !help for a list of commands.", cfg.CHAN[i])
    uptime = time.time()
    _thread.start_new_thread(utils.threadFillOpList, ())

    while True:
        response = s.recv(1024).decode('utf-8')
        try:
            channel = response.split('#')[1].split(' ')[0]
        except Exception as e:
            channel = ''
        if response == 'PING :tmi.twitch.tv\r\n':
            s.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
        else:
            username = re.search(r'\w+', response).group(0)
            message = chat_msg.sub('', response)
            #print(response)

            # --------------------------CUSTOM COMMANDS--------------------------
            ms = message.strip()
            #print(ms)
            if ms == '!help':
                utils.chat(s, 'List of commands - pastebin.com/cra4fLgQ', channel)

            if ms == '!info':
                utils.chat(s, 'CIS T7 for framedata and more! Made by eatsports - twitch.tv/mousewell/ '
                              'I\'m renting a server to keep this bot running, '
                              'if you like this bot, please consider donating at my twitch page!', channel)

            if ms == '!characters':
                utils.chat(s, 'List of characters - ' + ' '.join(sorted(chars)) +
                           ' (!%character% %move% to get frame data)', channel)

            # --------------------------FRAMEDATA--------------------------
            if ms.startswith('!') and len(ms) > 1 and ms[1:].split(' ')[0][0].isalpha() \
                    and not ms.startswith('!sr') and not ms.startswith('!song') and not ms.startswith('!device')\
                    and not ms.startswith('!chars'):
                msg = ms[1:]
                name = msg.split(' ')[0].lower()
                if len(msg.split(' ')) > 1:
                    full_notation = msg.split(name[-2:] + ' ')[1]
                    notation = full_notation.lower()
                    for i, j in swap.items():
                        notation = notation.replace(i,j)
                else:
                    full_notation = ''
                    notation = ''

                if name in [item for sublist in list(chd.CHAR_NAMES.values()) for item in sublist]:
                    for key, val in chd.CHAR_NAMES.items():
                        if name in val:
                            name = key

                elif ''.join(msg.split(' ')[:2]).lower() \
                        in [item for sublist in list(chd.CHAR_NAMES.values()) for item in sublist]:
                    name = ''.join(msg.split(' ')[:2]).lower()
                    for key, val in chd.CHAR_NAMES.items():
                        if name in val:
                            full_notation = msg.split(name[-2:] + ' ')[1]
                            notation = full_notation.lower()
                            for i, j in swap.items():
                                notation = notation.replace(i,j)
                            name = key

                try:
                    m = df.loc[(df['Character'] == name) & (df['Command'] == notation)].values[0]
                    for i in range(len(m)):
                        if pd.isnull(m[i]):
                            m[i] = '-'
                    
                    output = 'Hit Level: {} ' \
                             'Startup: {} ' \
                             'On Block: {} ' \
                             'On Hit: {} ' \
                             'On CH: {} ' \
                             'Damage: {} ' \
                             'Notes: {}'.format(m[2], m[4], m[5], m[6], m[7], m[3], m[8])
                    utils.chat(s, output, channel)
                except Exception as e:
                    if name not in chars:
                        guess_c = difflib.get_close_matches(name.capitalize(), chars, n=2, cutoff=0.6)
                        utils.chat(s, 'Character not found: {}.'.format(name), channel)
                        if guess_c:
                            utils.chat(s, 'Maybe you meant this character(s)?: '
                                          '{}'.format(', '.join(guess_c)), channel)
                    else:
                        try:
                            moves = df.loc[df['Character'] == name]['Notation'].values
                            guess_m = difflib.get_close_matches(full_notation, moves, n=5, cutoff=0.5)
                            utils.chat(s, 'Move not found for {}: {}.'.format(name, full_notation), channel)
                            if guess_m:
                                utils.chat(s, 'Maybe you meant: {}'.format('; '.join(guess_m)), channel)
                            else:
                                moves = df.loc[df['Character'] == name]['Command'].values
                                guess_m = difflib.get_close_matches(notation, moves, n=5, cutoff=0.5)
                                if guess_m:
                                    utils.chat(s, 'Maybe you meant: {}'.format(' or '.join(guess_m)), channel)
                        except Exception as e:
                            print(e)

            if ms == '!uptime':
                diff = time.time() - uptime
                utils.chat(s, 'Went live {}h {}m ago.'.format(
                    str(diff/3600)[:1], str(diff/60)[:1]), channel)

            if ms == '!time':
                utils.chat(s, 'It is currently ' + time.strftime('%I:%M %p %Z on %A, %B %d, %Y.'), channel)

            if ms == '!messages' and utils.isOp(username):
                utils.chat(s, "Please give me a follow at twitch.tv/mousewell", channel)
                utils.chat(s, "Go to twitter.com/mousewell1 for my Twitter", channel)
        sleep(1)


if __name__ == "__main__":
    main()
