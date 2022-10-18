import requests
from bs4 import BeautifulSoup
import re
import colorama

URL = 'https://proza.ru/'
# user_name = input('Введите логин: ').lower()  # все логины на stihi.ru прописаны маленьким регистром
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}


def get_homepage_statistic(login: str):
    """Получаем статистику со страницы автора"""
    url = f'{URL}/avtor/{login.lower()}'
    response = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    # Получаем заголовок
    name = 'Статистика по профилю на проза.ру: ' + soup.find('h1').text

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
    url = f'{URL}/rec_author.html?{login.lower()}'
    response = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    # Ищем нужный блок
    block = soup.find('div', class_="recproza").text

    # Выводим на экран
    return last_review_formatting(block)


def last_review_formatting(block):
    last_review = re.sub('Заявить о нарушении', '', block.replace('', ''))
    last_review = last_review.strip()
    return f'Последняя полученная рецензия:\n{last_review}'


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
                 ' это пользователи интернета, не зарегистрированные на портале Проза.ру.':
        return block.find_all('p')[0].text
    return result


def get_last_received_review(login: str):
    """Получаем последнюю рецензию, которую написал автор(login)"""
    url = f'{URL}/rec_writer.html?{login.lower()}'
    response = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    # Ищем нужный блок
    block = soup.find('div', class_="recproza").text

    # Выводим на экран
    return last_received_review_formatter(block)


def last_received_review_formatter(block):
    last_review = re.sub('Заявить о нарушении', '', block.replace('', ''))
    last_review = last_review.strip()
    return f'Последняя написанная рецензия:\n{last_review}'


def how_many_readers_today(login: str):
    """Получаем строку с данными о новых читателях за сегодняшний день"""
    url = f'{URL}/readers.html?{login.lower()}'
    response = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    # Ищем нужный блок
    block = soup.find('index')
    return check_and_display_number_of_reads(block)
    # вывод: 'Сегодня n новых читателей и n прочтений всех произведений'


def get_last_reader(login: str) -> str:
    """Узнать последнего читателя"""
    url = f'{URL}/readers.html?{login.lower()}'
    response = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    block = soup.find('div', class_='margins')  # Ищем нужную информацию
    block = block.find_all('tr')

    result = block[1].text.strip().split('\n')  # Используем первую строку, форматируем ее
    return f'Последний читатель:\nЧитатель: {result[0].title()}\nПроизведение: {result[1]}\n' \
           f'Дата: {result[2]}\nВремя: {result[3]}\nИсточник: {result[4].title()}'


# def get_favorites(login: str):  # OPTIMIZE-ME!!!
#     url = 'http://stat.stihira-proza.ru/'
#
#     cookies = {
#         'ASP.NET_SessionId': 'gpaovy5kqbj53acw2vjuwkkn',
#         '__ddg1_': 'Exm41GDctbLpQp6aJg1c',
#     }
#
#     headers = {
#         'Accept': '*/*',
#         'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'DNT': '1',
#         'Origin': 'http://stat.stihira-proza.ru',
#         'Referer': 'http://stat.stihira-proza.ru/',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
#         'X-MicrosoftAjax': 'Delta=true',
#         'X-Requested-With': 'XMLHttpRequest',
#     }
#
#     data = {
#         'ctl00$ctl10': 'ctl00$MainContent$updatePanel|ctl00$MainContent$buttonShowStat',
#         'ctl00$MainContent$listPortals': 'proza.ru',
#         'ctl00$MainContent$textAuthorLogin': f'{login}',
#         'ctl00$MainContent$listStatViewParam': 'Followers',
#         '__EVENTTARGET': '',
#         '__EVENTARGUMENT': '',
#         '__LASTFOCUS': '',
#         '__VIEWSTATE': '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',
#         '__VIEWSTATEGENERATOR': 'CA0B0334',
#         '__EVENTVALIDATION': 'I2PkYNOc2UWrnLTlXf7eBMk34pVRO7ZcBr63A0cTZe4U6umIfQ9ObbhYyXldP/uWTUNQV1qIrzxaiOyv8n/jqOo2SJQ5J7tLhVzoKc5mvOfMPGR/7W2sqPeVPpTCD8TVC2WIOV7NQV14im6XMkmG/X8+WojTu+g7SzgvjdQ6PoRbcxfqp+2kVWCJL66mx02sicyHsWsdWVW6cO6s35p3m3lN26kYHgdsJTSNOa7KPhytGP6wCBqtbIbJIbfB5AYekfeT/u7CFGXObzqlLLkfN6k9hBXuISI/ktzzpW0h53v0YESjXtxX6ADyMbhqKqyX4Hu9Znmd4cLa2ph4RQnvy4TiuGN/uN1YF30FQxDAcY2Ou+JiMKA2X57vzgu0qsiqddYD9BobMZypgL0AvX/3UvFWpHtCFPxcc/8vDRy7FCUd2FPMZv/wRVx4sNhAkr66o9fpPus4tg5burWD7Zwdu7rRvUMovPpN9bshpCMrZcCtJQJyHofKgloYs6l02vO3Xfq9+igJl90Kz1oqbfI1gX/b46mLUqDKHaoaf03jSaP5DoO+Pd7X3Pcnefx/lQXIbSwNDGHp43kkFMgD5uIcYeEgsvBtNN4DkyUkXnTCnxpNZb7tCHEPfSN4iwmw4uX8MAp8KVgU7Zs5DsH6DCJU2UhucXGLZDdwfJ9vBD5nzlY/yPJLnxBV2iHfCKZIynnhVqZ4egryqPEja9FNI8cldKyQI/H805wqgR4jjtO6aWsHChKpYhwdMWnB7w7XyzBmkG8DF0qh/jRuKOams/PkRytOISuvIJBG/ATbhISu+MUQ8LgTQO3l74uHy6r7Mqotv1ZV8dS6ng+zARq2qusJOcxNxdK9xuAZiWNIvaIgYK6n5IasuUqXIW4r79IK4eZFbZChryMIXqTEosXmWBnWG4kSztelyXvvJfA+JrLqZrrrXwf/dLpYFAaSPtd8DcO4s7xnxnA7klZofLAvTqK7YJKpOJn5gJ374mA+NxJMBo5P+D5od3t8X2xMSydMiYd2haxZ/c39yxu+YmxCHmSS6+4MmW0qSbD4dmbRsdmGiABpkCzyxYkxjHe/dZG7Xmqn5EtCvHvaOOg8jObB1+5z5SFN0s40aFjLqIFkCqxVKLE483nW2/yO33yJq/9rpw9/',
#         '__ASYNCPOST': 'true',
#         'ctl00$MainContent$buttonShowStat': 'Показать',
#     }
#
#     response = requests.post(url=url, headers=headers, cookies=cookies, data=data, verify=False).text
#     soup = BeautifulSoup(response, 'lxml')
#     result = soup.find('caption', align='Top').text.strip()
#     result_str = f'В избранных у {result[-1]} авторов'


def print_all_stats(login: str):
    """"Вывести всю статистику в консоль"""
    if login == '0':  # Проверка на пропуск сбора статистики
        pass
    else:  # Выводим статистику
        print(colorama.Fore.GREEN + '--------------------')
        print(get_homepage_statistic(login))
        print('--------------------')
        print(get_last_given_review(login))
        print('--------------------')
        print(get_last_received_review(login))
        print('--------------------')
        print(how_many_readers_today(login))
        print('--------------------')
        print(get_last_reader(login))
        # print('--------------------')
        # print(get_favorites(login))
