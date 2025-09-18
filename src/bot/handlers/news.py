from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.states import UserState
from src.bot.config import sub_service
from src.bot.keyboards.news_keyboards import stop_keyboard, confirmation_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(UserState.add_category)

    kb = stop_keyboard()

    await message.answer(text=(
        "👋 Добро пожаловать в <b>Tech Digest</b>!\n\n"
        "Здесь вы сможете получать свежие статьи и новости по темам, "
        "которые вам интересны.\n\n"
        "Чтобы начать получать посты, введите категории."
        ),
        parse_mode="HTML",
        reply_markup=kb
    )


@router.message(UserState.add_category)
async def add_category(message: Message, state: FSMContext):
    category = message.text.lower().strip()
    sub_service.subscribe(category, message.from_user.id)

    kb = stop_keyboard()

    await message.answer(
        text=f"✅ Категория <i>{category}</i> успешно добавлена!\n"
             "Вы можете добавить ещё или нажать «Готово».",
        parse_mode="HTML",
        reply_markup=kb
    )


@router.callback_query(
    F.data == "stop",
    StateFilter(UserState.add_category)
)
async def confirm_categories(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    categories = sub_service.get_user_categories(user_id)

    if not categories:
        await callback.answer("❌ У вас нет добавленных категорий!", show_alert=True)
        return

    categories_list = "\n".join(f"- {cat}" for cat in categories)
    
    kb = confirmation_keyboard()
    await callback.message.answer(
        text=(
            "📂 Вы выбрали следующие категории:\n\n"
            f"{categories_list}\n\n"
            "Подтверждаете выбор?"
        ),
        parse_mode="HTML",
        reply_markup=kb
    )

    await state.set_state(UserState.confirm_categories)
    await callback.answer("Проверьте список категорий")


@router.callback_query(
    F.data.in_(["confirmation_yes", "confirmation_no"]),
    StateFilter(UserState.confirm_categories)
)
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirmation_yes":
        categories = sub_service.repo.get_user_categories(callback.from_user.id)

        await callback.message.answer(
            text=(
                "✅ Отлично! Вы будете получать статьи по категориям:\n"
                f"<i>{', '.join(categories)}</i>\n\n"
                "Ожидайте свежие материалы 🚀"
            ),
            parse_mode="HTML"
        )
        await state.set_state(UserState.subscribed)

    elif callback.data == "confirmation_no":
        sub_service.unsubscribe_all(callback.from_user.id)

        await callback.message.answer(
            text=(
                "🔄 Хорошо, давайте изменим список.\n"
                "Введите новые категории:"
            )
        )
        await state.set_state(UserState.add_category)

    await callback.message.edit_reply_markup(reply_markup=None)

