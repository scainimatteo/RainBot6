from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from os import environ
from socket import *
import logging
import json

serverName = 'localhost'
serverPort = int(environ['R6SSPORT'])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
STATS, LISTA = range(2)

ranks = {
        "rame V" : 1200,
        "rame IV" : 1300,
        "rame III" : 1400,
        "rame II" : 1500,
        "rame I" : 1600,

        "bronzo V" : 1700,
        "bronzo IV" : 1800,
        "bronzo III" : 1900,
        "bronzo II" : 2000,
        "bronzo I" : 2100,

        "argento V" : 2200,
        "argento IV" : 2300,
        "argento III" : 2400,
        "argento II" : 2500,
        "argento I" : 2600,

        "oro III" : 2800,
        "oro II" : 3000,
        "oro I" : 3200,

        "platino III" : 3600,
        "platino II" : 4000,
        "platino I" : 4400,

        "diamante" : 5000,

        "champion" : 10000
        }

def stats(update, context):
    global chatid
    chatid = update.effective_chat.id
    user = update.effective_chat.username
    f = open('requesters.txt', 'a')
    f.write(user + '\n')
    f.close()
    context.bot.send_message(chat_id = chatid, text = "Manda la gamertag del giocatore")
    return STATS

def retstats(update, context):
    dict = {}
    dict['name'] = update.message.text
    dict['request'] = '1'
    jsonrequest = json.dumps(dict)
    clientSocket.send(jsonrequest.encode('utf-8'))
    ret = clientSocket.recv(2048)
    stats = json.loads(ret)
    message = '- - - - - STATISTICHE GENERALI - - - - -'
    context.bot.send_message(chat_id = chatid, text = message)
    name = stats['name']
    level = stats['level']
    kill = stats['kill']
    death = stats['death']
    kd = stats['kd']
    diff = kill - death
    message = '%s (livello %d) ha totalizzato %s kill e %s morti con un kd di %.3f [%s]' % (name, level, kill, death, kd, diff)
    context.bot.send_message(chat_id = chatid, text = message)
    win = stats['win']
    lose = stats['lose']
    vs = stats['vs']
    diff = win - lose
    message = 'ha %s partite vinte e %s sconfitte con un vs di %.2f [%s]' % (win, lose, vs, diff)
    context.bot.send_message(chat_id = chatid, text = message)
    mmr = int(stats['mmr'])
    rankmmr = ''
    for i in ranks:
        if mmr > ranks[i]:
            rankmmr = i
        else:
            rankmmr = i
            break
    maxmmr = int(stats['maxmmr'])
    rankmaxmmr = ''
    for j in ranks:
        if maxmmr > ranks[j]:
            rankmaxmmr = j
        else:
            rankmaxmmr = j
            break
    message = 'attualmente ha %d punti (%s) e ha raggiunto un massimo di %d (%s)' % (mmr, rankmmr, maxmmr, rankmaxmmr)
    context.bot.send_message(chat_id = chatid, text = message)
    message = '- - - - - STATISTICHE STAGIONALI - - - - -'
    context.bot.send_message(chat_id = chatid, text = message)
    skill = stats['skill']
    sdeath = stats['sdeath']
    skd = stats['skd']
    diff = skill - sdeath
    message = 'in questa stagione %s ha totalizzato %s kill e %s morti con un kd di %.3f [%s]' % (name, skill, sdeath, skd, diff)
    context.bot.send_message(chat_id = chatid, text = message)
    swin = stats['swin']
    slose = stats['slose']
    svs = stats['svs']
    diff = swin - slose
    message = 'ha vinto %s partite e ne ha perse %s con un vs di %.2f [%s]' % (swin, slose, svs, diff)
    context.bot.send_message(chat_id = chatid, text = message)
    message = '- - - - - OPERATORI - - - - -'
    context.bot.send_message(chat_id = chatid, text = message)
    atktime = stats['atktime']
    atk = stats['atk']
    mins, sec = divmod(atktime, 60)
    hours, mins = divmod(mins, 60)
    akd = stats['akd']
    avs = stats['avs']
    message = "l'attaccante più usato è %s con %dh%dm con un kd di %.3f e un vs di %.2f" % (atk, hours, mins, akd, avs)
    context.bot.send_message(chat_id = chatid, text = message)
    dfdtime = stats['dfdtime']
    dfd = stats['dfd']
    mins, sec = divmod(dfdtime, 60)
    hours, mins = divmod(mins, 60)
    dkd = stats['dkd']
    dvs = stats['dvs']
    message = "il difensore più usato è %s con %dh%dm con un kd di %.3f e un vs di %.2f" % (dfd, hours, mins, dkd, dvs)
    context.bot.send_message(chat_id = chatid, text = message)

    return ConversationHandler.END

def lista(update, context):
    global chatid
    chatid = update.effective_chat.id
    user = update.effective_chat.username
    f = open('requesters.txt', 'a')
    f.write(user + '\n')
    f.close()
    message = "Manda la gamertag del giocatore, che operatori vuoi(attaccanti o difensori) e per quale statistica ordinare la lista (time, kd, vs)\nes: ITAP Scaini, attaccanti, kd"
    context.bot.send_message(chat_id = chatid, text = message)
    return LISTA

def retlista(update, context):
    dict = {}
    ritorno = update.message.text
    strsplit = ritorno.split(", ")
    dict['name'] = strsplit[0]
    dict['oper'] = strsplit[1]
    dict['type'] = strsplit[2]
    dict['request'] = '2'

    jsonrequest = json.dumps(dict)
    clientSocket.send(jsonrequest.encode('utf-8'))

    ret1 = clientSocket.recv(2048)
    ret2 = clientSocket.recv(4096)
    playername = json.loads(ret1)
    retdict = json.loads(ret2)

    if dict['oper'] == 'attaccanti':
        message = "lista degli attaccanti di %s ordinati per %s:" % (playername, dict['type'])
        context.bot.send_message(chat_id = chatid, text = message)
    elif dict['oper'] == 'difensori':
        message = "lista dei difensori di %s ordinati per %s:" % (playername, dict['type'])
        context.bot.send_message(chat_id = chatid, text = message)

    for i in retdict:
        name = i
        temp = retdict[i]['time']
        min, sec = divmod(temp, 60)
        hour, min = divmod(min, 60)
        kill = retdict[i]['kill']
        kd = retdict[i]['kd']
        win = retdict[i]['win']
        vs = retdict[i]['vs']
        if temp != 0:
            message = "%s giocato %dh%dm con kd di %.3f (%d kill) e con vs di %.2f (%d win)" % (name, hour, min, kd, kill, vs, win)
            context.bot.send_message(chat_id = chatid, text = message)

    return ConversationHandler.END

def cancel(update, context):
    return ConversationHandler.END

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error(update, context):
    logger.warning('update "%s" caused errore "%s"', update, context.error)

def main():
    bot = Updater(environ['R6STOKEN'], use_context=True)

    dp = bot.dispatcher

    Stats_conv = ConversationHandler(
            entry_points = [CommandHandler('stats', stats)],

            states = {
                STATS: [MessageHandler(Filters.text, retstats)]
                },
            
            fallbacks = [CommandHandler('cancel', cancel)]
            )

    List_conv = ConversationHandler(
            entry_points = [CommandHandler('lista', lista)],

            states = {
                LISTA: [MessageHandler(Filters.text, retlista)]
                },
            
            fallbacks = [CommandHandler('cancel', cancel)]
            )

    dp.add_handler(Stats_conv)
    dp.add_handler(List_conv)

    dp.add_error_handler(error)

    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()
