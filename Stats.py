# script per la richiesta delle statistiche di Rainbow
from operator import attrgetter
from pprint import pprint
from os import environ
from time import sleep
from socket import *
import asyncio
import r6sapi
import json

jsonsend = ''
attackers = ['ace', 'amaru', 'ash', 'blackbeard', 'blitz', 'buck', 'capitão', 'dokkaebi', 'finka', 'fuze', 'glaz', 'gridlock', 'hibana', 'iana', 'iq', 'jackal', 'kali', 'lion', 'maverick', 'montagne', 'nomad', 'nokk', 'sledge', 'thatcher', 'thermite', 'twitch', 'ying', 'zero', 'zofia']
defenders=['alibi', 'bandit', 'castle', 'caveira', 'clash', 'doc', 'echo', 'ela', 'frost', 'goyo', 'jager', 'kaid', 'kapkan', 'lesion', 'maestro', 'melusi', 'mira', 'mozzie', 'mute', 'oryx', 'pulse', 'rook', 'smoke', 'tachanka', 'valkyrie', 'vigil', 'wamai', 'warden']

class playerstat():
    def __init__(self, nome, level, kill, death, kd, win, lose, vs, skill, sdeath, skd, swin, slose, svs, mmr, maxmmr, atktime, atk, akd, avs, dfdtime, dfd, dkd, dvs):
        self.name = nome
        self.level = level
        self.kill = kill
        self.death = death
        self.kd = kd
        self.win = win
        self.lose = lose
        self.vs = vs
        self.skill = skill
        self.sdeath = sdeath
        self.skd = skd
        self.swin = swin
        self.slose = slose
        self.svs = svs
        self.mmr = mmr
        self.maxmmr = maxmmr
        self.atktime = atktime
        self.atk = atk
        self.akd = akd
        self.avs = avs
        self.dfdtime = dfdtime
        self.dfd = dfd
        self.dkd = dkd
        self.dvs = dvs

async def statsret(nome):
    global jsonsend

    auth = r6sapi.Auth(environ['R6SMAIL'], environ['R6SPASS'])
    name = nome
    player = await auth.get_player(name, r6sapi.Platforms.XBOX)

    await player.load_general()
    await player.load_queues()
    await player.load_all_operators()
    await player.load_level()
    rank = await player.get_rank('emea')

    name = player.name
    f = open('player.txt', 'a')
    f.write(name + '\n')
    f.close()
    level = player.level
    kill = player.ranked.kills
    death = player.ranked.deaths
    kd = kill / death
    win = player.ranked.won
    lose = player.ranked.lost
    vs = win / lose
    id = player.id
    skill = player._last_data['players'][id]['kills']
    sdeath = player._last_data['players'][id]['deaths']
    skd = skill / sdeath
    swin = player._last_data['players'][id]['wins']
    slose = player._last_data['players'][id]['losses']
    svs = swin / slose
    mmr = rank.mmr
    maxmmr = rank.max_mmr
    atktime = 0
    dfdtime = 0
    atk = ''
    dfd = ''
    for i in player.operators:
        nameop = player.operators[i].name
        time = player.operators[i].time_played
        if nameop in attackers:
            if time > atktime:
                atktime = time
                atk = nameop
        elif nameop in defenders:
            if time > dfdtime:
                dfdtime = time
                dfd = nameop
    akill = player.operators[atk].kills
    adeath = player.operators[atk].deaths
    akd = akill / adeath
    awin = player.operators[atk].wins
    alose = player.operators[atk].losses
    avs = awin / alose
    dkill = player.operators[dfd].kills
    ddeath = player.operators[dfd].deaths
    dkd = dkill / ddeath
    dwin = player.operators[dfd].wins
    dlose = player.operators[dfd].losses
    dvs = dwin / dlose
    new_pl = playerstat(name, level, kill, death, kd, win, lose, vs, skill, sdeath, skd, swin, slose, svs, mmr, maxmmr, atktime, atk, akd, avs, dfdtime, dfd, dkd, dvs)
    pl_dict = new_pl.__dict__
    jsonsend = json.dumps(pl_dict)
    
    await auth.close()    

# ho le liste attackers e defenders che contengono i nomi e la lista operators per aggiungere gli oggetti singleop
async def listret(nome, oper, type):
    global jsonsend
    op_dict = {}
    sortlist = []

    auth = r6sapi.Auth("galilei.scaini.02031999@gmail.com", "Danigiomat71")
    name = nome
    player = await auth.get_player(name, r6sapi.Platforms.XBOX)

    await player.load_general()
    await player.load_all_operators()

    playername = player.name
    f = open('player.txt', 'a')
    string = '%s, %s, %s' % (playername, oper, type)
    f.write(string + '\n')
    f.close()

    if oper == 'attaccanti':
        for i in player.operators:
            name = player.operators[i].name
            if name in attackers:
                op_dict[name] = {}
                op_dict[name]['time'] = player.operators[i].time_played
                kill = player.operators[i].kills
                op_dict[name]['kill'] = kill
                death = player.operators[i].deaths
                if death == 0:
                    death = 1
                op_dict[name]['kd'] = kill / death
                win = player.operators[i].wins
                op_dict[name]['win'] = win
                lose = player.operators[i].losses
                if lose == 0:
                    lose = 1
                op_dict[name]['vs'] = win / lose
    elif oper == 'difensori':
        for i in player.operators:
            name = player.operators[i].name
            if name in defenders:
                op_dict[name] = {}
                op_dict[name]['time'] = player.operators[i].time_played
                kill = player.operators[i].kills
                op_dict[name]['kill'] = kill
                death = player.operators[i].deaths
                if death == 0:
                    death = 1
                op_dict[name]['kd'] = kill / death
                win = player.operators[i].wins
                op_dict[name]['win'] = win
                lose = player.operators[i].losses
                if lose == 0:
                    lose = 1
                op_dict[name]['vs'] = win / lose

    sortdict = sorted (op_dict, key = lambda x: op_dict[x][type], reverse = True)
    newdict = {}
    for i in sortdict:
        newdict[i] = op_dict[i]
    lenlist = len(newdict)
    jsonsend = json.dumps(playername)
    connectionSocket.send(jsonsend.encode('utf-8'))
    jsonsend = json.dumps(newdict)
    connectionSocket.send(jsonsend.encode('utf-8'))

async def main():
    global connectionSocket
    serverPort = int(environ['R6SSPORT'])

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)

    while 1:
        print('Server pronto')
        connectionSocket, clientAddress = serverSocket.accept()
        print('Server connesso con:', clientAddress)
        while 1:
            ret = connectionSocket.recv(4096)
            dict = json.loads(ret)
            if dict['request'] == '1':
                f = open('player.txt', 'a')
                f.write("stats: ")
                f.close()
                await statsret(dict['name'])
                connectionSocket.send(jsonsend.encode('utf-8'))
            elif dict['request'] == '2':
                f = open('player.txt', 'a')
                f.write('lista: ')
                f.close()
                await listret(dict['name'], dict['oper'], dict['type'])
            elif dict['request'] == '4':
                break
        connectionSocket.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
