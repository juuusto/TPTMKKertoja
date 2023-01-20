#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import argparse
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from constants import BOTTOKEN, HOST_GROUP
from messages import NEWCOMMENT, NEWTHREAD

bot = telegram.Bot(BOTTOKEN)


def load_chats():
    with open("channels.json", "r") as fp:
        return json.load(fp)


def save_channels(chats):
    with open("channels.json", "w") as fp:
        chats = list(set(chats))
        json.dump(chats, fp)


def start(update, context):
    """Send a message when the command /start is issued."""
    chats = load_chats()
    chats.append(str(update.message.chat_id))
    save_channels(chats)
    update.message.reply_text("A wizard is never late, nor is he early, he arrives precisely when he means to.")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("GANDAAALF!")


def users(update, context):
    """List."""
    chats = load_chats()
    names = []
    if update["message"]["chat"]["id"] == HOST_GROUP:
        for c in chats:
            try:
                names.append(
                    "@" + (bot.get_chat_member(c, c).user.username) + " -> " + str(c)
                )
            except:
                pass
    bot.send_message(-323913787, "\n".join(names), parse_mode="HTML")


def post(update, context):
    chats = load_chats()
    save = False
    nchats = []
    text = update["message"]["text"][5:]
    if update["message"]["chat"]["id"] == HOST_GROUP:
        for c in chats:
            try:
                bot.send_message(c, text, parse_mode="HTML")
                nchats.append(c)
            except:
                save = True
        if save:
            save_channels(chats)


def tell(update, context):
    """tell."""
    if update["message"]["chat"]["id"] == HOST_GROUP:
        text = " ".join(update["message"]["text"].split(" ")[2:])
        i = update["message"]["text"].split(" ")[1]
        bot.send_message(i, text, parse_mode="HTML")


def other(update, context):
    """other."""
    if update["message"]["chat"]["id"] != HOST_GROUP:
        if update["message"]["sticker"]:
            bot.send_message(
                HOST_GROUP,
                "Sticker from @" + update["message"]["chat"]["username"],
                parse_mode="HTML",
            )
        bot.forward_message(
            HOST_GROUP, update["message"]["chat"]["id"], update["message"]["message_id"]
        )


def tg_bot():
    print("starting bot")
    """Start the bot."""
    updater = Updater(BOTTOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", users))
    dp.add_handler(CommandHandler("post", post))
    dp.add_handler(CommandHandler("tell", tell))
    #dp.add_handler(CommandHandler("reward", reward))
    #dp.add_handler(CommandHandler("punish", punish))
    dp.add_handler(MessageHandler(Filters.all, other))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    tg_bot()
