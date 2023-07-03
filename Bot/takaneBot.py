import requests,os


import logging


from dotenv import load_dotenv


from aiogram import Bot,Dispatcher,executor,types


from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


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
button2=KeyboardButton('Красотуля😘',callback_data='+')
button3=KeyboardButton('Кринжуля😈',callback_data='-')
RatingKeyboard=ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(button2,button3,button1)



@dp.message_handler(commands=['start'])
async def start(message:types.Message):
  username = message.from_user.username
  user_fullname= message.from_user.full_name
  if user_fullname != 'None':
      await message.answer(f'Hi, {user_fullname}!',reply_markup=ReplyKeyboard)
  else: await message.answer(f'Hi, {username}!',reply_markup=ReplyKeyboard)
  
  

@dp.message_handler()
async def send_kitty(message: types.Message):
    context={'Отправь китю! 😽','Красотуля😘','Кринжуля😈'}
    if message.text in context:
        response = requests.get(API).json()
        kitty = response[0].get('url')
        kitty_id = response[0].get('id')
        
        try:
            if message.text == 'Отправь китю! 😽':
                
                await message.answer('Ван минут...')
                chat_id=message.from_user.id
                await bot.send_photo(chat_id=chat_id,photo=kitty,reply_markup=RatingKeyboard) 
            else: await rating_kitty(message.text,kitty_id)
                
        except: await message.answer('Все кисы разбежались 😓')


async def rating_kitty(rating,id):
    if rating == 'Красотуля😘':
       requests.post(API_POST,{'x-api-key':KEY,'image_id':id,'value':'10'})
    else: requests.post(API_POST,{'x-api-key':KEY,'image_id':id,'value':'-10'})


       


if __name__ == '__main__':
    executor.start_polling(dp)

