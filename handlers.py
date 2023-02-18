from aiogram import types
from loader import dp
import random

max_count = 150
total = 0
new_game = False

@dp.message_handler(commands=['start', 'старт'])
async def mes_start(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'{name}, привет! Сегоня сыграем в игру "Конфеты". Для начала игры введи команду /new_game.'
                         f'Для настройки конфет введи команду /set и укажи количество конфет.')

# @dp.message_handler(commands=['help'])
# async def mes_help(message: types.Message):
#     await message.answer('Помоги себе сам')

@dp.message_handler(commands=['new_game'])
async def mes_game(message: types.Message):
    global new_game
    global total
    global max_count
    new_game = True
    total = max_count
    first = random.randint(0, 1)
    if first:
        await message.answer(f'Игра началась. По жребию первым ходит {message.from_user.first_name}! ' 
                             f'Сколько конфет возьмешь?')
    else:
        await message.answer(f'Игра началась. По жребию первым ходит Бот')
        await bot_turn(message)

@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global total
    global new_game
    name = message.from_user.first_name
    count = message.text.split()[1]
    if not new_game:
        if count.isdigit():
            max_count = int(count)
            await message.answer(f'Конфет теперь будет {max_count} ')
        else:
            await message.answer(f'{name}, напиши цифрами!')
    else:
        await message.answer(f'{name}, нельзя менять правила во время игры!')


@dp.message_handler()
async def mes_take_candy(message: types.Message):
    global total
    global new_game
    name = message.from_user.first_name
    count = message.text
    if new_game:
        if message.text.isdigit() and 0< int(message.text) < 29:
            total -= int(message.text)
            if total <= 0:
                await message.answer(f'Ура! {name}, ты победил(а)!')
                new_game = False
            else:
                await message.answer(f'{name} взял(а) {message.text} конфет. '
                                 f'На столе осталось {total}')
                await bot_turn(message)
        else:
            await message.answer(f'{name}, надо указать число от 1 до 28')
        
async def bot_turn(message: types.Message):
    global total
    global new_game
    bot_take = 0
    if 0 < total < 29:
        bot_take = total
        total -= bot_take
        await message.answer(f'Бот взял {bot_take} конфет.'
                              f'На столе осталось {total} и бот одержал победу.')
        new_game = False
    else:
        remainder = total%29
        bot_take = remainder if remainder != 0 else 28
        total -= bot_take
        await message.answer(f'Бот взял {bot_take} конфет. На столе осталось {total}')
        