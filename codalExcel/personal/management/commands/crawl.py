import jdatetime
import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

from personal.models import Codal

requests.packages.urllib3.disable_warnings()

URL = 'https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true' \
      '&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1' \
      '&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=12&Publisher=false&TracingNo=-1&search=false'

j = requests.get(URL, verify=False).json()
print(j.keys())

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
    elif "اطلاعات و صورت‌های مالی میاندوره‌ای" in title:
        return "miyandore"
    elif "تلفیقی" in title:
        return "talfigi"
    else:
        return "unknown"


def some_value(self):
    try:
        f = open(self, encoding='utf-8')
        html_doc = f.read()
        f.close()

        query = "سود (زيان) ناخالص "
        query2 = "سود (زیان) ناخالص "

        soup = BeautifulSoup(html_doc, 'html.parser')

        elemenet = soup.find('span', text=query)
        if not elemenet:
            elemenet = soup.find('span', text=query2)
        parent = elemenet.find_parent()
        next_parent = parent.find_next_sibling()
        return int(next_parent.text.translate(TRANS).replace(',', '').strip())
    except:
        return "Error in sood"


def some_value1(self):
    try:
        f = open(self, encoding='utf-8')
        html_doc = f.read()
        f.close()

        query = "سود (زيان) ناخالص "
        query2 = "سود (زیان) ناخالص "

        soup = BeautifulSoup(html_doc, 'html.parser')

        elemenet = soup.find('span', text=query)
        if not elemenet:
            elemenet = soup.find('span', text=query2)
        parent = elemenet.find_parent()
        next_parent = parent.find_next_sibling()
        next_next_parent = next_parent.find_next_sibling()
        return int(next_next_parent.text.translate(TRANS).replace(',', '').strip())
    except:
        return "Error in sood"


def crawl():
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

            print('Downloading ..')
            r = requests.get(url, verify=False)
            print('Done.')

            filename = f'media/codal{company_name}.xls'

            with open(filename, 'wb') as f:
                f.write(r.content)
            sood = some_value(filename)
            sood1 = some_value1(filename)

            Codal.objects.create(
                title=title,
                symbol=symbol,
                company_name=company_name,
                filename=filename,
                publish_date_time=d.togregorian(),
                fund=fund,
                type=type,
                sood=sood,
                sood1=sood1
            )


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('START CRAWLING')
        crawl()
