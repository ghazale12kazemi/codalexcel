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
    fund = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    sood = models.CharField(max_length=128)
    sood1 = models.CharField(max_length=128)

    @property
    def download_link(self):
        return f'{self.filename}'

    @property
    def some_value(self):
        try:
            f = open(self.filename, encoding='utf-8')
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

    @property
    def some_value1(self):
        try:
            f = open(self.filename, encoding='utf-8')
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

    # @property
    # def some_value(self):
    #    try:
    #        df = pandas.read_html(self.filename)[0]
    #        sood = int(df.loc[3][2].translate(TRANS).replace(',', ''))
    #        return sood
    #    except Exception:
    #        return 'bad'

    def __str__(self):
        return self.symbol
