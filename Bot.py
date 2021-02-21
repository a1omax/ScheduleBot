from schedule import schedule
import cfg
from datetime import datetime
import telebot
from arg import *
from dateutil.tz import tzoffset

timezone = 2
offset = tzoffset(None, timezone * 3600)  # offset in seconds


def time_update():
    global now,hour,minute
    now = datetime.now(offset)
    hour =  int(now.strftime("%H"))
    minute =  int(now.strftime("%M"))


bot = telebot.TeleBot(cfg.TOKEN)


def day_change(arg):
    return arg + count


def hours_para():
    
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
    elif (hour == 16 and minute > 50) or (hour >=17):
        return 6


def hours_break():
    if hour == 10 and (30 > minute > 20):
        return 1
    elif (hour == 11 and minute > 50) or (hour == 12 and minute <30):
        return 2
    elif hour == 13 and minute > 50:
        return 3
    elif hour == 15 and (30 > minute > 20):
        return 4


def week_now(change=0):
    week = (int(now.strftime("%V")) + change) % 2
    # Учебный год начинаться с четной недели (не совпадает)
    if week == 1:
        return schedule[1]
    elif week == 0:
        return schedule[0]


def number_of_para(arg):
    return (week_now().get(now.weekday())).get(arg)


def para_today_by_arg(key=0):
    para_numb = hours_para()
    if para_numb is not None:
        numb = key + para_numb
    else:
        break_numb = hours_break()
        if key == 0:
            return "Сейчас перемена после пары №" + str(break_numb)
        elif key > 0:
            numb = break_numb + key
        else:
            numb = break_numb + key + 1
    if numb <= 0:
        return "Пары ещё не начались"
    elif numb <= 5:
        para = number_of_para(numb)
        if para is not None:
            return "\nПара №" + str(numb) + "\nУ первой подгруппы: " + para[0] + "\nУ второй подгруппы: " + para[1]
        else:
            return "\nУ первой и второй подгруппы сейчас нет пар"
    elif numb >= 6:
        return "Пары уже закончились"


def para_today_by_number(numb):
    para = number_of_para(numb)
    return "\nПара №" + str(numb) + "\nУ первой подгруппы: " + para[0] + "\nУ второй подгруппы: " + para[1]


def para_by_key_word(day):
    if now.weekday() > day >= 0:
        another_week = 1
        day = day_change(day)
    else:
        day = day_change(day)
        another_week = day // 7

    def output(numb, key=0):
        return str(numb) + " пара: " + "\n" + \
               (week_now(another_week).get(key % 7)).get(numb)[0] + "\n" + \
               (week_now(another_week).get(key % 7)).get(numb)[1] + "\n"

    out = "\n"
    for i in range(1, 6):
        out += output(i, day)
    return out


chatId = None


@bot.message_handler(commands=['help', 'start', 'para'])
def first(message):
    first_buttons = telebot.types.ReplyKeyboardMarkup(True, True)
    first_buttons.row('Какая сейчас пара?', 'Какая следующая пара', 'Какая прошлая пара')
    #first_buttons.row('Какие пары сегодня?', 'Какие пары завтра?')
    bot.send_message(message.chat.id, 'Что Вы хотите узнать?', reply_markup=first_buttons)


def listener(message):
    time_update()



    msg_txt = ""
    chat_id = ""

    for m in message:
        chat_id = m.chat.id
        if m.content_type == 'text':
            msg_txt = m.text.lower()

    def the_day(value):
        return (now.weekday() + value) % 7

    msg_txt = msg_txt.replace('?', '')
    msg_txt = msg_txt.replace('!', '')

    split_msg = msg_txt.split()

    global count

    for i in ['пара', 'пары', 'расписание']:
        for j in split_msg:
            if i == j:
                msg_txt = msg_txt.replace(i, '')

                count = msg_txt.count('после') - msg_txt.count('поза') - msg_txt.count('перед') - msg_txt.count('до')

                msg_txt = (msg_txt.strip())
                msg_txt += " "
                print(msg_txt)

                def check():
                    i=-1
                    while i<12:
                        for slovo in arg[i]:
                            if slovo in msg_txt:
                                print(slovo)
                                if i <= 1:
                                    return para_by_key_word(the_day(i))
                                elif i <= 8:
                                    return para_by_key_word(i-2)
                                elif i == 9:
                                    return para_today_by_number(int(slovo))
                                elif i <= 11:
                                    return para_today_by_arg(i-10)
                        i += 1
                    else:
                        return 0

                send = check()

                if send != 0:
                    bot.send_message(chat_id, str(send))
                break


bot.set_update_listener(listener)

try:
    bot.polling(none_stop=True)
except:
    pass
