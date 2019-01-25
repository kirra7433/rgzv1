#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bot_private_constants
import timetable

import telebot

import json
import time
import random
import os.path
import re

bot = telebot.TeleBot(bot_private_constants.token)

S = json.load(open("strings.json"))

commands_with_description = [
	"/group_list — Список группы",
	"/today — Расписание на сегодня",
	"/tomorrow — Расписание на завтра",
    "/timetable — Расписание на неделю",
    "/now — А что сейчас?"
]


@bot.message_handler(commands = ['group_list'])
def group_list(message):
	group_list_string = ""
	for index, person in enumerate(bot_private_constants.group_list, start = 1):
		group_list_string += str(index) + ". " + person + "\n"
	bot.send_message(message.chat.id, group_list_string)

@bot.message_handler(commands = ['help', 'start'])
def introduction(message):
	intro_message = "Я бот-помощник. Умею отвечать на команды:\n\n"
	for command in commands_with_description:
		intro_message += command + "\n"
	bot.send_message(message.chat.id, intro_message, True)

@bot.message_handler(commands = ['today'])
def today(message):
    timetable_string = "\n".join(
        map(timetable.make_long_subject,
            timetable.get_today_subjects()))
    bot.send_message(message.chat.id, timetable_string)

@bot.message_handler(commands = ['tomorrow'])
def tomorrow(message):
    timetable_string = "\n".join(
        map(timetable.make_long_subject,
            timetable.get_tomorrow_subjects()))
    bot.send_message(message.chat.id, timetable_string)

@bot.message_handler(commands = ['timetable'])
def show_timetable(message):
    timetable_string = ""
    for day, dayname in enumerate(S['weekdays'][:-1]):
        timetable_string += "{}\n{}\n\n".format(
                dayname,
                "\n".join(
                    map(timetable.make_long_subject,
                        timetable.get_subjects(day))))
    bot.send_message(message.chat.id, timetable_string)

@bot.message_handler(commands = ['now'])
def tomorrow(message):
    subject, tm = timetable.get_next_subject()
    if subject == None:
        if tm == 0:
            fmt = S["no_subject"]
        else:
            fmt = S["weekend"]
    else:
        subject = timetable.make_inline_subject(subject)
        if tm > 0:
            fmt = S["next_subject"]
        else:
            fmt = S["current_subject"]
    interval = timetable.make_human_time("{:02}:{:02}".format(
        abs(int(tm)) // 3600, abs(int(tm)) // 60 % 60))
    message_string = fmt.format(subject=subject, interval=interval)
    bot.send_message(message.chat.id, message_string)



bot.polling(none_stop=True)
while True:
    time.sleep(100)
