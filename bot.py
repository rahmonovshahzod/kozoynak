import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile, ContentType
from tts import tts_full
from PIL import Image
import pytesseract
import requests
from stt import transcribe
from pydub import AudioSegment
import aiohttp
import aiofiles

def image_to_text(image_path):
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)
    return text

API_TOKEN = '7387367782:AAHRb3eg_Ej0IjaY_1DZJpNmOc-DWSNsY1g'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Define the path where images will be saved
image_path = 'images/uploaded.jpg'  # Make sure this directory exists

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when the user sends `/start` or `/help` command
    """
    await message.reply("Assalomu alaykum kitob marhamat rasmini yuboring")

@dp.message_handler(content_types=ContentType.VOICE)
async def handle_voice(message: types.Message):
    voice = message.voice
    file_info = await bot.get_file(voice.file_id)
    file_path = file_info.file_path

    # Download the voice file
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(f'https://api.telegram.org/file/bot{API_TOKEN}/{file_path}') as response:
            if response.status == 200:
                f = await aiofiles.open('input.ogg', mode='wb')
                await f.write(await response.read())
                await f.close()
                convert_ogg_to_wav('input.ogg', 'input.wav')
                text = transcribe("input.wav")
                await message.reply(text)

def convert_ogg_to_wav(input_file, output_file):
    audio = AudioSegment.from_ogg(input_file)
    audio.export(output_file, format='wav')

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.reply(".....ishlanmoqda....")

    photo = message.photo[-1]
    file_id = photo.file_id

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    downloaded_file = await bot.download_file(file_path)

    image_save_path = os.path.join(image_path)
    with open(image_save_path, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    text = image_to_text(image_path).replace("x","h").replace("X","H")
    tts_full(text)
    wav_file_path = 'result_211.wav'

    wav_file = InputFile(wav_file_path)
    await message.reply_audio(audio=wav_file)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)