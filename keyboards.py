from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


async def languages_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text="🇺🇿O‘zbek tili", )
    key2 = KeyboardButton(text="🇷🇺Русский язык", )
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="🇺🇿O‘zbek tili", callback_data="uz"),
                InlineKeyboardButton(text="🇷🇺Русский язык", callback_data="ru"),
            ],
        ]
    )
    return keyboard


async def agree_keyboard(lang):
    if lang == "uz":
        text = ['Roziman', "Orqaga"]
    else:
        text = ['Я согласен', "Назад"]
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton(text=f"✅{text[0]}"), KeyboardButton(text=f"⬅️{text[1]}"))
    keyboard.resize_keyboard = True
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"✅{text[0]}", callback_data="confirm"),
                InlineKeyboardButton(text=f"⬅️{text[1]}", callback_data="cancel"),
            ],
        ]
    )
    return keyboard


async def choose_keyboard(lang):
    if lang == "uz":
        text = ["Taklif va tavsiyalar yuborish", "Murojaat va shikoyatlar yuborish", "Boshqa masalalar"]
    else:
        text = ["Отправить предложения и рекомендации", "Подать заявку и пожаловаться", "Другие вопросы"]
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton(text=f"🖊 {text[0]}"))
    keyboard.add(KeyboardButton(text=f"📩 {text[1]}"))
    keyboard.add(KeyboardButton(text=f"📝 {text[2]}"))
    keyboard.resize_keyboard = True

    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [

            [InlineKeyboardButton(text=f"{text[0]}", callback_data="taklif")],
            [InlineKeyboardButton(text=f"{text[1]}", callback_data="murojaat")],
            [InlineKeyboardButton(text=f"{text[2]}", callback_data="boshqa")],
        ]
    )
    return keyboard


async def check_legal(lang):
    if lang == "ru":
        text = ["Физическое лицо", "Юридическое лицо"]
    else:
        text = ["Jismoniy shaxs", "Yuridik shaxs"]
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton(text=f"👤 {text[0]}"), KeyboardButton(text=f"💼 {text[1]}"))
    keyboard.resize_keyboard = True
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"👤{text[0]}", callback_data="personal"),
                InlineKeyboardButton(text=f"💼{text[1]}", callback_data="community"),
            ],
        ]
    )
    return keyboard


async def confirm_keyboard(lang):
    if lang == "uz":
        text = ['Murojaatni yuborish', "Orqaga"]
    else:
        text = ['Отправлять', "Назад"]
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton(text=f"✅ {text[0]}"))
    keyboard.add(KeyboardButton(text=f"⬅️{text[1]}"))
    keyboard.resize_keyboard = True

    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=f"✅{text[0]}", callback_data="confirm")],
            [InlineKeyboardButton(text=f"⬅️{text[1]}", callback_data="cancel")]
        ]
    )
    return keyboard


async def cancel_keyboard(lang):
    if lang == "uz":
        text = ["O'tkazib yuborish"]
    else:
        text = ['Пропустить']
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton(text=f"🔜{text[0]}"))
    keyboard.resize_keyboard = True
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=f"✅{text[0]}", callback_data="cancel")],
        ]
    )
    return keyboard
