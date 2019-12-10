import requests
from bs4 import BeautifulSoup as bs
import csv

# эмулируем поведение браузера
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/78.0.3904.108 Safari/537.36'}

base_url = 'https://spb.hh.ru/search/vacancy?area=2&search_period=3&text=Python&page=0'


def hh_parse(base_url, headers):
    """функция для парсинга данных с сайта HH"""
    # создаем список для вакансий
    jobs_hh = []
    # браузер думает, что мы человек и не выкидывает нас
    session = requests.Session()
    # эмулируем открытие страницы в браузере
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        # находим вакансии на стр hh
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        # углубляемся в вакансию и находим нужную инфу
        for div in divs:
            # выводим название вакансии
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            # теперь находим ссылки на вакансии
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            # находим компанию
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            # описание вакансии
            text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = text1 + ' ' + text2
            jobs_hh.append({
                'title': title,
                'href': href,
                'company': company,
                'content': content
            })
        print(len(jobs_hh))
    else:
        print('ERROR.Status code :' + str(request.status_code))
    return jobs_hh


def files_w(jobs_hh):
    """Функция для записи в файл csv"""
    with open('vacancy_pars.csv', 'w') as f:
        vacancy_hh = csv.writer(f)
        vacancy_hh.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for jobs in jobs_hh:
            vacancy_hh.writerow((jobs['title'], jobs['href'], jobs['company'], jobs['content']))


# вызываем функции
jobs_hh = hh_parse(base_url, headers)
files_w(jobs_hh)
