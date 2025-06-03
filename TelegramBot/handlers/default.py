import asyncio

from TelegramBot.keyboards.main import get_menu_kb

from aiogram import Bot
from aiogram import Router, F
from aiogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery,
    
)
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.exceptions import TelegramBadRequest

from TelegramBot.helpers.admin_filter import IsAdmin
from TelegramBot.config import ADMINS, CHAT_ID

default_router = Router()
pre_checkout_failed_reason = "Что-то пошло не так. Нет больше места для денег 😭"
pre_checkout_ok_reason = "Ваши денежки у нас"

@default_router.message(CommandStart())
async def default_handler(message: Message) -> None:
    await message.answer('Извините, я не говорю по-русски.', )

@default_router.message(Command('test_k'))
async def cmd_start_2(message: Message):
    button = InlineKeyboardButton(text="Test", callback_data="test_me")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.reply("Just a test", reply_markup=keyboard)

@default_router.message(F.text.regexp(r'.*одогреть общак.*'))
async def cmd_donate(message: Message):
    text = message.text.split(" ")
    if len(text) != 3 or not text[2].isdigit() or int(text[2]) == 0:
        return message.reply("""
                            Дружище, ты пишешь что-то странное. Вот образец:
                            подогреть общак 100
                            """)

    amount = int(text[2])

    prices = [LabeledPrice(label="XTR", amount=amount)]
    await message.answer_invoice(
        title="Пополнение казны",
        description=f"Варвара будет довольна {amount} звездам",
        prices=prices,

        provider_token="",
        payload=f"{amount}_stars",

        currency="XTR"
    )

@default_router.pre_checkout_query()
async def on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(
        ok=True,
        error_message=f"{pre_checkout_ok_reason}"
    )

@default_router.message(F.successful_payment)
async def on_successful_payment(message: Message, bot: Bot):
    async def send_user_message():
        await message.answer(
            text="Обещаем ваши деньги обязательно пойдут на развлечения и кутеж",
            message_effect_id="5104841245755180586",
        )

    async def notify_chat():
        await bot.send_message(
            CHAT_ID,
            text=f"Казна пополнена на {message.successful_payment.total_amount}",
        )

    await asyncio.gather(
        send_user_message(),
        notify_chat()
    )

@default_router.message(IsAdmin(ADMINS), Command("refund"))
async def cmd_refund(message: Message, bot: Bot, command: CommandObject):
    transaction_id = command.args
    if transaction_id is None:
        await message.answer(f"refund-no-code-provided")
        return
    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id
        )
        await message.answer(f"refund-ok")
    except TelegramBadRequest as error:
        if "CHARGE_NOT_FOUND" in error.message:
            text = f"refund-code-not-found"
        elif "CHARGE_ALREADY_REFUNDED" in error.message:
            text = f"refund-already-refunded"
        else:
            text = f"refund-code-not-found"
        await message.answer(text)
        return
