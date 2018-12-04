from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import json
import re
import requests

from home_automation import utils, system

# Enable logging.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
                            %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_token():
    with open(system.TGTOKEN_PATH) as jsn:
        data = json.load(jsn)
    return data['token']


def general(func):
    def wrapper(bot, update):
        func(bot, update)
        composed_answer = utils.compose_state()
        update.message.reply_text(composed_answer, parse_mode=telegram.ParseMode.MARKDOWN)
    return wrapper


@general
def start(bot, update):
    update.message.reply_text('Hi!')


@general
def text_handler(bot, update):
    username = str(update.message.from_user.username)
    print(username)
    pass


@general
def command_handler(bot, update):
    text = update.message.text
    device = re.sub(r'{}*'.format(system.SWITCH), '', text)
    # Switch `device` state.
    requests.get('http://localhost:5000/switch/{}'.format(device))


def url_command(bot, update):
    publicurl = utils.get_publicurl()
    update.message.reply_text(publicurl)


def make_photo(bot, update):
    filename = "/home/pi/photo.jpeg"
    r = requests.get('http://192.168.0.8:5000/get_image')

    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)

    with open(filename, "rb") as f:
        update.message.reply_photo(photo=f)


def run():
    token = get_token()

    req = telegram.utils.request.Request(proxy_url='socks5h://127.0.0.1:9050',
                                         read_timeout=30, connect_timeout=20,
                                         con_pool_size=10)
    bot = telegram.Bot(token=token, request=req)
    updater = Updater(bot=bot)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('url', url_command))
    dp.add_handler(CommandHandler('photo', make_photo))
    dp.add_handler(MessageHandler(Filters.text, text_handler))
    dp.add_handler(MessageHandler(Filters.command, command_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run()
