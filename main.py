import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

url = 'https://otakudesu.cloud'

def getAnimeTitles():
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        titles = [title.get_text(strip=True) for title in soup.find_all('h2')]
        return {"titles": titles}
    except requests.RequestException as e:
        return {"error": str(e)}

def searchAnime(search):
    try:
        params = {'s': search, 'post_type': 'anime'}
        r = requests.get(url, params=params)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        titles = [title.get_text(strip=True) for title in soup.find_all('h2')]
        return {"titles": titles}
    except requests.RequestException as e:
        return {"error": str(e)}

@app.route('/anime-list')
def animeList():
    data = getAnimeTitles()
    return jsonify(data)

@app.route('/anime-search/<anime>')
def animeSearch(anime):
    data = searchAnime(anime)
    return jsonify(data)

@app.route('/')
def home():
    return '<h1>Hello, World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
