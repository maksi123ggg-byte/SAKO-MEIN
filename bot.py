import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8996202857:AAHI9zeyF5Ivl80u0-GC8uRwGLeXcg6zemI"

FUNPAY_URL = "https://funpay.com/uk/users/19612186/"
PAYGAME_URL = "https://paygame.ru/users/SAKO1"
REVIEWS_URL = "https://funpay.com/uk/users/19612186/"
SUPPORT_URL = "https://t.me/SK_SAKO"

products = {
    "7-Я|СОПРОВОД|ГАРАНТ 20КК+ШМОТ": "230 ₽",
    "7-Я|СОПРОВОД|ГАРАНТ 10КК+ШМОТ": "150 ₽",
    "7-Я|СОПРОВОД|ГАРАНТ 50КК+ШМОТ": "450 ₽",
    "5-Я|СОПРОВОД|ГАРАНТ 10КК+ШМОТ": "150 ₽",
    "5-Я|СОПРОВОД|ГАРАНТ 20КК+ШМОТ": "250 ₽",
    "7-Я|БУСТ|20КК-БЕЗ ШМОТА": "200 ₽",
    "7-Я|БУСТ|50КК-БЕЗ ШМОТА": "400 ₽"
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛒 Услуги клана SK¹", callback_data="view_products")
    kb.button(text="⭐ Отзывы", url=REVIEWS_URL)
    kb.button(text="💬 Поддержка", url=SUPPORT_URL)
    kb.adjust(1)

    await message.answer(
        "🎒 Добро пожаловать!\n\nВыбирайте 👇",
        reply_markup=kb.as_markup()
    )

@dp.callback_query(F.data == "view_products")
async def show_products(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()

    for idx, (product, price) in enumerate(products.items()):
        kb.button(text=f"{product} — {price}", callback_data=f"prod:{idx}")

    kb.button(text="⬅️ Назад", callback_data="back_to_menu")
    kb.adjust(1)

    await callback.message.edit_text(
        "📱 СПИСОК УСЛУГ:",
        reply_markup=kb.as_markup()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("prod:"))
async def select_product(callback: CallbackQuery):
    prod_idx = int(callback.data.split(":")[1])

    product_name = list(products.keys())[prod_idx]
    product_price = list(products.values())[prod_idx]

    kb = InlineKeyboardBuilder()
    kb.button(text="💳 FunPay", url=FUNPAY_URL)
    kb.button(text="💳 PayGame", url=PAYGAME_URL)
    kb.button(text="⬅️ Назад", callback_data="view_products")
    kb.adjust(1)

    await callback.message.edit_text(
        f"{product_name}\n\n💰 {product_price}",
        reply_markup=kb.as_markup()
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛒 Услуги", callback_data="view_products")
    kb.button(text="⭐ Отзывы", url=REVIEWS_URL)
    kb.button(text="💬 Поддержка", url=SUPPORT_URL)
    kb.adjust(1)

    await callback.message.edit_text(
        "Главное меню",
        reply_markup=kb.as_markup()
    )
    await callback.answer()

async def handle(request):
    return web.Response(text="Bot is running")

async def main():
    asyncio.create_task(dp.start_polling(bot))

    app = web.Application()
    app.router.add_get("/", handle)

    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
