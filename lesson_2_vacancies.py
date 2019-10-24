import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

vacancy_name = str(input('Введите название вакансии '))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
page_count = 0
vacs = pd.DataFrame(columns=['name', 'link_to_vac', 'min_pay', 'max_pay', 'source'])
cycle_count = 0
while page_count <= 2:
    req = requests.get(
        f'https://kazan.hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&text={vacancy_name}&page={page_count}',
        headers=headers).text
    html_parsed = bs(req, 'lxml')

    vacancy_block = html_parsed.find('div', {'class': 'vacancy-serp'})
    vacancies = vacancy_block.findAll('div', {
        'data-qa': ['vacancy-serp__vacancy', 'vacancy-serp__vacancy vacancy-serp__vacancy_premium']})

    for vac in vacancies:
        vac_data = {}
        main_info = vac.find('span', {'class': 'g-user-content'}).findChild()
        name = main_info.getText()
        link_to_vac = main_info['href']
        if vac.find('div', {'class': 'vacancy-serp-item__compensation'}) == None:
            pay = 'None'
        else:
            pay = vac.find('div', {'class': 'vacancy-serp-item__compensation'}).getText()
        min_pay = re.findall('(\d+[\s\d]*)-?', pay)

        if len(min_pay) > 0:
            min_pay = int(min_pay[0].replace('\xa0', ''))

        max_pay = re.findall('-([0-9]+\s*[0-9]+|[до]+\s*[0-9]+\s*[0-9]+)', pay)
        if len(max_pay) > 0:
            max_pay = int(max_pay[0].replace('\xa0', ''))
        if not max_pay:
            max_pay = 'None'
        if not min_pay:
            min_pay = 'None'

        vac_data['name'] = name
        vac_data['link_to_vac'] = link_to_vac
        vac_data['min_pay'] = min_pay
        vac_data['max_pay'] = max_pay
        vac_data['source'] = 'hh.ru'
        vacs.loc[cycle_count] = vac_data
        cycle_count += 1

    page_count += 1

# Пишем код для superjob
main_link_job = 'https://www.superjob.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
page_superjob = 1
cycle_count_job = cycle_count
while page_superjob <= 3:
    req_superjob = requests.get(f'https://www.superjob.ru/vacancy/search/?keywords={vacancy_name}&page={page_superjob}',
                                headers=headers).text
    superjob_parsed = bs(req_superjob, 'lxml')
    vacancy_block_superjob = superjob_parsed.find('div', {'style': 'display:block'})
    vacancies_superjob = vacancy_block_superjob.findAll('div',
                                                        {'class': '_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})
    for vac_job in vacancies_superjob:
        vac_data_job = {}
        name_superjob = vac_job.findChild('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
        pay = vac_job.find('span',
                           {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()

        min_pay_job = re.findall('По договорённости|[от]\s[0-9]+\s[0-9]+|[0-9]+\s[0-9]+\s—|[0-9]+\s[0-9]+', pay)
        max_pay_job = re.findall('— ([0-9]+\s?[0-9]+)', pay)
        if len(min_pay_job) > 0:
            min_pay_job = min_pay_job[0].replace('\xa0', '')
        if min_pay_job == 'По договорённости':
            min_pay_job = 'None'
        if len(max_pay_job) > 0:
            max_pay_job = int(max_pay_job[0].replace('\xa0', ''))
        if not max_pay_job:
            max_pay_job = 'None'
        link_to_vac_job = vac_job.find('div', {'class': '_3syPg _1_bQo _2FJA4'}).findChild().findChild()['href']
        vac_data_job['name'] = name_superjob
        vac_data_job['link_to_vac'] = main_link_job + link_to_vac_job
        vac_data_job['min_pay'] = min_pay_job
        vac_data_job['max_pay'] = max_pay_job
        vac_data_job['source'] = 'superjob.ru'
        vacs.loc[cycle_count_job] = vac_data_job
        cycle_count_job += 1

    page_superjob += 1

vacs
