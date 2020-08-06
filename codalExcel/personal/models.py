from bs4 import BeautifulSoup
from django.db import models
from django.utils.html import format_html


TRANS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
ARAB_TRANS = str.maketrans('يك', 'یک')


class Codal(models.Model):
    title = models.CharField(max_length=128)
    symbol = models.CharField(max_length=128)
    company_name = models.CharField(max_length=128)
    filename = models.CharField(max_length=128)
    publish_date_time = models.DateTimeField()

    @property
    def download_link(self):
        return f'{self.filename}'

   # @property
   # def some_value(self):
    #    try:
    #        df = pandas.read_html(self.filename)[0]
    #        sood = int(df.loc[3][2].translate(TRANS).replace(',', ''))
    #        return sood
    #    except Exception:
    #        return 'bad'

    @property
    def some_value(self):
        try:
            with open(self.filename) as f:
                soup = BeautifulSoup(f, 'html.parser')
            element = soup.find(text='سود (زيان) ناخالص')

            print(type(element))
            print(element)

            if not element:
                element = soup.find(text='سود (زيان) ناخالص ')
            sood = element.next.text
            sood = int(sood.translate(TRANS).replace(',', '').strip())
            return sood
        except Exception as e:
            print(e)
            return 'bad'
    @property
    def some_value1(self):
        try:
            with open(self.filename) as f:
                soup = BeautifulSoup(f, 'html.parser')
            element = soup.find(text='سود (زیان) ناخالص ')
            if not element:
                element = soup.find(text='سود (زيان) ناخالص ')
            sood = element.next.text
            element1 = soup.find(text=sood)
            sood1 = element1.next.text
            sood1 = int(sood1.translate(TRANS).replace(',', '').strip())
            return sood1
        except Exception:
            return 'bad'
    @property
    def some_table(self):
        try:
            with open(self.filename) as f:
                soup = BeautifulSoup(f.read().translate(ARAB_TRANS), 'html.parser')
                h3 = soup.find('h3')
                table = h3.find_next('table')
                return format_html(table.prettify())
        except Exception as e:
            return 'bad table'

    def __str__(self):
        return self.symbol
