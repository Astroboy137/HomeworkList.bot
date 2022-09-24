from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import sqlite3 as sq
import time

async def on_startup(_):
    print("бот работает")
    sql_start()
storage=MemoryStorage


class FSMAdmin(StatesGroup):
    subject = State()
    day = State()
    homework = State()

timer=time.localtime(time.time())
day1=timer.tm_mday
button_load = types.KeyboardButton("/загрузить")
button_del = types.KeyboardButton("/удалить")
button_case_admin = types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_del)
ID=None
bot = Bot("5552710032:AAHkB124DT6b8lyUK8cc1TZiXDxanrBed2A")
dp = Dispatcher(bot=bot,storage=MemoryStorage())
###

###-----------------Admin-----------------###
@dp.message_handler(commands="хуй")
async def start(message:types.Message):
    await message.reply('нахуй иди,матерится плохо')

@dp.message_handler(commands=["moderator"],is_chat_admin=True)
async def changes_command(message:types.Message):
    global ID
    ID = message.from_user.id
    await message.delete()
    await bot.send_message(message.from_user.id,"я в вашем подчинении",reply_markup=button_case_admin)
@dp.message_handler(commands="Загрузить",state=None)
async def start(message:types.Message):
    if message.from_user.id==ID:
        await FSMAdmin.subject.set()
        await message.reply("Введи название предмета")

@dp.message_handler(state=FSMAdmin.subject)
async def load_subject(message:types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["subject"] = message.text
        await FSMAdmin.next()
        await message.reply("Введи дату на которое задали домашее задание по этому предмету")

@dp.message_handler(state=FSMAdmin.day)
async def load_day(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["day"] = message.text
        await FSMAdmin.next()
        await message.reply("Введи что задали")


@dp.message_handler(state=FSMAdmin.homework)
async def load_homework(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["homework"] = message.text
        await sql_add_command(state)
        await message.answer("готово")
        await state.finish()

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query:types.CallbackQuery):
    read= await sql_read2()
    await sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ","")} удалена.',show_alert=True)

@dp.message_handler(commands="удалить")
async def delete_item(message:types.Message):
    if message.from_user.id == ID:
        read = await sql_read2()
        for ret in read:
             await bot.send_message(message.from_user.id,f'Урок:{ret[0]}\n Дата:{ret[1]}\n Задание:{ret[2]}')
             await bot.send_message(message.from_user.id,text="^^^",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f"Удалить {ret[0]}",callback_data=f'del {ret[0]}')))




@dp.message_handler(commands="порно")
async def porn(message:types.Message):
    await message.answer(text="для секаса нажми на кнопку ниже",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="секс тут",url="https://clck.ru/3vyXS")))





###---------------------------CLIENT---------------------------###

@dp.message_handler(commands="rasp")
async def rasp(message:types.Message):
    await sql_delete_command_date()
    await sql_read(message)


###--------------------------DB----------------------------###


def sql_start():
    global base,cur
    base=sq.connect("datab.db")
    cur = base.cursor()
    if base:
        print("database connected")
    base.execute('CREATE TABLE IF NOT EXISTS hw(subject TEXT,day TEXT, homework TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO hw VALUES (?,?,?)', tuple(data.values()))
        base.commit()
async def sql_read(message):
    for ret in cur.execute("SELECT * FROM hw").fetchall():
        await message.answer(f'Урок:,{ret[0]}\nДата: {ret[1]}\nЗадание: {ret[2]}')
async def sql_read2():
    return cur.execute("SELECT * FROM hw").fetchall()
async def sql_delete_command(data):
    cur.execute('DELETE FROM hw WHERE subject==?', (data,))
    base.commit()
async def sql_delete_command_date():
    cur.execute(f'DELETE FROM hw WHERE day={day1}')
    base.commit()
'''
Мой первый проект на гитхабе)
Сейчас 24 сент. 2022 года
Мне скоро исполнится 16 лет)
Самый разгар пандемии и суета на украине
'''



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)