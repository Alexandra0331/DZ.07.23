from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
import emoji

from random import randint
from config import TOKEN
import processor as p


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Глобальные переменные - список игрового поля, словарь имен игроков, флаги
gamefield, cia, bot_first  = [' '] * 9, True, False
players = {True: 'Крестики', False: 'Нолики'}
pvb_flag, smart_flag = False, False
end_of_game = False

def get_keys(win_flag=False):
    # Генератор клавиатуры - на основе глобальной переменной со списком игрового поля
    global gamefield
    buttons = []
    for i in range(len(gamefield)):
        buttons.append(types.InlineKeyboardButton(
            text=gamefield[i], callback_data=i+1))
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    if win_flag:
        keyboard.add(types.InlineKeyboardButton(
            text='Еще раз...', callback_data='reset'))
    return keyboard


@dp.message_handler(commands=["help", "hello", "pvp_game", "game"])
async def cmd_numbers(message: types.Message):
    global gamefield, players, pvb_flag, cia
    match message.text[1:]:
        case 'help':
            await message.reply(f'Привет, {message.from_user.first_name}!\n/hello - приветствие\n'+
                                                                           '/help - список команд\n'+
                                                                           '/pvp_game - игрок против игрока\n'+
                                                                           '/game - игрок против бота\n', reply=False)
        case 'hello':
            await message.reply(f'Привет, {message.from_user.first_name}! \nНачинаем игру? Если будешь игрть с соперником жми /pvp_game или  поиграй со мной /game' + emoji.emojize(':winking_face:', language='alias'), reply=False)
        case 'pvp_game':
            pvb_flag = False
            await new_game(message)
        case 'game':
            pvb_flag, smart_flag = True, False
            await new_game(message)
@dp.message_handler()
async def cmd_numbers(message: types.Message):
    await message.reply(f'{message.from_user.first_name}, я тебя не понимаю'+ emoji.emojize(':face_with_rolling_eyes:', language='alias')+ 'но могу помочь, жми /help'+ emoji.emojize(':winking_face:', language='alias'), reply=False)

async def update_fld(message: types.Message, new_value: int):
    global players, cia, end_of_game, bot_first
    if pvb_flag and not smart_flag:
        gamemode = '(Игра с  ботом)'
    else: gamemode = ''

    if p.check_4_win(gamefield):
        win_str = 10*'\U0001f3c6'+'\n'+  f'{players[not cia].upper()} ПОБЕДИЛИ!!!!'+'\n' + 10*'\U00002728'
        p.write_log(p.t(), f'{gamemode} - {players[not cia]} победили!!!')
        await message.edit_text(f"{win_str}", reply_markup=get_keys(True))
        end_of_game = True
    elif not p.isfull(gamefield):
        await message.edit_text(f"{new_value}", reply_markup=get_keys())
        end_of_game = False
    else:
        win_str = f'НИЧЬЯ!'
        p.write_log(p.t(), f'Ничья{gamemode}!')
        await message.edit_text(f"{win_str}", reply_markup=get_keys(True))
        end_of_game = True

async def new_game(message: types.Message):
    global gamefield, cia, pvb_flag, bot_first
    gamefield, cia, stup_flag = [' '] * 9, True, False
    match pvb_flag:
        case True:
            # случайный выбор первого игрока - бот или игрок
            bot_first = bool(randint(0, 1))
            s = 'бот' if bot_first else 'игрок'
            out_str = f'\nза {players[True]} играет {s}.\n'
            if bot_first:
                gamefield, cia = p.bot_turn(gamefield, cia, smart_flag)
        case False:
            out_str = ''
    try:
        await message.edit_text(out_str + f"Ходят {players[cia].lower()}:", reply_markup=get_keys())
    except exceptions.MessageCantBeEdited:
        await message.answer(out_str + f"Ходят {players[cia].lower()}:", reply_markup=get_keys())


@dp.callback_query_handler()
async def callbacks_num(call: types.CallbackQuery):
    global cia, gamefield, players, end_of_game, pvb_flag
    action = call.data
    # обработка нажатия кнопок
    if action.isdecimal():
        gamefield[int(action)-1] = '\U0000274C' if cia else '\U00002B55'
        cia = not cia
        out_val = f'Ходят {players[cia].lower()}:'
        await update_fld(call.message, out_val)
    else:
        if action == 'reset':
            end_of_game = False
            await new_game(call.message)
            return
        else:
            await call.answer()
            return

    if not end_of_game:  # остановка при первом победителе
        if pvb_flag:
            gamefield, cia = p.bot_turn(gamefield, cia, smart_flag)
            out_val = f'Ходят {players[cia].lower()}:'
            await update_fld(call.message, out_val)

    # отчет о получении колбэка
    await call.answer()


if __name__ == '__main__':
    try:
        p.write_log(p.t(), 'Старт')
        executor.start_polling(dp)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        p.write_log(p.t(), 'Завершение')