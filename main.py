from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from data.db_session import *
from data.spells import Spells
from data.classes import Classes
from data.players import Players
from api_folder import all_for_api
from requests import get, post, delete
import logging

logging.basicConfig(
    filename='example.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
classes, is_count = False, False

global_init('db/spells.db')
your_lvl = False
reply_keyboard = [['/classes', '/spells', '/create_hero'], ['/All_heroes']]
special_for_spells = ReplyKeyboardMarkup([['/close']], one_time_keyboard=True)
reply_markup_classes = [['/bard', '/wizard', '/druid', '/priest'], ['/magician', '/pathfinder', '/paladin', '/witcher'],
                        ['/close']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup_classes = ReplyKeyboardMarkup(reply_markup_classes, one_time_keyboard=False)
ac = [['Бард', 'Чародей', 'Волшебник'], ['Варвар', 'Друид', 'Воин'], ['Жрец', 'Монах', 'Колдун'], ['Плут', 'Паладин', 'Следопыт'], ['/close']]
all_classes = ReplyKeyboardMarkup(ac, one_time_keyboard=True)
TOKEN = '1712547917:AAENBafzhZVC8onZ6qD6GnuDr6TJakuJa1g'


def start(update, context):
    update.message.reply_text('Данный бот отправляет данные по заклинаниям классов игры DnD', reply_markup=markup)


def classes(update, context):
    update.message.reply_text('Вы можете узнать заклинания которые может узнать ваш класс, выберите класс',
                              reply_markup=markup_classes)


def choose_lvl(clas):
    global your_lvl, classes, is_count
    is_count = False
    if clas == 0:
        classes = 'Бард'
    elif clas == 1:
        classes = 'Волшебник'
    elif clas == 2:
        classes = 'Друид'
    elif clas == 3:
        classes = 'Жрец'
    elif clas == 4:
        classes = 'Чародей'
    elif clas == 5:
        classes = 'Следопыт'
    elif clas == 6:
        classes = 'Паладин'
    elif clas == 7:
        classes = 'Колдун'
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

def show_all_heroes(update, context):
    heroes = get('http://127.0.0.1:5000/api/player').json()
    for hero in heroes['players']:
        update.message.reply_text('Имя: ' + hero['name'] + '\nКласс: ' + hero['y_class'])


def starter(update, context):
    update.message.reply_text('Вы решили создать класс, выберите класс', reply_markup=all_classes)


def say_spell(update, context):
    global is_count, your_lvl
    exitt = ['Выйти', 'выйти', 'close', 'Close']
    if update.message.text in exitt and (is_count or your_lvl):
        close(update, context)
        return
    if is_count:
        db_sess = create_session()
        logging.info('Произошел запрос:' + update.message.text.upper())
        try:
            spells = db_sess.query(Spells).filter(Spells.name.like(f'%{update.message.text.upper()}%')).all()
            if spells:
                for spell in spells:
                    logging.info('По запросу найден ' + spell.name)
                    update.message.reply_text(
                        spell.name + '\n' + 'Уровень:' + str(spell.level) + '\n' + 'Компоненты' + spell.components + '\n' + spell.description)
            else:
                logging.info('Не найден запрос')
                update.message.reply_text('Вы ввели неверное название заклинания, попробуйте еще раз')
        except Exception as e:
            logging.error(e)
            update.message.reply_text('Ошибка сервера')

    elif your_lvl:
        lvl = update.message.text
        db_sess = create_session()
        spells = db_sess.query(Classes).filter(Classes.name == classes).all()
        if spells:
            text = ''
            for spell in spells:
                logging.info('Получен запрос на получение заклинаний')
                spell_list = [i.upper() for i in spells[0].spells_list.split('\n')]
                new_spells = db_sess.query(Spells).filter(Spells.name.in_(spell_list), Spells.level <= lvl).all()
                for n_spell in new_spells:
                    text += n_spell.name + '\n'
                update.message.reply_text('Доступные вам заклинания:\n' + text)
                is_count = True
        else:
            logging.error('Остутствие класса' + classes)
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

def first_response(update, context):
    if update.message.text not in classs:
        update.message.reply_text('Вы выбрали неверный класс, начните сначала')
        close()
    else:
        global klass
        klass = update.message.text
        update.message.reply_text('Выберите расу', reply_markup=all_races)

def main():
    global is_count
    from api_folder.all_for_api import app, api
    api.add_resource(all_for_api.ClassListResource, '/api/player')
    api.add_resource(all_for_api.ClassResource, '/api/player/<int:class_id>')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    logging.info('Start server')
    updater.start_polling()
    dp.add_handler(CommandHandler('All_heroes', show_all_heroes))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_hero', starter)],

        states={
            1: [MessageHandler(Filters.text, first_response)],
            2: [MessageHandler(Filters.text, second_response)]
        },
        fallbacks=[CommandHandler('close', close)]
    )
    dp.add_handler(conv_handler)
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
    app.run()
    updater.idle()
    logging.info('Finish server')


if __name__ == '__main__':
    main()
