import requests,os


import logging


from dotenv import load_dotenv


from aiogram import Bot,Dispatcher,executor,types


from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton


logging.debug('отладка')
logging.info('Сообщение отправлено')
logging.warning('Не ок')
logging.error('Кринжанул')
logging.critical('Опаньки,приехали!')

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

load_dotenv()
TOKEN = os.getenv('TOKEN')
API = os.getenv('API')
API_POST = os.getenv('API_POST')
KEY = os.getenv('KEY')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

button1=KeyboardButton('Отправь китю! 😽')
ReplyKeyboard=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(button1)
#requests.post(API_POST), data={'value':'10'}
button2=InlineKeyboardButton('Красотуля😘',callback_data='+')
button3=InlineKeyboardButton('Кринжуля😈',callback_data='-')
InlineKeyboard=InlineKeyboardMarkup(row_width=2).add(button2,button3)



@dp.message_handler(commands=['start'])
async def start(message:types.Message):
  username = message.from_user.username
  user_fullname= message.from_user.full_name
  if user_fullname != 'None':
      await message.answer(f'Hi, {user_fullname}!',reply_markup=ReplyKeyboard)
  else: await message.answer(f'Hi, {username}!',reply_markup=ReplyKeyboard)
  
  

@dp.message_handler()
async def send_kitty(message: types.Message):
    if message.text == 'Отправь китю! 😽':
        await message.answer('Ван минут...')
        try:
            response = requests.get(API).json()
            kitty = response[0].get('url')
            chat_id=message.from_user.id
            await bot.send_photo(chat_id=chat_id,photo=kitty,reply_markup=InlineKeyboard)
        except: await message.answer('Все кисы разбежались 😓')


@dp.callback_query_handler()
async def process_callback(callback:types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    if callback.id=='+':
        requests.post(API_POST, {'x-api-key':f'{API_POST}/api-key={KEY}','value':'1'})
    else: requests.post(API_POST, {'x-api-key':f'{API_POST}/api-key={KEY}','value':'-1'})


if __name__ == '__main__':
    executor.start_polling(dp)

