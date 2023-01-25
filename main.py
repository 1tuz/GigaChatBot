import openai
import os
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

load_dotenv()
token = os.getenv('TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')

bot = Bot(token)
dp = Dispatcher(bot)
openai.api_key = openai_api_key

user_messages = {}

@dp.message_handler()
async def save_user_message(message: types.Message):
    user_messages[message.from_user.id] = message.text
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
    await message.answer(response['choices'][0]['text'])

@dp.message_handler()
async def follow_up_correction(message: types.Message):
    if message.from_user.id in user_messages:
        previous_message = user_messages[message.from_user.id]
        # use previous_message and message.text to handle follow-up corrections

@dp.message_handler(commands=['/restart'])
async def restart(message: types.Message):
    await message.answer("Bot restarting...")
    executor.stop()
    executor.start_polling(dp, skip_updates=True)

executor.start_polling(dp, skip_updates=True)
