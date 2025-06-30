import sqlite3

con = sqlite3.connect('../db.sql')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS movies(title TEXT,user_id TEXT,rating INT)")
con.commit()
con.close()

def get_list_of_movies(user_id, handler):

	con = sqlite3.connect('../db.sql')
	cur = con.cursor()
	cur.execute(f"SELECT title,rating FROM movies WHERE user_id = {user_id}")
	movies = cur.fetchall()
	con.close()

	if not movies:
		return "У вас нет сохранённых фильмов"
	else:
		if handler == "list":
			text = "🍿 *Мои фильмы/сериалы*:\n\n"
		elif handler == "remove":
			text = "*Напишите название удаляемого фильма/сериала* \[Q\]\n\n"
		i = 0
		for title,rating in movies:
			i = i + 1 
			text = text + f"{i}\. *{title}* \n   ⭐ Рейтинг: {rating}/177\n\n"
		return text

def add_movie_to_db(title,user_id,rating):

	con = sqlite3.connect('../db.sql')
	cur = con.cursor()
	cur.execute("INSERT INTO movies(title,user_id,rating) VALUES(?,?,?)",(title,user_id,rating))
	con.commit()
	con.close()

def remove_from_db(title, user_id):

	con = sqlite3.connect('../db.sql')
	cur = con.cursor()
	cur.execute(f"DELETE FROM movies WHERE user_id = ? AND title = ?", (user_id,title))
	con.commit()
	con.close()
