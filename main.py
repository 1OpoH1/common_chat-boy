from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from data.db_session import *
import logging

logging.basicConfig(level=logging.INFO)
bard, wizard, druid, priest, magician, pathfinder, paladin, witcher, is_count = False, False, False, False, False, False, False, False, False

your_lvl = True
reply_keyboard = [['/classes', '/spells']]
special_for_spells = ReplyKeyboardMarkup([['/close']], one_time_keyboard=True)
reply_markup_classes = [['/bard', '/wizard', '/druid', '/priest'], ['/magician', '/pathfinder', '/paladin', '/witcher'],
                        ['/close']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup_classes = ReplyKeyboardMarkup(reply_markup_classes, one_time_keyboard=False)
TOKEN = '1712547917:AAENBafzhZVC8onZ6qD6GnuDr6TJakuJa1g'


def start(update, context):
    update.message.reply_text('Данный бот отправляет данные по заклинаниям классов игры DnD', reply_markup=markup)


def classes(update, context):
    update.message.reply_text('Вы можете узнать заклинания которые может узнать ваш класс, выберите класс',
                              reply_markup=markup_classes)


def choose_lvl(clas):
    global your_lvl, bard, wizard, druid, priest, magician, pathfinder, paladin, witcher
    classes = [bard, wizard, druid, priest, magician, pathfinder, paladin, witcher]
    classes[clas] = True
    your_lvl = True


def bard(update, context):
    choose_lvl(0)
    update.message.reply_text('Введите ваш уровень')


def wizard(update, context):
    choose_lvl(1)
    update.message.reply_text('Введите ваш уровень')


def druid(update, context):
    choose_lvl(2)
    update.message.reply_text('Введите ваш уровень')


def priest(update, context):
    choose_lvl(3)
    update.message.reply_text('Введите ваш уровень')


def magician(update, context):
    choose_lvl(4)
    update.message.reply_text('Введите ваш уровень')


def pathfinder(update, context):
    choose_lvl(5)
    update.message.reply_text('Введите ваш уровень')


def paladin(update, context):
    choose_lvl(6)
    update.message.reply_text('Введите ваш уровень')


def witcher(update, context):
    choose_lvl(7)
    update.message.reply_text('Введите ваш уровень')


def say_spell(update, context):
    global is_count, your_lvl
    exitt = ['Выйти', 'выйти', 'close', 'Close']
    if update.message.text in exitt and is_count:
        close(update, context)
        return
    if is_count:
        db_sess = create_session()

        update.message.reply_text('Hi')
    if your_lvl:
        update.message.reply_text('Hoi')
    your_lvl = False


def spells(update, context):
    global is_count
    is_count = True
    update.message.reply_text('Вы можете ввести название заклинания и получить информацию по нему',
                              reply_markup=special_for_spells)


def close(update, context):
    global is_count, your_lvl
    is_count, your_lvl = False, False
    update.message.reply_text('Вы вернулись назад', reply_markup=markup)


def main():
    global is_count
    global_init('db/spells.db')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    logging.info('Start server')
    updater.start_polling()
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('classes', classes))
    dp.add_handler(CommandHandler('close', close))
    dp.add_handler(CommandHandler('spells', spells))
    dp.add_handler(CommandHandler('bard', bard))
    dp.add_handler(CommandHandler('wizard', wizard))
    dp.add_handler(CommandHandler('druid', druid))
    dp.add_handler(CommandHandler('priest', priest))
    dp.add_handler(CommandHandler('magician', magician))
    dp.add_handler(CommandHandler('pathfinder', pathfinder))
    dp.add_handler(CommandHandler('paladin', paladin))
    dp.add_handler(CommandHandler('witcher', witcher))
    dp.add_handler(MessageHandler(Filters.text, say_spell))
    updater.idle()
    logging.info('Finish server')


if __name__ == '__main__':
    main()
