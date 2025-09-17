from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(text=(
        "👋 Добро пожаловать в <b>Tech Digest</b>!\n\n"
        "📚 Здесь вы сможете получать свежие статьи и новости по темам, "
        "которые вам интересны."
    ),
    parse_mode="HTML")

