from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


api = ''
bot = Bot(token=api)

dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
ikb = InlineKeyboardMarkup()

button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.row(button1)
kb.row(button2)

inlineButton1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inlineButton2 = InlineKeyboardButton(text='Формулы рассчёта', callback_data='formulas')
ikb.row(inlineButton1)
ikb.row(inlineButton2)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')


@dp.message_handler(commands=['start'])
async def start(message):
    print(f'Получена команда: {message.text}')
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    print(f'Получено сообщение: {call.message.text}')
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']) + 5
    await message.answer(f'Норма калорий: {calories}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    print(f'Получено сообщение: {message.text}')
    await message.answer('Введите команду /start чтобы начать общение')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)