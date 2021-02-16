from schedule import schedule
import cfg
from datetime import datetime
import telebot
from arg import * 
from dateutil.tz import tzoffset

timezone = 2
bot = telebot.TeleBot(cfg.TOKEN)


def day_change(arg):
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


def week_now(change=0):
    week = (int(now.strftime("%V")) + change) % 2
    # Учебный год начинаться с четной недели (не совпадает)
    if week == 1:
        return schedule[1]
    elif week == 0:
        return schedule[0]


def number_of_para(arg):
    return (week_now().get(now.weekday())).get(arg)


def para_today_by_arg(key=1):
    para = number_of_para(key)
    if para is not None:
        return "\nУ первой подгруппы: " + para[0] + "\nУ второй подгруппы: " + para[1]
    else:
        return "\nУ первой и второй подгруппы сейчас нет пар"


def para_by_key_word(day):
    if now.weekday() > day and day >= 0:
        another_week = 1
        day = day_change(day)
    else:
        day = day_change(day)
        another_week = day // 7

    def output(i, day = 0):
        return str(i) + " пара: " + "\n" + \
               (week_now(another_week).get(day % 7)).get(i)[0] + "\n" + \
               (week_now(another_week).get(day % 7)).get(i)[1] + "\n"

    out = "\n"
    for i in range(1, 6):
        out += output(i, day)
    return out


chatId = None

@bot.message_handler(commands=['help','start', 'para'])
def first(message):
    first_buttons = telebot.types.ReplyKeyboardMarkup(True, True)
    first_buttons.row('Какая сейчас пара?', 'Какая следующая пара')
    first_buttons.row('Какие пары сегодня?', 'Какие пары завтра?')
    bot.send_message(message.chat.id, 'Что Вы хотите узнать?', reply_markup=first_buttons)


def listener(message):
    global now

    offset = tzoffset(None, timezone * 3600)  # offset in seconds
    now = datetime.now(offset)

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

    for i in para_input:
        for j in split_msg:
            if i == j:
                msg_txt = msg_txt.replace(i, '')

                count = msg_txt.count('после') - msg_txt.count('поза') - msg_txt.count('перед') - msg_txt.count('до')

                msg_txt = (msg_txt.strip())
                msg_txt += " "
                print(msg_txt)

                def check():
                    a = (right_now, today, tomorrow, yesterday, monday, tuesday, wednesday, thursday, friday, saturday, sunday, next, number)
                    for i in a:
                        for x in i:
                            if x in msg_txt:
                                print(i)
                                argument = 0
                                if i == right_now:
                                    argument = hours()
                                elif i == today:
                                    argument == the_day(0)
                                elif i == tomorrow:
                                    argument = the_day(1)
                                elif i == yesterday:
                                    argument = the_day(-1)
                                elif i == monday:
                                    argument = 0
                                elif i == tuesday:
                                    argument = 1
                                elif i == wednesday:
                                    argument = 2
                                elif i == thursday:
                                    argument = 3
                                elif i == friday:
                                    argument = 4
                                elif i == saturday:
                                    argument = 5
                                elif i == sunday:
                                    argument = 6
                                elif i == next:
                                    argument = hours() + 1
                                elif i == number:
                                    argument = int(x)
                                day = para_today_by_arg(argument)
                                return day
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