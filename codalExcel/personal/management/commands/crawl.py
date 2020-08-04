import jdatetime
import requests
from django.core.management import BaseCommand
from bs4 import BeautifulSoup

from personal.models import Codal

requests.packages.urllib3.disable_warnings()

URL = 'https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true' \
      '&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1' \
      '&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=-1&search=fals'

j = requests.get(URL, verify=False).json()
print(j.keys())

TRANS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
ARAB_TRANS = str.maketrans('يك', 'یک')
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


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
            trans_datetime = raw_datetime.translate(TRANS)
            publish_date_time = jdatetime.datetime.strptime(trans_datetime, DATE_FORMAT)

            #=======
            d = jdatetime.datetime.strptime(publish_date_time, "%d-%b-%Y")
            desired_output = '{d.day} {d.month} {d.year}'.format(d=d)
            publish_date_time = jdatetime.datetime.strftime(d, "%d %m %Y")

            print('Downloading ..')
            r = requests.get(url, verify=False)
            print('Done.')

            filename = f'media/codal{company_name}.xls'

            with open(filename, 'wb') as f:
                f.write(r.content)

            Codal.objects.create(
                title=title,
                symbol=symbol,
                filename=filename,
                publish_date_time=publish_date_time.togregorian()
            )


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('START CRAWLING')
        crawl()
