import re

import colorama
import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = 'https://stihi.ru'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}


def get_homepage_statistic(login: str):
    """Получаем статистику со страницы автора"""
    url = f'{URL}/avtor/{login}'
    response = requests.get(url=url, headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')

    # Получаем заголовок
    name = 'Статистика по профилю на стихи.ру: ' + soup.find('h1').text

    # Ищем нужный нам блок
    block = soup.find('p', style="margin-left:20px")

    # Всего произведений:
    poems = check_poems(block)
    # Получено рецензий:
    received_reviews = check_received_reviews(block)
    # Написано рецензий:
    given_reviews = check_given_reviews(block)
    # Читателей:
    number_of_readers = check_number_of_readers(block)
    # Вывод статистики
    return homepage_statistic_formatter(name, poems, received_reviews, given_reviews, number_of_readers)


def check_poems(block) -> str:
    """Возвращает количество произведений, ищет в html блоке(block)"""
    poems_count = block.find('b').text
    return f'Произведений: {poems_count}'


def check_received_reviews(block) -> str:
    """Возвращает количество полученных рецензий, ищет в html блоке(block)"""
    received_reviews = block.find_all('b')[1].text
    return f'Получено рецензий: {received_reviews}'


def check_given_reviews(block) -> str:
    """Возвращает количество написанных рецензий, ищет в html блоке(block)"""
    given_reviews = block.find_all('b')[2].text
    return f'Написано рецензий: {given_reviews}'


def check_number_of_readers(block) -> str:
    """Возвращает количество читателей, ищет в html блоке(block)"""
    number_of_readers = block.find_all('b')[3].text
    return f'Читателей: {number_of_readers}'


def homepage_statistic_formatter(name, poems, r_reviews, g_reviews, readers):
    """Форматирование данных в строку (5)"""
    return f'{name}\n{poems}\n{r_reviews}\n{g_reviews}\n{readers}'


def get_last_given_review(login: str):
    """Получаем последнюю рецензию, которую получил автор(login)"""
    url = f'{URL}/rec_author.html?{login}'
    response = requests.get(url=url, headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')

    # Ищем нужный блок
    block = soup.find('div', class_="recstihi").text

    # Выводим на экран
    return last_review_formatter(block)


def last_review_formatter(block):
    last_review = re.sub('Заявить о нарушении', '', block.replace('', ''))
    last_review = last_review.strip()
    return f'Последняя полученная рецензия:\n{last_review}'


def get_last_received_review(login: str):
    """Получаем последнюю рецензию, которую написал автор(login)"""
    url = f'{URL}/rec_writer.html?{login}'
    response = requests.get(url=url, headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')

    # Ищем нужный блок
    block = soup.find('div', class_="recstihi").text

    # Выводим на экран
    return last_received_review_formatter(block)


def check_and_display_number_of_reads(block):
    try:
        block.find('b')
        index = 1
    except:
        index = 2
    result = block.find_all('p')[index].text
    if result == 'В данном списке отображаются все прочтения за последние две недели.' \
                 ' Счетчик на авторской странице учитывает уникальных читателей:' \
                 ' один и тот же читатель может прочитать несколько произведений автора,' \
                 ' но счетчиком читателей он будет учтен один раз. Неизвестные читатели –' \
                 ' это пользователи интернета, не зарегистрированные на портале Стихи.ру.':
        return block.find_all('p')[0].text
    return result


def last_received_review_formatter(block):
    last_review = re.sub('Заявить о нарушении', '', block.replace('', ''))
    last_review = last_review.strip()
    return f'Последняя написанная рецензия:\n{last_review}'


def how_many_readers_today(login: str):
    """Получаем строку с данными о новых читателях за сегодняшний день"""
    url = f'{URL}/readers.html?{login}'
    response = requests.get(url=url, headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')
    # Ищем нужный блок
    block = soup.find('index')
    return check_and_display_number_of_reads(block)
    # вывод: 'Сегодня n новых читателей и n прочтений всех произведений'


def get_last_reader(login: str) -> str:
    """Узнать последнего читателя"""
    url = f'{URL}/readers.html?{login}'
    response = requests.get(url=url, headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')

    block = soup.find('div', class_='margins')  # Ищем нужную информацию
    block = block.find_all('tr')

    result = block[1].text.strip().split('\n')  # Используем первую строку, форматируем ее
    return f'Последний читатель:\nЧитатель: {result[0].title()}\nПроизведение: {result[1]}\n' \
           f'Дата: {result[2]}\nВремя: {result[3]}\nИсточник: {result[4].title()}'  # Fix-Me


def get_elected(login: str):
    url = f'http://stat.stihira-proza.ru/?portal=stihi&login={login}'
    response = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    block = soup.find('table')
    result = block.find_all('tr')[1].find_all('td')[4].get_text()

    return f'В избранных у {result} авторов/автора:\n' \
           f'{get_list_of_elected(login)}'


def get_list_of_elected(soup):
    table = soup.find('table', id='MainContent_gridStatFollowers')

    headers = []
    for i in table.find_all('th'):
        title = i.text
        headers.append(title)

    # Создание дата фрейма
    mydata = pd.DataFrame(columns=headers)

    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(mydata)
        mydata.loc[length] = row
    # Export to csv
    # mydata.to_csv('stihiru_elected.csv', index=False)
    return mydata


def print_all_stats(login: str):
    if login == '0':
        pass
    else:
        """"Вывод статистики"""
        print('\n' + colorama.Fore.YELLOW + '--------------------')
        print(get_homepage_statistic(login))
        print('--------------------')
        print(get_last_given_review(login))
        print('--------------------')
        print(get_last_received_review(login))
        print('--------------------')
        print(how_many_readers_today(login))
        print('--------------------')
        print(get_last_reader(login))
        print('--------------------')
        print(get_elected(login), '\n')  # '\n' чтобы не было соединения со статистикой модуля 'prozarustats.py'
