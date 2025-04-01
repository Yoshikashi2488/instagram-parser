import json
import csv
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

DEMO_PROFILE = "https://www.instagram.com/instagram/"  # Официальный аккаунт Instagram
CHROME_DRIVER_PATH = "./chromedriver"  # Относительный путь (драйвер в папке проекта)


def parse_instagram_profile(profile_url):
    """
    Парсит публичные данные профиля Instagram
    :param profile_url: URL профиля для анализа
    :return: Словарь с данными профиля
    """
    # Настройка Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    try:
        # Инициализация драйвера
        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Загрузка страницы
        driver.get(profile_url)
        time.sleep(5)  # Ожидание загрузки (можно заменить на явное ожидание)

        # Парсинг основных метрик
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        followers, posts = parse_profile_metrics(soup)

        # Парсинг постов (упрощенный вариант)
        post_data = parse_posts_data(driver)

        # Формирование результата
        return {
            "profile": profile_url,
            "followers": int(followers) if followers else 0,
            "posts": int(posts) if posts else 0,
            "posts_data": "saved to instagram_posts.csv" if post_data else "no posts data"
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}
    finally:
        if 'driver' in locals():
            driver.quit()


def parse_profile_metrics(soup):
    """Извлекает метрики профиля из HTML"""
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        if 'property' in tag.attrs and tag.attrs['property'] == 'og:description':
            content = tag.attrs['content']
            parts = content.split()
            return parts[0].replace(',', ''), parts[4].replace(',', '')
    return None, None


def parse_posts_data(driver):
    """Парсит данные постов"""
    post_data = []
    try:
        # Эти классы могут измениться при обновлении Instagram
        posts = driver.find_elements(By.CSS_SELECTOR, 'div._aabd._aa8k._al3l')[:3]  # Ограничиваем 3 постами для демо

        for post in posts:
            try:
                post.click()
                time.sleep(2)
                post_html = driver.page_source
                post_soup = BeautifulSoup(post_html, 'html.parser')

                # Извлечение данных поста
                caption = post_soup.find('div', {'class': '_a9zs'}).text if post_soup.find('div',
                                                                                           {'class': '_a9zs'}) else ''
                likes = post_soup.find('span', {'class': '_aacl._aaco._aacw._aacx._aada'}).text if post_soup.find(
                    'span', {'class': '_aacl._aaco._aacw._aacx._aada'}) else '0'
                date = post_soup.find('time')['datetime'][:10] if post_soup.find(
                    'time') else datetime.now().date().isoformat()

                post_data.append({
                    'caption': caption[:100] + '...' if len(caption) > 100 else caption,  # Обрезаем длинные описания
                    'likes': likes,
                    'date': date
                })

                # Закрытие модального окна
                driver.find_element(By.CSS_SELECTOR, 'div.x160vmok.x10l6tqk.x1eu8d0j.x1vjfegm').click()
                time.sleep(1)

            except Exception as e:
                print(f"Post parsing error: {str(e)}")
                continue

        # Сохранение в CSV
        if post_data:
            pd.DataFrame(post_data).to_csv('instagram_posts.csv', index=False)

    except Exception as e:
        print(f"Posts processing error: {str(e)}")

    return post_data


if __name__ == "__main__":
    print("Instagram Profile Parser Demo")
    print(f"Analyzing profile: {DEMO_PROFILE}")

    result = parse_instagram_profile(DEMO_PROFILE)
    print("\nResult:")
    print(json.dumps(result, indent=2))