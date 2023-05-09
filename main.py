import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


BOT_TOKEN = 'Твой токен'

bot = Bot(token=BOT_TOKEN,parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp=Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

class newNabor(StatesGroup):
    naborName = State()
    oneSticker = State()


class FsmToAdmin(StatesGroup):
    messageToAdmin = State()

adminid = 6271073561

@dp.message_handler(commands=['start'])
async def process_start_command(message:types.Message):
    await message.reply("Привет👋\nЯ бот, в котором ты можешь бесплатно выбрать стикерпак на любой вкус 👀")


@dp.message_handler(commands=['help'])
async def helpMessage(message: types.Message):
    await message.answer('Что-нибудь накалякаешь', reply_markup=kb1)


@dp.callback_query_handler(text='drugoe')
async def get_menu0(call: types.CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.edit_text(text='Если обнаружили какой-то баг или есть предложение(реклама тоже) то пишите ниже👇', reply_markup=helpkb)


@dp.callback_query_handler(text='reklama', state=None)
async def kateg(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Пожалуйста, отправьте ваше предложение боту ОДНИМ СООБЩЕНИЕМ, в случае согласия разработчика, он свяжется с вами так же, через бота. Для удобства можете указать свой Телеграм. Отправьте сообщение:')
    await FsmToAdmin.messageToAdmin.set()

@dp.callback_query_handler(text='dobavit nabor', state=None)
async def newnabor(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id,'Напишите категорию данного стикерпака(Даже если ее нет):')
    await newNabor.naborName.set()


@dp.message_handler(content_types=['text'], state=newNabor.naborName)
async def loadNabor(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Теперь отправьте сам стикер')
    await newNabor.next()


@dp.message_handler(content_types=['sticker'], state=newNabor.oneSticker)
async def loadSticker(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(5722409799, text=data['name'])
    await bot.send_sticker(5722409799, sticker=message.sticker.file_id)
    await state.finish()
@dp.message_handler(content_types=['photo', 'video', 'file', 'text', 'mediagroup'], state=FsmToAdmin.messageToAdmin)
async def zxc(message: types.Message, state: FSMContext):
    await bot.forward_message(message.chat.id, 5722409799, message.message_id)
    await state.finish()





kb1 = InlineKeyboardMarkup()
    
kb1.add(InlineKeyboardButton('📲Стикеры по категориям', callback_data='ctikeri po kategoriyam'))

kb1.add(InlineKeyboardButton('⚙Другое', callback_data='drugoe'))

helpkb = InlineKeyboardMarkup()

helpkb.add(InlineKeyboardButton(callback_data='reklama', text='Реклама|предложения')).add(InlineKeyboardButton("Добавить свой набор", callback_data='dobavit nabor'))


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)