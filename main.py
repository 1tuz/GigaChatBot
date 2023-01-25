import openai
import os
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

load_dotenv()

token = os.getenv('TOKEN')
openai.api_key = os.getenv('OPENAI_KEY')

bot = Bot(token)
dp = Dispatcher(bot)

# Store the previous context
context = ""

class States:
    Normal = 'normal'
    WaitForCorrection = 'wait_for_correction'

@dp.message_handler(state=States.Normal)
async def send(message: types.Message):
    global context
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text + context,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
    # Send the AI's response
    await message.reply(response['choices'][0]['text'])
    # Send a follow-up message asking the user if they would like to make any corrections
    follow_up_message = "Is there anything you would like to correct in my response?"
    follow_up_keyboard = types.InlineKeyboardMarkup()
    follow_up_keyboard.add(types.InlineKeyboardButton("Yes", callback_data="yes"))
    follow_up_keyboard.add(types.InlineKeyboardButton("No", callback_data="no"))
    await bot.send_message(message.chat.id, follow_up_message, reply_markup=follow_up_keyboard)
    context = response['choices'][0]['text']
