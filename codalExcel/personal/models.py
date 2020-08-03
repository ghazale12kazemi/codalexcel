from bs4 import BeautifulSoup
from django.db import models
import pandas


TRANS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')


class Codal(models.Model):
    title = models.CharField(max_length=128)
    symbol = models.CharField(max_length=128)
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
            element = soup.find(text='سود (زیان) ناخالص ')
            if not element:
                element = soup.find(text='سود (زيان) ناخالص ')
            sood1 = element.next.text
            sood1 = int(sood1.translate(TRANS).replace(',', '').strip())
            return sood1
        except Exception:
            return 'bad'

    def __str__(self):
        return self.symbol
