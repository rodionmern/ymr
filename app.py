import requests
import telebot
from telebot import types
from logic.kinopoisk_api import get_movie_by_name
from logic.database import get_list_of_movies, add_movie_to_db, remove_from_db

token = "token"

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_button(message):
	markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
	list_btn=types.KeyboardButton("Мои фильмы")
	find_btn=types.KeyboardButton("Найти и добавить фильм")
	remove_btn=types.KeyboardButton("Удалить фильм")
	markup.add(list_btn,find_btn,remove_btn)
	bot.send_message(message.chat.id,"Выберите нужное в меню.",reply_markup=markup)

@bot.message_handler(content_types="text")
def commands(message):
	user_id = message.from_user.id
	if message.text == "Мои фильмы":
		send_list_of_movies(message, user_id, "list")
	if message.text == "Найти и добавить фильм":
		msg = bot.send_message(message.chat.id, "Напишите название фильма, который хотите найти:")
		bot.register_next_step_handler(msg, search_movie)
	if message.text == "Удалить фильм":
		send_list_of_movies(message, user_id, "remove")
		bot.register_next_step_handler(message, lambda m: remove_movie(m, user_id))

def search_movie(message):
	query = message.text
	try:
		data = get_movie_by_name(query)
		print(data)
		if data:
			bot.send_photo(message.chat.id, data[0], data[1])
		msg = bot.send_message(message.chat.id, "*Напишите оценку от 1 до 10\!* 🌟", parse_mode="MarkdownV2")
		bot.register_next_step_handler(msg, lambda m: save_rating(m, query))
	except Exception as e:
		bot.send_message(message.chat.id, "Ошибка получения данных")

def save_rating(message, title):
	rating = int(message.text)
	user_id = message.from_user.id
	if isinstance(rating, int):
		add_movie_to_db(title, user_id, rating)
		bot.send_message(message.chat.id, "*Фильм успешно добавлен в базу данных\!* 💾", parse_mode="MarkdownV2")

def remove_movie(message, user_id):
	query = message.text
	try:
		remove_from_db(query, user_id)
		bot.send_message(message.chat.id, "*Фильм успешно удален из базы данных\!* 🗑️", parse_mode="MarkdownV2")
	except Exception as e:
		bot.send_message(message.chat.id, "Ошибка удаления данных")

def send_list_of_movies(message, user_id, handler):
	try:
		data = get_list_of_movies(user_id, handler)
		if data:
			bot.send_message(message.chat.id, data, parse_mode="MarkdownV2")
	except Exception as e:
		bot.send_message(message.chat.id, "Ошибка получения данных")

bot.infinity_polling()