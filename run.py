import logging
import smtplib
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram.types import ParseMode, ContentType

from keyboards import *

API_TOKEN = '1825629775:AAHXI8_JonznuHT2MMa4hpkfzArmy3rouoM'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id, username=message.from_user.username)
    await state.set_state("get_lang")
    markup = await languages_keyboard()
    await message.reply("Tilni tanlang/ Выберите язык", reply_markup=markup, parse_mode=ParseMode.HTML)


@dp.message_handler(state="get_lang")
async def agree(message: types.Message, state: FSMContext):
    call_data = message.text
    user_id = message.from_user.id
    if call_data == '🇷🇺Русский язык':
        markup = await agree_keyboard("ru")
        await state.update_data(lang="ru")
        text = "Здравствуйте, добро пожаловать на бота, созданного для борьбы с коррупцией и антикоррупционной " \
               "деятельности в сфере туризма!\n\n<b>Важный!</b> Закон Республики Узбекистан «<b>О персональных данных</b>» " \
               "предусматривает трансграничную передачу данных физических лиц только при наличии согласия физических " \
               "лиц на трансграничную передачу персональных данных.\n\nДля того, чтобы использовать " \
               "@turizm_va_sport_vazirligi_антикоррупция_бота (@motas_antikor_bot) в соответствии с данным законом, " \
               "вы должны дать согласие на использование вашей личной информации. "
    else:
        markup = await agree_keyboard("uz")
        await state.update_data(lang="uz")
        text = "Assalomu alaykum, Turizm va sport sohasida korrupsion holatlarni va korrupsiyaga doir faoliyatlarga " \
               "qarshi kurashish uchun yaratilgan botga xush kelibsiz! \n\n<b>Muxim!</b> Jismoniy shaxslarning o‘z shaxsiga " \
               "ta’luqli ma’lumotlarini transchegaraviy uzatishga roziligi mavjud bo‘lgan taqdirdagina ma’lumotlarni " \
               "transchegaraviy uzatishning amalga oshirilishi O‘zbekiston Respublikasining  “Shaxsga doir " \
               "ma’lumotlar to‘g‘risida”gi Qonunda nazarda tutilgan. \n\nMazkur qonunga asosan " \
               "@turizm_va_sport_vazirligi_anticorruption_bot (@motas_antikor_bot) dan foydalanish uchun Sizning " \
               "shaxsingizga doir ma’lumotlaringizdan foydalanishga rozilik bildirishingiz lozim. "
    await bot.send_message(chat_id=user_id, text=text, parse_mode=ParseMode.HTML, reply_markup=markup)
    await state.set_state("choose")


@dp.message_handler(state='choose')
async def choose(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = message.text
    lang = data.get("lang")
    if lang == "uz":
        if text == "✅Roziman":
            data = "confirm"
        else:
            data = "cancel"
        text = "Ma’qul variantni tanlang:"
    else:
        if text == "✅Я согласен":
            data = "confirm"
        else:
            data = "cancel"
        text = "Выберите нужный вариант:"

    if data == "confirm":
        markup = await choose_keyboard(lang)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
        await state.set_state("legal")
    else:
        markup = await languages_keyboard()
        await bot.send_message(chat_id=message.from_user.id, text="Tilni tanlang/ Выберите язык", reply_markup=markup,
                               parse_mode=ParseMode.HTML)
        await state.set_state("get_lang")


@dp.message_handler(state="legal")
async def legal(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text_message = message.text
    lang = data.get("lang")
    if lang == "uz":
        text = "Shaxs turini tanlang:"
    else:
        text = "Выберите тип лица:"
    markup = await check_legal(lang)
    await state.update_data(choose=text_message)
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
    await state.set_state("name")


@dp.message_handler(state="name")
async def get_name(message: types.Message, state: FSMContext):
    message_text = message.text
    data = await state.get_data()
    lang = data.get("lang")
    datacha = ''
    choosing = data.get("choose")
    if lang == "uz":
        if choosing == "🖊 Taklif va tavsiyalar yuborish":
            datacha = "taklif"
        elif choosing == "📩 Murojaat va shikoyatlar yuborish":
            datacha = "murojaat"
        else:
            datacha = "boshqa"
    if datacha == "taklif":
        if lang == "uz":
            text = "Taklif va tavsiyalar beruvchi F.I.Sh / yuridik shaxs nomini kiriting"
        else:
            text = "Введите ФИО лица, делающего предложение и рекомендации Ф.И.Ш/юридическое лицо"
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await state.set_state("get_name")
    elif datacha == "murojaat":
        if lang == "uz":
            text = "Murojaat va shikoyatlar beruvchi F.I.Sh / yuridik shaxs nomini kiriting"
        else:
            text = "Введите наименование Ф.И.Ш/юридического лица, подающего жалобу и претензии"
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await state.set_state("location")
    else:
        if lang == "uz":
            text = "Murojaat va shikoyatlar beruvchi F.I.Sh / yuridik shaxs nomini kiriting"
        else:
            text = "Введите наименование Ф.И.Ш/юридического лица, подающего жалобу и претензии"
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await state.set_state("location")


@dp.message_handler(state="get_name")
async def get_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    name = message.text
    await state.update_data(name=name)
    if lang == "uz":
        text = "📞 Telefon raqamingiz "
    else:
        text = "📞 Ваш номер телефона"
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await state.set_state("phone")


@dp.message_handler(state="location")
async def get_location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    name = message.text
    await state.update_data(name=name)
    if lang == "uz":
        text = "📍 Manzilingizni kiriting"
    else:
        text = "📍 Введите свой адрес"
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await state.set_state("get_address")


@dp.message_handler(state="get_address")
async def get_address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    address = message.text
    await state.update_data(address=address)
    if lang == "uz":
        text = "Telefon raqamingiz "
    else:
        text = "📞 Ваш номер телефона"
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await state.set_state("phone")


@dp.message_handler(state="phone")
async def get_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    if lang == "uz":
        text = "📄 Murojaat matnini kiriting"
    else:
        text = "📄 Введите текст сообщения"
    phone = message.text
    await state.update_data(phone=phone)
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await state.set_state("main_text")


@dp.message_handler(state="main_text")
async def main_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    if lang == "uz":
        text = "Tegishli fayllarni biriktiring (video, audio, tekst va boshqalar)"
    else:
        text = "Прикрепите соответствующие файлы (видео, аудио, текст и т. д.)"
    main = message.text
    await state.update_data(main_text=main)
    markup = await cancel_keyboard(lang)
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
    await state.set_state("main_file")


@dp.message_handler(state="main_file", content_types=types.ContentType.DOCUMENT)
async def main_document(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    data = await state.get_data()
    name = message.document.file_name
    await message.document.download(destination=f"files/{name}")
    lang = data.get("lang")
    if lang == 'uz':
        text = f"<b>Kimdan: </b> {data.get('name')}\n" \
               f"<b>Tel: </b> {data.get('phone')}\n" \
               f"<b>username: </b> @{data.get('username')}\n" \
               f"<b>Murojaaj turi: </b> {data.get('choose')}\n" \
               f"<b>Murojaat matni: </b> {data.get('main_text')}\n"
    else:
        text = f"<b>От кого: </b> {data.get('name')}\n" \
               f"<b>Тел: </b> {data.get('phone')}\n" \
               f"<b>имя пользователя: </b> @{data.get('username')}\n" \
               f"<b>Тип: </b> {data.get('choose')}\n" \
               f"<b>Текст: </b> {data.get('main_text')}\n"
    await state.update_data(body=text, file_name=name, file_type="only")
    markup = await confirm_keyboard(data.get('lang'))
    await bot.send_document(chat_id=message.from_user.id, document=file_id, caption=text, reply_markup=markup,
                            parse_mode=ParseMode.HTML)
    await state.set_state("for_end")


@dp.message_handler(state="main_file", content_types=types.ContentType.PHOTO)
async def main_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    data = await state.get_data()
    file_name = f"{file_id}.jpg"
    await message.photo[-1].download(destination=f"files/{file_id}.jpg")
    lang = data.get("lang")
    if lang == 'uz':
        text = f"<b>Kimdan: </b> {data.get('name')}\n" \
               f"<b>Tel: </b> {data.get('phone')}\n" \
               f"<b>username: </b> @{data.get('username')}\n" \
               f"<b>Murojaaj turi: </b> {data.get('choose')}\n" \
               f"<b>Murojaat matni: </b> {data.get('main_text')}\n"
    else:
        text = f"<b>От кого: </b> {data.get('name')}\n" \
               f"<b>Тел: </b> {data.get('phone')}\n" \
               f"<b>имя пользователя: </b> @{data.get('username')}\n" \
               f"<b>Тип: </b> {data.get('choose')}\n" \
               f"<b>Текст: </b> {data.get('main_text')}\n"
    await state.update_data(body=text, file_name=file_name, file_type="only")
    markup = await confirm_keyboard(data.get('lang'))
    await bot.send_photo(chat_id=message.from_user.id, photo=file_id, caption=text, reply_markup=markup,
                         parse_mode=ParseMode.HTML)
    await state.set_state("for_end")


@dp.message_handler(state="main_file", content_types=types.ContentType.VIDEO)
async def main_video(message: types.Message, state: FSMContext):
    file_id = message.video.file_id
    data = await state.get_data()
    await message.video.download(destination=f"files/{message.video.file_name}")
    lang = data.get("lang")
    if lang == 'uz':
        text = f"<b>Kimdan: </b> {data.get('name')}\n" \
               f"<b>Tel: </b> {data.get('phone')}\n" \
               f"<b>username: </b> @{data.get('username')}\n" \
               f"<b>Murojaaj turi: </b> {data.get('choose')}\n" \
               f"<b>Murojaat matni: </b> {data.get('main_text')}\n"
    else:
        text = f"<b>От кого: </b> {data.get('name')}\n" \
               f"<b>Тел: </b> {data.get('phone')}\n" \
               f"<b>имя пользователя: </b> @{data.get('username')}\n" \
               f"<b>Тип: </b> {data.get('choose')}\n" \
               f"<b>Текст: </b> {data.get('main_text')}\n"
    await state.update_data(body=text, file_name=message.video.file_name, file_type="only")
    dat = await state.get_data()
    markup = await confirm_keyboard(data.get('lang'))
    await bot.send_video(chat_id=message.from_user.id, video=file_id, caption=text, reply_markup=markup,
                         parse_mode=ParseMode.HTML)
    await state.set_state("for_end")


@dp.message_handler(state="main_file", content_types=types.ContentType.VOICE)
async def main_audio(message: types.Message, state: FSMContext):
    file_id = message.voice.file_id
    file_name = f"{file_id}.ogg"
    data = await state.get_data()
    await message.voice.download(destination=f"files/{file_id}.ogg")
    lang = data.get("lang")
    if lang == 'uz':
        text = f"<b>Kimdan: </b> {data.get('name')}\n" \
               f"<b>Tel: </b> {data.get('phone')}\n" \
               f"<b>username: </b> @{data.get('username')}\n" \
               f"<b>Murojaaj turi: </b> {data.get('choose')}\n" \
               f"<b>Murojaat matni: </b> {data.get('main_text')}\n"
    else:
        text = f"<b>От кого: </b> {data.get('name')}\n" \
               f"<b>Тел: </b> {data.get('phone')}\n" \
               f"<b>имя пользователя: </b> @{data.get('username')}\n" \
               f"<b>Тип: </b> {data.get('choose')}\n" \
               f"<b>Текст: </b> {data.get('main_text')}\n"
    await state.update_data(body=text, file_name=message.video.file_name, file_type="only")
    markup = await confirm_keyboard(data.get('lang'))
    await bot.send_voice(chat_id=message.from_user.id, voice=file_id, caption=text, reply_markup=markup,
                         parse_mode=ParseMode.HTML)
    await state.set_state("for_end")


@dp.message_handler(state="main_file", content_types=types.ContentType.AUDIO)
async def main_audio(message: types.Message, state: FSMContext):
    data = await state.get_data()
    audio = message.audio
    await message.audio.download(destination=f"files/{audio.file_name}")
    lang = data.get("lang")
    if lang == 'uz':
        text = f"<b>Kimdan: </b> {data.get('name')}\n" \
               f"<b>Tel: </b> {data.get('phone')}\n" \
               f"<b>username: </b> @{data.get('username')}\n" \
               f"<b>Murojaaj turi: </b> {data.get('choose')}\n" \
               f"<b>Murojaat matni: </b> {data.get('main_text')}\n"
    else:
        text = f"<b>От кого: </b> {data.get('name')}\n" \
               f"<b>Тел: </b> {data.get('phone')}\n" \
               f"<b>имя пользователя: </b> @{data.get('username')}\n" \
               f"<b>Тип: </b> {data.get('choose')}\n" \
               f"<b>Текст: </b> {data.get('main_text')}\n"
    await state.update_data(body=text, file_name=message.audio.file_name, file_type="only")
    markup = await confirm_keyboard(data.get('lang'))
    await bot.send_audio(chat_id=message.from_user.id, audio=audio.file_id, caption=text, reply_markup=markup,
                         parse_mode=ParseMode.HTML)
    await state.set_state("for_end")


@dp.message_handler(state="main_file", content_types=types.ContentType.TEXT)
async def cancel_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    if lang == 'uz':
        text = f"<b>Kimdan: </b> {data.get('name')}\n" \
               f"<b>Tel: </b> {data.get('phone')}\n" \
               f"<b>username: </b> @{data.get('username')}\n" \
               f"<b>Murojaaj turi: </b> {data.get('choose')}\n" \
               f"<b>Murojaat matni: </b> {data.get('main_text')}\n"
    else:
        text = f"<b>От кого: </b> {data.get('name')}\n" \
               f"<b>Тел: </b> {data.get('phone')}\n" \
               f"<b>имя пользователя: </b> @{data.get('username')}\n" \
               f"<b>Тип: </b> {data.get('choose')}\n" \
               f"<b>Текст: </b> {data.get('main_text')}\n"
    await state.update_data(body=text, file_name="")
    markup = await confirm_keyboard(data.get('lang'))
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
    await state.set_state("for_end")


@dp.message_handler(state="for_end")
async def end(message: types.Message, state: FSMContext):
    message_text = message.text
    data = await state.get_data()
    body = data.get("body")
    lang = data.get("lang")
    call_data = ""
    if lang == "uz":
        if message_text == "✅ Murojaatni yuborish":
            call_data = "confirm"
        else:
            call_data = "calcel"
        text = "Murojaat yuborildi"
    else:
        if message_text == "✅ Отправлять":
            call_data = "confirm"
        else:
            call_data = "calcel"
        text = "Обращение было отправлено"
    file_type = data.get("file_type")
    file_name = data.get("file_name")
    if call_data == 'confirm':
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        sender_address = 'forbot2503@gmail.com'
        sender_pass = 'Wertus89'
        receiver_address = 'jahongirnormuminov8@gmail.com'
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Yangi murojaat'
        message.attach(MIMEText(body, 'html'))
        if file_name != "":
            if file_type == "only":
                file = MIMEApplication(open(f"files/{file_name}", 'rb').read())
                file.add_header('Content-Disposition', 'attachment', filename=file_name)
                message.attach(file)
            else:
                files = file_name.split("=+=")
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()

    else:
        data = await state.get_data()
        lang = data.get("lang")
        if lang == "uz":
            text = "Tegishli fayllarni biriktiring (video, audio, tekst va boshqalar)"
        else:
            text = "Прикрепите соответствующие файлы (видео, аудио, текст и т. д.)"
        markup = await cancel_keyboard(lang)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
        await state.set_state("main_file")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
