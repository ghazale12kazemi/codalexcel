import jdatetime
import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from requests import Timeout
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from unidecode import unidecode

from personal.models import Codal, Symbol

requests.packages.urllib3.disable_warnings()

TRANS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
ARAB_TRANS = str.maketrans('يك', 'یک')
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


def isFund(company_name):
    if "سرمایه" in company_name or "صندوق" in company_name:
        return "fund"
    else:
        return "not fund"


def whichType(title):
    if "گزارش فعالیت ماهانه" in title:
        return "mahane"
    elif "صورت‌های مالی  سال مالی" in title:
        return "salane"
    elif "اطلاعات و صورت‌های مالی میاندوره‌ای  دوره" in title:
        return "miyandore"
    elif "تلفیقی" in title:
        return "talfigi"
    else:
        return "unknown"


def load_all_values_from_excel(self, query):
    try:
        f = open(self, encoding='utf-8')
        html_doc = f.read().translate(ARAB_TRANS)
        f.close()

        soup = BeautifulSoup(html_doc, 'html.parser')

        elemenet = soup.find_all('span')

        for e in elemenet:
            if query == e.text.strip():
                parent = e.find_parent()
                next_parent = parent.find_next_sibling()

                if len(next_parent.text.strip()) > 0:
                    break

        if '(' in next_parent.text:
            return (-1 * int(
                next_parent.text.translate(TRANS).replace(',', '').replace(')', '').replace('(', '').strip()))
        else:
            return int(next_parent.text.translate(TRANS).replace(',', '').strip())
    except:
        return "Error"


def find_duration(title, type):
    if type == "miyandore":
        return unidecode(title[42])
    elif type == "salane":
        return 12
    elif type == "mahane":
        return 1
    elif type == "talfigi":
        if "سال " in title:
            return 12
        else:
            return unidecode(title[48])
    else:
        return 0


def find_year(title, type):
    if type == "miyandore":
        return unidecode(title[58:62])
    elif type == "salane":
        return unidecode(title[32:37])
    elif type == "mahane":
        return unidecode(title[41:45])
    elif type == "talfigi":
        if "سال " in title:
            return unidecode(title[39:43])
        else:
            return unidecode(title[64:68])
    else:
        return 0


def find_month(title, type):
    if type == "miyandore":
        return unidecode(title[63:65])
    elif type == "salane":
        return unidecode(title[38:40])
    elif type == "mahane":
        return unidecode(title[46:48])
    elif type == "talfigi":
        if "سال " in title:
            return unidecode(title[44:46])
        else:
            return unidecode(title[69:71])
    else:
        return 0


def should_crawl_codal_detail(title, type):
    if "(حسابرسی نشده)" in title:
        if type == "miyandore" and len(title) == 83:
            return True
        elif type == "salane" and len(title) == 58:
            return True
        elif type == "mahane":
            return True
        elif type == "talfigi":
            if "سال " in title and len(title) == 64:
                return True
            elif len(title) == 89:
                return True
        else:
            return False


def crawl():
    driver = webdriver.Chrome()
    for i in range(1, 50):
        URL = 'https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true' \
              '&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1' \
              '&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={}&Publisher=false&TracingNo=-1&search=false'.format(
            i + 1)
        print(i)

        js = requests.get(URL, verify=False).json()

        ls = js['Letters']
        for l in ls:
            if l['HasExcel']:
                u = "https://www.codal.ir/" + l['Url']
                url = str(u).replace("&sheetId=.*", "&sheetId=1")
                title = l['Title'].replace('/', '-')
                symbol = l['Symbol']
                company_name = l['CompanyName']
                raw_datetime = l['PublishDateTime']
                fund = isFund(company_name)
                type = whichType(title)
                trans_datetime = raw_datetime.translate(TRANS)
                d = jdatetime.datetime.strptime(trans_datetime, DATE_FORMAT)
                duration = find_duration(title, type)
                year = find_year(title, type)
                month = find_month(title, type)

                if fund == "not fund" and type != "unknown" and type != "mahane" and should_crawl_codal_detail(title,
                                                                                                               type):
                    print(type)
                    print(raw_datetime)
                    url = str(url) + "&sheetId=1"
                    print('Downloading ..')
                    r = requests.get(url, verify=False).text
                    driver.get(url)
                    try:
                        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'table')))
                        content = driver.page_source
                        filename = f'media/{company_name}-codal{title}.html'

                        with open(filename, 'wb') as f:
                            f.write(content.encode())
                        forosh = load_all_values_from_excel(filename, "درآمدهای عملیاتی")
                        sood_amaliyati = load_all_values_from_excel(filename, 'سود (زیان) عملیاتی')
                        sood_khales = load_all_values_from_excel(filename, 'سود (زیان) خالص')


                    finally:
                        print("kkk")

                    sym, _ = Symbol.objects.get_or_create(slug=symbol, defaults={'company_name': company_name})

                    Codal.objects.create(
                        title=title,
                        symbol=sym,
                        filename=filename,
                        publish_date_time=d.togregorian(),
                        fund=fund,
                        type=type,
                        forosh=forosh,
                        sood_amaliyati=sood_amaliyati,
                        sood_khales=sood_khales,
                        duration=duration,
                        years=year,
                        month=month
                    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('START CRAWLING')
        crawl()
