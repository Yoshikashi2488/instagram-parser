# Instagram Profile Parser

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Парсер публичных данных профилей Instagram с сохранением результатов в CSV.

##  Возможности

- Получение количества подписчиков и публикаций
- Сохранение данных о постах (описание, лайки, дата)
- Работа в headless-режиме (без открытия браузера)
- Экспорт результатов в JSON и CSV

##  Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Yoshikashi2488/instagram-parser.git
cd instagram-parser
```
2. Установите зависимости:

```bash
pip install requests beautifulsoup4 selenium pandas
```
Скачайте ChromeDriver для вашей версии Chrome и поместите в папку проекта.

## Использование
Основной скрипт:

```bash
python parser.py
```
Для анализа конкретного профиля:
```
from parser import parse_instagram_profile

result = parse_instagram_profile("https://www.instagram.com/username/")
print(result)
```