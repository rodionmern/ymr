import requests

headers = {"X-API-KEY": "token"}

def get_movie_by_name(query):
	print(query)
	params = {
		'query': query
	}
	response = requests.get(
		'https://api.kinopoisk.dev/v1.4/movie/search',
		headers=headers,
		params=params
	)

	if response.status_code == 200:
		data = response.json()
		if data.get('docs'):
			data = data['docs'][0]
			title = data['name']
			year = data['year']
			description = f'{(data['description'])[:200]}...'
			rating_kp = round(float(data['rating']['kp']), 1)
			rating_imdb = data['rating']['imdb']
			photo_url = data['poster']['url']
		else:
			return {"error": "Фильм не найден."}
	else:
		return {"error": f"API Error: {response.status_code}"}

	result = [photo_url, f"""{title} {year}

{description}

Рейтинг: 
{rating_kp}/10 KP
{rating_imdb}/10 IMDB"""]

	return result

	# bot.send_message(message=message.chat.id, text="Секс", reply_markup=find_markup)
