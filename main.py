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

@dp.message_handler() 
async def send(message : types.Message): 
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
    # Send the AI's response as a reply
    await message.reply(response['choices'][0]['text'])

executor.start_polling(dp, skip_updates=True)
