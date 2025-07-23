from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/osint', methods=['POST'])
def osint_search():
    data = request.get_json()
    query = data.get('query', '')
    results = []

    try:
        # Пошук у соціальних мережах
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

        # Перевірка WHOIS (з API whoisxmlapi.com)
        try:
            whois_url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?domainName={query}&username=anovyk@gmail.com&password=7002TolikS@n2007F!xer2025"
            whois_response = requests.get(whois_url, timeout=10)
            if whois_response.status_code == 200:
                whois_data = whois_response.json()
                results.append({'source': 'WHOIS', 'data': whois_data.get('WhoisRecord', 'Немає даних')})
            else:
                results.append({'source': 'WHOIS', 'data': f'Помилка: {whois_response.status_code}'})
        except Exception as e:
            results.append({'source': 'WHOIS', 'data': f'Помилка: {str(e)}'})

        # Пошук email (використання Email Permutator)
        try:
            if '@' in query:
                email_parts = query.split('@')
                if len(email_parts) == 2:
                    domain = email_parts[1]
                    possible_emails = [f"{name}@{domain}" for name in ['info', 'support', 'contact']]  # Проста генерація
                    results.append({'source': 'Email Permutator', 'data': possible_emails})
                else:
                    results.append({'source': 'Email Permutator', 'data': 'Неправильний формат email'})
            else:
                results.append({'source': 'Email Permutator', 'data': 'Введіть email для генерації варіантів'})
        except Exception as e:
            results.append({'source': 'Email Permutator', 'data': f'Помилка: {str(e)}'})

        # Геолокація (використання OpenStreetMap Nominatim)
        try:
            nominatim_url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json"
            nominatim_response = requests.get(nominatim_url, timeout=10)
            if nominatim_response.status_code == 200:
                nominatim_data = nominatim_response.json()
                if nominatim_data:
                    geo_info = {'lat': nominatim_data[0]['lat'], 'lon': nominatim_data[0]['lon'], 'display_name': nominatim_data[0]['display_name']}
                    results.append({'source': 'Geolocation (OpenStreetMap)', 'data': geo_info})
                else:
                    results.append({'source': 'Geolocation (OpenStreetMap)', 'data': 'Геолокація не знайдена'})
            else:
                results.append({'source': 'Geolocation (OpenStreetMap)', 'data': f'Помилка: {nominatim_response.status_code}'})
        except Exception as e:
            results.append({'source': 'Geolocation (OpenStreetMap)', 'data': f'Помилка: {str(e)}'})

    except Exception as e:
        results.append({'source': 'Помилка', 'data': f'Виникла помилка: {str(e)}'})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
