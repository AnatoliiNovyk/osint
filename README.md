# osint
## OSINT веб-додаток

**Пояснення:**  
Цей OSINT веб-додаток містить два файли:  
1. **index.html**: Фронтенд на React із Tailwind CSS для зручного інтерфейсу. Дозволяє вводити запити (нік, email, домен) і відображає результати пошуку.  
2. **server.py**: Бекенд на Flask, який обробляє запити та збирає дані з відкритих джерел:  
   - Пошук у соціальних мережах (Google Dorks для Twitter, LinkedIn, Facebook).  
   - Перевірка WHOIS для доменів (потрібен API-ключ).  
   - Пошук email через Hunter.io (потрібен API-ключ).  
   - Геолокаційний пошук через OpenCage (потрібен API-ключ).  
**Встановлення:**  
   - Встановіть Python і бібліотеки: `pip install flask requests beautifulsoup4`.  
   - Замініть `your_hunter_api_key` і `your_opencage_api_key` реальними ключами від Hunter.io та OpenCage.  
   - Запустіть сервер: `python server.py`.  
   - Відкрийте `index.html` у браузері.  
**Функціонал:**  
   - Збір інформації з соціальних мереж.  
   - Аналіз доменів і email.  
   - Геолокація за запитами.  
   - Можливість розширення для Shodan, Maltego, архівів Wayback Machine.
