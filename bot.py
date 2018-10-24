from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import telegram
import logging
import json
import re

import utils

# Enable logging.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
                            %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

users_locations = dict()


def get_token():
    with open('token.json') as jsn:
        data = json.load(jsn)
    return data['token']


def start(bot, update):
    update.message.reply_text('Hi!')

    composed_answer = utils.compose_state()
    update.message.reply_text(composed_answer, parse_mode=telegram.ParseMode.MARKDOWN)


def text_handler(bot, update):
    composed_answer = utils.compose_state()
    update.message.reply_text(composed_answer, parse_mode=telegram.ParseMode.MARKDOWN)


def command_handler(bot, update):
    text = update.message.text
    alias = re.sub(r'{}*'.format(utils.SWITCH), '', text)

    # Switch `alias` device.
    utils.switch(alias)

    composed_answer = utils.compose_state()
    update.message.reply_text(composed_answer, parse_mode=telegram.ParseMode.MARKDOWN)


def run():
    token = get_token()

    req = telegram.utils.request.Request(proxy_url='socks5h://127.0.0.1:9050',
                                         read_timeout=30, connect_timeout=20,
                                         con_pool_size=10)
    bot = telegram.Bot(token=token, request=req)
    updater = Updater(bot=bot)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, text_handler))
    dp.add_handler(MessageHandler(Filters.command, command_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run()