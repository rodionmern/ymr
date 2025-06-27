import sqlite3
import telebot
from telebot import types

token = "token"

bot=telebot.TeleBot(token)

con = sqlite3.connect('db.sql')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS movies(title TEXT,user_id TEXT,rating INT)")
con.commit()
con.close()

@bot.message_handler(commands=['start'])
def start_button(message):
	markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
	list_btn=types.KeyboardButton("Мои фильмы")
	add_btn=types.KeyboardButton("Добавить фильм")
	remove_btn=types.KeyboardButton("Удалить фильм")
	markup.add(list_btn,add_btn,remove_btn)
	bot.send_message(message.chat.id,"Выберите нужное в меню.",reply_markup=markup)

@bot.message_handler(content_types="text")
def commands(message):
	user_id = message.from_user.id

	if message.text == "Мои фильмы":
		list_of_movies(user_id, message, "list")
	if message.text == "Добавить фильм":
		bot.send_message(message.chat.id,"Введите через запятую название фильма и его оценку:")
		bot.register_next_step_handler(message,add_to_db)
	if message.text == "Удалить фильм":
		list_of_movies(user_id, message, "remove")
		bot.register_next_step_handler(message, remove_from_db)

def list_of_movies(user_id, message, handler):

	con = sqlite3.connect('db.sql')
	cur = con.cursor()
	cur.execute(f"SELECT title,rating FROM movies WHERE user_id = {user_id}")
	movies = cur.fetchall()
	con.close()
	if not movies:
			bot.send_message(message.chat.id,"Нет сохранённых фильмов.")
	else:
		if handler == "list":
			text = "Мои фильмы:\n"
		elif handler == "remove":
			text = "Напишите название удаляемого фильма:\n"
		i = 0
		for title,rating in movies:
			i = i + 1 
			text = text + f"{i}\. *{title}* \| {rating}/10\n"
		bot.send_message(message.chat.id,text,parse_mode="MarkdownV2")

def add_to_db(message):
	data = message.text

	user_id = message.from_user.id # КОСТЫЛЬ!!! надо будет найти решение
	
	title = data.split(',')[0]
	rating = data.split(',')[-1].strip()
	con = sqlite3.connect('db.sql')
	cur = con.cursor()
	cur.execute("INSERT INTO movies(title,user_id,rating) VALUES(?,?,?)",(title,user_id,rating))
	con.commit()
	con.close()
	bot.send_message(message.chat.id,"Фильм успешно сохранён в базу данных.")

def remove_from_db(message):
	movie_title = message.text

	user_id = message.from_user.id # КОСТЫЛЬ!!! надо будет найти решение

	con = sqlite3.connect('db.sql')
	cur = con.cursor()
	cur.execute(f"DELETE FROM movies WHERE user_id = ? AND title = ?", (user_id,movie_title))
	con.commit()
	con.close()

	bot.send_message(message.chat.id,"Фильм успешно удален из базы данных.")

bot.infinity_polling()