#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import argparse
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from constants import BOTTOKEN
from messages import NEWCOMMENT, NEWTHREAD
bot = telegram.Bot(BOTTOKEN)

def load_chats():
    with open('channels.json', 'r') as fp:
        return json.load(fp)

def save_channels(chats):
    with open('channels.json', 'w') as fp:
        chats = list(set(chats))
        json.dump(chats, fp)

def start(update, context):
    """Send a message when the command /start is issued."""
    chats = load_chats()
    chats.append( str( update.message.chat_id ) )
    save_channels(chats)
    update.message.reply_text('Thank you for subsciring to Kertoja!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Risto Reipaaas!')

def users(update, context):
    """List."""
    chats = load_chats()
    names = []
    if (update['message']['chat']['id'] == -323913787):
        for c in chats:
            try:
                names.append('@' + (bot.get_chat_member(c, c).user.username) + ' -> ' + str(c))
            except:
                pass
    bot.send_message(-323913787, '\n'.join(names), parse_mode="Markdown" )

def post(update, context):
    chats = load_chats()
    save = False
    nchats = []
    #print(context.chat_data)
    #print(update)
    #print(update['message']['chat'])
    print()
    text = update['message']['text'][5:]
    print(text)
    if (update['message']['chat']['id'] == -323913787):
        for c in chats:
            try:
                bot.send_message(c, text, parse_mode="Markdown" )
                nchats.append(c)
            except:
                save = True
        if save:
            save_channels(chats)

def reward(update, context):
    """rew."""
    print("ye")
    if (update['message']['chat']['id'] == -323913787):
        text = update['message']['text'][8:]
        i = bot.get_chat(text).id
        #CAADAQADAgADf3BGHAXMZNg3IivIFgQ
        bot.send_sticker(i, 'CAADAQADAgADf3BGHAXMZNg3IivIFgQ')
        #bot.send_message(i, 'You have been given 20 social credits!', parse_mode="Markdown" )
    print("done")

def punish(update, context):
    """pun."""
    if (update['message']['chat']['id'] == -323913787):
        text = update['message']['text'][8:]
        i = bot.get_chat(text).id
        bot.send_sticker(i, 'CAADAQADAwADf3BGHENZiEtY50bNFgQ')
        #bot.send_message(i, '20 social credits have been removed!', parse_mode="Markdown" )

def other(update, context):
    """other."""
    if (update['message']['chat']['id'] != -323913787):
        if(update['message']['sticker']):
            bot.send_message(-323913787, 'Sticker from @' +update['message']['chat']['username'] , parse_mode="Markdown" )
        bot.forward_message(-323913787, update['message']['chat']['id'], update['message']['message_id'])
        #bot.send_message(i, '20 social credits have been removed!', parse_mode="Markdown" )


def tg_bot():
    print("starting bot")
    """Start the bot."""
    updater = Updater(BOTTOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("post", post))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", users))
    dp.add_handler(CommandHandler("reward", reward))
    dp.add_handler(CommandHandler("punish", punish))
    dp.add_handler(MessageHandler(Filters.all, other))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    tg_bot()

