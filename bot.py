import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ====== SOZLAMALAR ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/erinaluz")
WEBSITE_URL = os.getenv("WEBSITE_URL", "https://erinal-shop.netlify.app/")
# ========================

router = Router()


class Register(StatesGroup):
    full_name = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Register.full_name)
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "Iltimos, <b>ism va familiyangizni</b> yozing.\n"
        "Masalan: <i>Alisher Karimov</i>",
        parse_mode="HTML",
    )


@router.message(Register.full_name, F.text)
async def get_name(message: Message, state: FSMContext):
    full_name = message.text.strip()

    if len(full_name.split()) < 2:
        await message.answer(
            "❗️ Iltimos, ism va familiyangizni birgalikda yozing.\n"
            "Masalan: <i>Alisher Karimov</i>",
            parse_mode="HTML",
        )
        return

    await state.update_data(full_name=full_name)
    await state.clear()

    channel_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=CHANNEL_URL)]
        ]
    )
    await message.answer(
        f"Rahmat, <b>{full_name}</b>! ✅\n\n"
        "🛍 <b>ERINAL shopga xush kelibsiz!</b>\n\n"
        "Yangiliklar, aksiyalar va chegirmalardan xabardor bo'lish uchun "
        "telegram kanalimizga obuna bo'ling 👇",
        parse_mode="HTML",
        reply_markup=channel_kb,
    )

    site_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 ERINAL saytiga o'tish", url=WEBSITE_URL)]
        ]
    )
    await message.answer(
        "Endi pastdagi tugmani bosib, <b>ERINAL</b> saytiga o'tishingiz mumkin 👇",
        parse_mode="HTML",
        reply_markup=site_kb,
    )


@router.message(Register.full_name)
async def wrong_input(message: Message):
    await message.answer("❗️ Iltimos, ism va familiyangizni matn ko'rinishida yozing.")


async def main():
    logging.basicConfig(level=logging.INFO)
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN topilmadi. Environment variable sifatida kiriting.")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
