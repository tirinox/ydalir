import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.helper import Helper, HelperMode, Item

from config import settings
from crypto.btc import make_keys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot')

bot = Bot(token=settings.telegram.token)
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware(logger))


class SwapStates(Helper):
    mode = HelperMode.snake_case

    START = Item()
    ASK_SOURCE = Item()
    ASK_DEST = Item()
    CONFIRM = Item()
    FINISHED = Item()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Ydalir bot!\nI swap coins. Powered by THORChain!")


@dp.message_handler()
async def echo(message: types.Message):
    qr_code_img, key = make_keys()
    await message.answer_photo(qr_code_img, f'deposit here: {key.address}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
