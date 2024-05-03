from hashlib import new
import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class StopGame:
	host = 'https://stopgame.ru'
	url = 'https://stopgame.ru/review/new'
	lastkey = ""
	lastkey_file = ""

	def __init__(self, lastkey_file):
		self.lastkey_file = lastkey_file

		if(os.path.exists(lastkey_file)):
			self.lastkey = open(lastkey_file, 'r').read()
		else:
			f = open(lastkey_file, 'w')
			self.lastkey = self.get_lastkey()
			f.write(self.lastkey)
			f.close()

	# def new_games(self):
	# 	r = requests.get(self.url)
	# 	html = BS(r.content, 'html.parser')

	# 	new = []
	# 	items = html.select('.tiles > .items > .item > a')
	# 	for i in items:
	# 		key = self.parse_href(i['href'])
	# 		if(self.lastkey < key):
	# 			new.append(i['href'])

	# 	return new
 
	# def new_games(self):
	# 	r = requests.get(self.url)
	# 	html = BS(r.content, 'html.parser')

	# 	new = []
	# 	items = html.select('.tiles > .items > .item > a')
	# 	for i in items:
	# 		new.append(i['href'])
		
	# 	return new
	
	def new_games(self):
		r = requests.get(self.url)
		if r.status_code == 200:
			html = BS(r.content, 'html.parser')
			print("Connection successful.")
		else:
			print(f"Error: Connection failed with status code {r.status_code}.")
  
		games = []
		items = html.select('.list-view > ._default-grid_1mwhk_258 > div > article > a')
	
		if items:
			print("Elements found.") 
		else:
			print("No elements found.")
        
		for item in items:
			href = item['href']
			games.append(href)

		return games

	def game_info(self, uri):
		link = self.host + uri
		r = requests.get(link)
		html = BS(r.content, 'html.parser')

		# Отримання зображення
  
		# Шукаємо тег <source>
		source_tag = html.find('source')
		# Якщо тег <source> знайдено
		if source_tag:
			# Отримуємо URL зображення з атрибута srcset
			image_url = source_tag['srcset'].split(',')[0].strip().split()[0]

		# Отримання заголовка
		title = html.find('h1').text.strip()

		# Отримання опису
		description = html.find('p', class_='_text_12po9_111 _text-width_12po9_111').text.strip()

		# Отримання оцінки
		rating_container = html.find('section', class_='_news-games-container_12po9_1602')

		if rating_container:
			rating_icons = rating_container.find('svg', class_='_sg-rating_17n8v_478')

		# Створення рядка для оцінки
		score = ""
		if rating_icons.find('use')['href'] == '#ratings/izum':
			score = "⭐⭐⭐⭐"  
		if rating_icons.find('use')['href'] == '#ratings/pohvalno':
			score = "⭐⭐⭐"  
		if rating_icons.find('use')['href'] == '#ratings/prohodnyak':
			score = "⭐⭐"  
		if rating_icons.find('use')['href'] == '#ratings/musor':
			score = "⭐"  		
		else:
			score = "Оцінка не знайдена"  # Встановлюємо повідомлення, якщо оцінка не знайдена	

		info = {
				"link": link, 
				"image": image_url,
				"title": title,
				"score": score,
				"excerpt": description
			}
		
		return info

	def download_image(self, url):
		r = requests.get(url, allow_redirects=True)

		a = urlparse(url)
		filename = os.path.basename(a.path)
		open(filename, 'wb').write(r.content)

		return filename

	def identify_score(self, score):
		if(score == 'score-1'):
			return "Мусор 👎"
		elif(score == 'score-2'):
			return "Проходняк ✋"
		elif(score == 'score-3'):
			return "Похвально 👍"
		elif(score == 'score-4'):
			return "Изумительно 👌"

	def get_lastkey(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		items = html.select('.list-view > ._default-grid_1mwhk_258 > div > article > a')
		return self.parse_href(items[0]['href'])

	def parse_href(self, href):
		return href.split('/')[-1]

	def update_lastkey(self, new_key):
		self.lastkey = new_key

		with open(self.lastkey_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(new_key))
			f.truncate()

		return new_key
	
	def parse_div(self):
		r = requests.get(self.url)
		html_content = r.content
		soup = BS(html_content, 'html.parser')

		# Знаходження всіх елементів <div>, які мають атрибут data-key
		divs_with_data_key = soup.find_all('div', attrs={'data-key': True})

		new = []
		for div in divs_with_data_key:
			article = div.find('article')
			new.append(article['aria-label'])

		return new