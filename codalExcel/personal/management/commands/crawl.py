import jdatetime
import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from requests import Timeout

from personal.models import Codal

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


def load_values_from_excel(self, query, query2):
    try:
        f = open(self, encoding='utf-8')
        html_doc = f.read().translate(ARAB_TRANS)
        f.close()

        soup = BeautifulSoup(html_doc, 'html.parser')

        elemenet = soup.find('span', text=query)
        if not elemenet:
            elemenet = soup.find('span', text=query2)
        parent = elemenet.find_parent()
        next_parent = parent.find_next_sibling()
        if '(' in next_parent.text:
            return (-1 * int(next_parent.text.translate(TRANS).replace(',', '').replace(')', '').replace('(', '').strip()))
        else:
            return int(next_parent.text.translate(TRANS).replace(',', '').strip())
    except:
        return "Error"


def load_all_values_from_excel(self, query):
    try:
        f = open(self, encoding='utf-8')
        html_doc = f.read().translate(ARAB_TRANS)
        f.close()

        soup = BeautifulSoup(html_doc, 'html.parser')

        elemenet = soup.find_all('span', text=query)

        for e in elemenet:
            parent = e.find_parent()
            next_parent = parent.find_next_sibling()
            len(next_parent.text)
            if len(next_parent.text) > 1:
                break

        if '(' in next_parent.text:
            return (-1 * int(next_parent.text.translate(TRANS).replace(',', '').replace(')', '').replace('(', '').strip()))
        else:
            return int(next_parent.text.translate(TRANS).replace(',', '').strip())
    except:
        return "Error"

def find_duration(title,type):
    if type == "miyandore":
        return title[42]
    elif type == "salane":
        return 12
    elif type == "mahane":
        return 1
    elif type == "talfigi":
        if "سال " in title:
            return 12
        else:
            return title[48]
    else:
        return 0

def crawl():
    num = 11
    for i in range(10):
        URL = 'https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true' \
              '&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1' \
              '&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={}&Publisher=false&TracingNo=-1&search=false'.format(
            num)
        num = num + 1

        js = requests.get(URL, verify=False).json()

        ls = js['Letters']
        for l in ls:
            if l['HasExcel']:
                print(f"Letter {l['Title']} has excel.")
                print(l)

                url = l['ExcelUrl']
                title = l['Title']
                symbol = l['Symbol']
                company_name = l['CompanyName']
                raw_datetime = l['PublishDateTime']
                fund = isFund(company_name)
                type = whichType(title)
                trans_datetime = raw_datetime.translate(TRANS)
                d = jdatetime.datetime.strptime(trans_datetime, DATE_FORMAT)
                duration = find_duration(title, type)

                print('Downloading ..')
                try:
                    r = requests.get(url, verify=False, timeout=20)
                except Timeout:
                    print(f'Downloading timeout\n{url}')
                    continue
                print('Done.')

                filename = f'media/codal{company_name}.xls'

                with open(filename, 'wb') as f:
                    f.write(r.content)
                forosh = load_values_from_excel(filename, "درآمدهای عملیاتی ", 'درآمدهای عملیاتی')
                sood_amaliyati = load_values_from_excel(filename, 'سود (زیان) عملیاتی ', 'سود (زيان) عملياتي')
                sood_khales = load_all_values_from_excel(filename, 'سود (زیان) خالص ')

                Codal.objects.create(
                    title=title,
                    symbol=symbol,
                    company_name=company_name,
                    filename=filename,
                    publish_date_time=d.togregorian(),
                    fund=fund,
                    type=type,
                    forosh=forosh,
                    sood_amaliyati=sood_amaliyati,
                    sood_khales=sood_khales,
                    duration = duration
                )


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('START CRAWLING')
        crawl()
