from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def languages_keyboard():
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="🇺🇿O‘zbek tili", callback_data="uz"),
                InlineKeyboardButton(text="🇷🇺Русский язык", callback_data="ru"),
            ],
        ]
    )
    return markup


async def agree_keyboard(lang):
    if lang == "uz":
        text = ['Roziman ', "Orqaga"]
    else:
        text = ['Я согласен ', "Назад"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"✅{text[0]}", callback_data="confirm"),
                InlineKeyboardButton(text=f"⬅️{text[1]}", callback_data="cancel"),
            ],
        ]
    )
    return markup


async def choose_keyboard(lang):
    if lang == "uz":
        text = ["Taklif va tavsiyalar yuborish", "Murojaat va shikoyatlar yuborish", "Boshqa masalalar"]
    else:
        text = ["Отправить предложения и рекомендации", "Подать заявку и пожаловаться", "Другие вопросы"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [

            [InlineKeyboardButton(text=f"{text[0]}", callback_data="taklif")],
            [InlineKeyboardButton(text=f"{text[1]}", callback_data="murojaat")],
            [InlineKeyboardButton(text=f"{text[2]}", callback_data="boshqa")],
        ]
    )
    return markup


async def check_legal(lang):
    if lang == "ru":
        text = ["Физическое лицо", "Юридическое лицо"]
    else:
        text = ["Jismoniy shaxs", "Yuridik shaxs"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"👤{text[0]}", callback_data="personal"),
                InlineKeyboardButton(text=f"💼{text[1]}", callback_data="community"),
            ],
        ]
    )
    return markup


async def confirm_keyboard(lang):
    if lang == "uz":
        text = ['Murojaatni yuborish', "Orqaga"]
    else:
        text = ['Отправлять', "Назад"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=f"✅{text[0]}", callback_data="confirm")],
            [InlineKeyboardButton(text=f"⬅️{text[1]}", callback_data="cancel")]
        ]
    )
    return markup


async def cancel_keyboard(lang):
    if lang == "uz":
        text = ["O'tkazib yuborish"]
    else:
        text = ['Пропустить']
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=f"✅{text[0]}", callback_data="cancel")],
        ]
    )
    return markup
