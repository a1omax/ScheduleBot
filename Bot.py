from schedule import schedule
import cfg
from datetime import datetime
import telebot
from arg import *

bot = telebot.TeleBot(cfg.TOKEN)


def wC(arg):
    return arg + count

def hours():
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    if hour < 9:
        return 0
    elif hour == 9 or (hour == 10 and minute <= 20):
        return 1
    elif (hour == 10 and minute >= 30) or (hour == 11 and minute <= 50):
        return 2
    elif (hour == 12 and minute >= 30) or (hour == 13 and minute <= 50):
        return 3
    elif hour == 14 or (hour == 15 and minute <= 20):
        return 4
    elif (hour == 15 and minute >= 30) or (hour == 16 and minute <= 50):
        return 5
    else:
        return -1

def weekNow(change=0):

    week = (int(now.strftime("%V"))+change)%2
    #Учебный год начинаться с четной недели (не совпадает)
    if week == 1:
        return schedule[1]
    elif week == 0:
        return schedule[0]

def numberOfPara(arg):
    return (weekNow().get(now.weekday())).get(arg)

def paraTodayByArg(key=1):

    para = numberOfPara(key)
    if para != None:
        return "\nУ первой подгруппы: " + para[0]+ "\nУ второй подгруппы: " + para[1]
    else:
        return "\nУ первой и второй подгруппы сейчас нет пар"

def paraByKeyWord(day): 
    if day < now.weekday() and day >= 0:
        anotherWeek = 1
    else:
        day = wC(day)
        anotherWeek = day // 7

    def output(i,day=0):
        return str(i) + " пара: " + "\n" + \
        (weekNow(anotherWeek).get(day%7)).get(i)[0] + "\n" + \
        (weekNow(anotherWeek).get(day%7)).get(i)[1] + "\n"
    out = "\n"
    for i in range(1,6):
        out+=output(i,day)
    return out


@bot.message_handler(commands=['para','пара'])
def start_message(message):
    global now
    now = datetime.now()

    def theDay(value):
        return (now.weekday() + value)%7

    chatId = message.chat.id
    keyW = message.text
    global count
    count = keyW.count('после') - keyW.count('поза')  - keyW.count('перед')  - keyW.count('до')

    keyW = keyW.replace('поза','')
    keyW = keyW.replace('перед', '')
    keyW = keyW.replace('после', '')
    keyW = keyW.replace('до', '')
    keyW = (keyW.strip()).split()
    print (keyW)

    day = paraTodayByArg(hours()) #по умолчанию

    for keyWord in keyW:
        if keyWord in today:
            print("today")
            day = paraByKeyWord(theDay(0))
            break
        elif keyWord in tomorrow:
            print("tomorrow")
            day = paraByKeyWord(theDay(1))
            break
        elif keyWord in yesterday:
            print("yesterday")
            day = paraByKeyWord(theDay(-1))
            break
        elif keyWord in monday:
            print("mon")
            day = paraByKeyWord(0)
            break
        elif keyWord in tuesday:
            print("tuesday")
            day = paraByKeyWord(1)
            break
        elif keyWord in wednesday:
            day = paraByKeyWord(2)
            print("wednesday")
            break
        elif keyWord in thursday:
            day = paraByKeyWord(3)
            print("thursday")
            break
        elif keyWord in friday:
            print("friday")
            day = paraByKeyWord(4)
            break
        elif keyWord in saturday:
            print("saturday")
            day = paraByKeyWord(5)
            break
        elif keyWord in sunday:
            print("sunday")
            day = paraByKeyWord(6)
            break
        elif keyWord in next:
            print("next")
            day = paraTodayByArg(hours()+1)
            break
        elif keyWord in number:
            print("number")
            day = paraTodayByArg(int(keyWord))
            break

    bot.send_message(chatId, str(day))

bot.polling()
