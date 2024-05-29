import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import urllib3
import math
urllib3.disable_warnings()

# TODO :
#  Подумать о прохождении по страничкам, процесс реализован, но возможен новый способ

pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 550)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 70)

df_summary = pd.DataFrame(columns=['tema','numbers', 'prices', 'executor', 'contract_date', 'suppliers', 'links','text_value','contract'])

spisok_tem = pd.read_excel(fr'goszacupki_text.xlsx', sheet_name='Лист1')
spisok_tem = list(spisok_tem)
# print(len(list(spisok_tem)))
spisok_tem = list(dict.fromkeys(spisok_tem))

for tema in spisok_tem:
    print(tema)

    # Код для определения кол-во записей и страниц
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'doNotAdviseToChangeLocationWhenIosReject=true; _ym_uid=1710413694532552103; _ym_d=1710413694; _ym_isad=2; _ym_visorc=b; contentFilter=; contractCsvSettingsId=80db3bf2-57a1-4b35-b47c-50da92d2e4d2',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        'searchString': f'{tema}',
        'morphology': 'on',
        'search-filter': 'Дате размещения',
        'pageNumber': '1',
        'sortDirection': 'false',
        'recordsPerPage': '_50',
        'showLotsInfoHidden': 'false',
        'sortBy': 'UPDATE_DATE',
        'fz44': 'on',
        'fz223': 'on',
        'af': 'on',
        'ca': 'on',
        'pc': 'on',
        'pa': 'on',
        'currencyIdGeneral': '-1',
    }
    response = (requests.get(
        'https://zakupki.gov.ru/epz/contract/search/results.html',
        params=params,
        headers=headers,
        verify=False))
    soup_1 = BeautifulSoup(response.text, 'html.parser')
    try:
        count_zap = int(soup_1.find('div', class_='search-results__total').text.split()[0])
    except:
        count_zap = 1000

    num_pages = math.ceil(count_zap/50)
    print(num_pages)

    for num_page in range(num_pages):
        # print(f'Страница: {num_page+1}')
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'doNotAdviseToChangeLocationWhenIosReject=true; _ym_uid=1710413694532552103; _ym_d=1710413694; _ym_isad=2; _ym_visorc=b; contentFilter=; contractCsvSettingsId=80db3bf2-57a1-4b35-b47c-50da92d2e4d2',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        params = {
            'searchString': f'{tema}',
            'morphology': 'on',
            'search-filter': 'Дате размещения',
            'pageNumber': f'{int(num_page+1)}',
            'sortDirection': 'false',
            'recordsPerPage': '_50',
            'showLotsInfoHidden': 'false',
            'sortBy': 'UPDATE_DATE',
            'fz44': 'on',
            'fz223': 'on',
            'af': 'on',
            'ca': 'on',
            'pc': 'on',
            'pa': 'on',
            'currencyIdGeneral': '-1',
        }
        response = (requests.get(
            'https://zakupki.gov.ru/epz/contract/search/results.html',
            params=params,
            headers=headers,
            verify=False))
        soup = BeautifulSoup(response.text, 'html.parser')
        numbers = [''.join(i.text.split()) for i in soup.find_all('div', class_='registry-entry__header-mid__number')]
        contract = [''.join(i.text.split()) for i in soup.find_all('div', class_='registry-entry__body-value')]
        prices = [''.join(i.text.split()) for i in soup.find_all('div', class_='price-block__value')]
        executor = [' '.join(i.text.split()) for i in soup.find_all('div', class_='registry-entry__body-href')]
        contract_date = [re.search('\d\d.\d\d.\d\d\d\d',' '.join(i.text.split())).group(0) for i in soup.find_all('div', class_='data-block mt-auto')]
        links = ['https://zakupki.gov.ru'+i.find('a').get('href') for i in soup.find_all('div', class_='registry-entry__header-mid__number')]
        text_value = []
        for i in soup.find_all('div', class_='d-flex lots-wrap-content__body__val'):
            if i.get("data-tooltip") is not None:
                text_value.append(i.get("data-tooltip").replace('<div class="custom-tooltiptext text-break">', '').replace('</div>', ''))
            else:
                if len(i) > 1:
                    text_value.append(' '.join(i.text.split()))
        suppliers = []
        for i in numbers:
            num = i[1:]
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                # 'Cookie': 'doNotAdviseToChangeLocationWhenIosReject=true; _ym_uid=1710413694532552103; _ym_d=1710413694; _ym_isad=2; contentFilter=; contractCsvSettingsId=80db3bf2-57a1-4b35-b47c-50da92d2e4d2; _ym_visorc=b',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            params = {'reestrNumber': f'{num}'}
            response = requests.get(
                'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html',
                params=params,
                headers=headers)
            soup_1 = BeautifulSoup(response.content, "html.parser")
            suppliers.append(re.sub (r'\s+', ' ',soup_1.find('td', class_='tableBlock__col tableBlock__col_first text-break').text))
        # print(len(numbers),len(prices),len(executor),len(contract_date),len(contract))
        data_tuples = list(zip(numbers, prices, executor, contract_date, suppliers,links,text_value,contract))
        df = pd.DataFrame(data_tuples, columns=['numbers', 'prices', 'executor', 'contract_date', 'suppliers', 'links','text_value','contract'])
        df['tema'] = tema
        # print(df)
        df_summary = pd.concat([df_summary, df])

    # df_summary.reset_index(inplace=True)
    # del df_summary['index']
    df_summary['prices'] = df_summary['prices'].apply(lambda x: x.replace('₽', ''))
df_summary.drop_duplicates(inplace=True)
df_summary['text_value'] = df_summary['text_value'].apply(lambda x: x.replace('\n', ''))
df_summary['text_value'] = df_summary['text_value'].apply(lambda x: x.replace('\r', ''))
df_summary['text_value'] = df_summary['text_value'].apply(lambda x: re.sub('\(\d+\)','', x))
df_summary['text_value'] = df_summary['text_value'].str.strip()
df_summary['contract_date'] = pd.to_datetime(df_summary['contract_date'], format='%d.%m.%Y')

print(df_summary)
# df_summary.to_excel('government_procurement_test.xlsx')
# df_summary.to_pickle('government_procurement_test.pkl')

