# server.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

app = Flask(__name__)

# Функція для збору даних із соціальних мереж
def scrape_social_media(query):
    results = []
    try:
        # Приклад пошуку в Google (Google Dorks)
        google_url = f"https://www.google.com/search?q={query}+site:*.twitter.com | site:*.linkedin.com | site:*.facebook.com"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(google_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links[:5]:
            href = link.get('href')
            if href and 'url=' in href:
                url = href.split('url=')[1].split('&')[0]
                results.append({'source': 'Social Media', 'data': url})
    except Exception as e:
        results.append({'source': 'Social Media', 'data': f'Помилка: {str(e)}'})
    return results

# Функція для перевірки WHOIS
def check_whois(domain):
    try:
        response = requests.get(f"https://api.whois.com/{domain}", timeout=10)
        return [{'source': 'WHOIS', 'data': response.json().get('registrant', 'Немає даних')}]
    except Exception as e:
        return [{'source': 'WHOIS', 'data': f'Помилка: {str(e)}'}]

# Функція для пошуку email
def find_emails(query):
    try:
        response = requests.get(f"https://api.hunter.io/v2/email-finder?domain={query}&api_key=your_hunter_api_key", timeout=10)
        return [{'source': 'Email Finder', 'data': response.json().get('data', 'Немає даних')}]
    except Exception as e:
        return [{'source': 'Email Finder', 'data': f'Помилка: {str(e)}'}]

# Функція для пошуку за геолокацією
def geolocation_search(query):
    try:
        response = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={query}&key=your_opencage_api_key", timeout=10)
        data = response.json()
        return [{'source': 'Geolocation', 'data': data.get('results', 'Немає даних')}]
    except Exception as e:
        return [{'source': 'Geolocation', 'data': f'Помилка: {str(e)}'}]

# Основний ендпоінт
@app.route('/api/osint', methods=['POST'])
def osint_search():
    data = request.get_json()
    query = data.get('query', '')
    results = []
    
    # Збір даних із різних джерел
    results.extend(scrape_social_media(query))
    if '.' in query:  # Перевірка, чи це домен
        results.extend(check_whois(query))
    results.extend(find_emails(query))
    results.extend(geolocation_search(query))
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
