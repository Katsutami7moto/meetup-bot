from functools import wraps

from environs import Env
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext


env = Env()
env.read_env()

LIST_OF_ADMINS = list(map(int, env.list('LIST_OF_ADMINS')))


def get_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    custom_keyboard = [
        ['Программа мероприятия'],
        ['Задать вопрос докладчику'],
    ]
    if is_user_admin(user_id):
        custom_keyboard.append(['Панель администратора'])

    return ReplyKeyboardMarkup(custom_keyboard)


def restricted(func):
    """Запрет доступа к обработчику для не-администраторов"""

    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if not is_user_admin(user_id):
            print(f'Нет прав доступа для user_id {user_id}.')
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='У вас нет прав доступа к данной опции меню!',
                reply_markup=get_main_menu(update.effective_user.id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def is_user_admin(user_id: int) -> bool:
    """Проверка: пользователь является администратором?"""
    if user_id in LIST_OF_ADMINS:
        return True
    return False


@restricted
def open_admin_panel(update: Update, context: CallbackContext):
    """Открыть панель администратора"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Панель администратора',
        reply_markup=get_admin_keyboard())


def get_admin_keyboard():
    """Меню для панели администратора"""
    custom_keyboard = [
        
    ]
    return ReplyKeyboardMarkup(custom_keyboard)
