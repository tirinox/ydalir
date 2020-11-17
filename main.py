import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import *
from aiogram.utils.helper import HelperMode

from config import settings
from crypto.btc import make_keys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot')

bot = Bot(token=settings.telegram.token, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware(logger))


class SwapStates(StatesGroup):
    mode = HelperMode.snake_case

    START = State()
    ASK_SOURCE = State()
    ASK_DEST = State()
    ASK_DEST_ADDRESS = State()
    CONFIRM = State()
    FINISHED = State()


@dp.message_handler(content_types=types.ContentTypes.STICKER, state='*')
async def handle_sticker(message: types.Message, state: FSMContext):
    st = message.sticker
    print(st)
    await message.answer(f"{st.emoji}: {st.file_id}")


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer("Hi!\nI'm Ydalir bot!\nI swap coins cross-chain. Powered by THORChain!\n\n"
                             "What asset would you like to swap?",
                             disable_notification=True,
                             reply_markup=ReplyKeyboardMarkup(keyboard=[
                                 [KeyboardButton('BTC'), KeyboardButton('BNB')],
                                 [KeyboardButton('RUNE')],
                             ], resize_keyboard=True))
        await SwapStates.ASK_SOURCE.set()


@dp.message_handler(state=SwapStates.ASK_SOURCE)
async def on_reply_source_asset(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['source_asset'] = message.text.strip().upper()
        await message.reply('What asset would you like to get?', disable_notification=True,
                            reply_markup=ReplyKeyboardMarkup(keyboard=[
                                [KeyboardButton('RUNE'), KeyboardButton('BNB')],
                            ], resize_keyboard=True))
        await SwapStates.ASK_DEST.set()


@dp.message_handler(state=SwapStates.ASK_DEST)
async def on_reply_dest_asset(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dest_asset'] = message.text.strip().upper()
        await message.reply('Please enter the destination address:', disable_notification=True,
                            reply_markup=ReplyKeyboardRemove())
        await SwapStates.ASK_DEST_ADDRESS.set()


@dp.message_handler(state=SwapStates.ASK_DEST_ADDRESS)
async def on_reply_dest_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dest_address'] = message.text.strip().upper()
        qrcode, keys = make_keys()

        source_asset = data['source_asset']
        await message.answer_photo(qrcode,
                                   f"Ok. Deposit {source_asset} to <b>{keys.address}</b>.\n"
                                   f"Don't send dust! Don't send any other asset except {source_asset}!"
                                   )

        await SwapStates.FINISHED.set()

        await asyncio.sleep(5.0)
        await message.answer('Deposit detected: <code>0.05 BTC</code>')

        msg = None
        n_conf = 3
        for conf in range(n_conf + 1):
            text = f'Waiting for confirmations: {conf}/{n_conf}.'
            if msg is None:
                msg = await message.answer(text, disable_notification=True)
            else:
                await msg.edit_text(text)
            await asyncio.sleep(1.0)

        await msg.edit_text('<b>Confirmed!</b> Swapping via THORChain...')
        await asyncio.sleep(5.0)

        await message.answer_sticker('CAACAgIAAxkBAANkX7NqCYOW61VwyZQSeN3lhgMjC1AAAhkAAxSSqB1ORm41YTN_0B4E',
                                     reply_markup=ReplyKeyboardMarkup([[
                                         KeyboardButton('/start')
                                     ]]))

        await message.answer('<b>Success!</b> <a href="https://explorer.binance.org/tx/123">TX</a>!\n'
                             'You got <code>852.27 RUNE</code>\n'
                             'Slippage = 0.014%, total fee was <code>$0.5</code>\n'
                             'Thank you!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
