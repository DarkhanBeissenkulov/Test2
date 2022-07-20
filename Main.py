import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
from pandas import ExcelWriter
from pandas import ExcelFile
import time
import urllib3
urllib3.disable_warnings()

pd.options.mode.chained_assignment = None  # default='warn'

r = requests.get('https://www.goszakup.gov.kz/ru/registry/rqc?count_record=2000&page=1', verify=False)
soup = BeautifulSoup(r.content, "html.parser")
results = soup.find("table", class_="table table-bordered table-hover").find_all('a')
results = [tag.get('href') for tag in results]

df_req_data = pd.DataFrame(columns=['Наименование организации', 'БИН организации', 'ФИО руководителя', 'ИИН руководителя', 'Полный адрес организации', 'link'])

for row in results:
    r2 = requests.get(str(row), verify=False)
    time.sleep(1)
    soup2 = BeautifulSoup(r2.content, "html.parser")
    results2 = soup2.find("div", class_="content-block")
    try:
        # -Наименование организации
        org_name = results2.find_all('h1')[0].text.strip()
    except:
        org_name = 'Ошибка'
    try:
        # -БИН организации
        bin = results2.find('th', text="БИН участника").find_next_sibling("td").text.strip()
    except:
        bin = 'Ошибка'
    try:
        # -ФИО руководителя
        fio = results2.find('th', text="ФИО").find_next_sibling("td").text.strip()
    except:
        fio = 'Ошибка'
    try:
        # -ИИН руководителя
        iin = results2.find('th', text="ИИН").find_next_sibling("td").text.strip()
    except:
        iin = 'Ошибка'
    try:
        # -Полный адрес организации
        address = results2.find_all("table", class_ = "table table-striped")[3].find_all("td")[2].text.strip()
    except:
        address = 'Ошибка'
    df_req_data.loc[df_req_data.shape[0]] = [org_name, bin, fio, iin, address, str(row)]
    
    org_name = ''
    bin = ''
    fio = ''
    iin = ''
    address = ''

# Файл должен содержать только уникальные записи (на источнике встречаются повторения)
df_req_data = df_req_data.drop_duplicates(subset='БИН организации', keep='first')

writer = pd.ExcelWriter('D:\+work\Dasha\Files\\test2.xlsx', engine='xlsxwriter')
df_req_data.to_excel(writer, sheet_name= 'Main', index=False)
writer.save()