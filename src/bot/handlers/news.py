from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.bot.states import UserState

from src.bot.config import sub_service

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(UserState.add_category)
    await message.answer(text=(
        "👋 Добро пожаловать в <b>Tech Digest</b>!\n\n"
        "Здесь вы сможете получать свежие статьи и новости по темам, "
        "которые вам интересны.\n\n"
        "Чтобы начать получать посты, введите категории."
    ),
    parse_mode="HTML")


@router.message(UserState.add_category)
async def add_category(message: Message, state: FSMContext):
   sub_service.subscribe(message.text.lower(), message.from_user.id) 

