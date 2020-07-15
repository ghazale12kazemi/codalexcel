from datetime import timezone

import requests

requests.packages.urllib3.disable_warnings()


    # num = 1
    # while num < 2:
    #    x = requests.get('https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Chi'
    #                     'lds=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-'
    #                     '1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={}&Publisher=false'
    #                     '&TracingNo=-1&search=false'.format(num), verify=False)

    #    num = num + 1
class Codal_crawl(object):
#    def __init__(self, symbol, url, title, company_name, publish_date_time, codal_excel):
#        self.symbol = symbol
#        self.url = url
#        self.title = title
#        self.company_name = company_name
#        self.publish_date_time = publish_date_time
#        self.codal_excel = codal_excel

    def __init__(self,url):
        self.url = url

    def get_html(self, url):
        try:
            html = requests.get(url, verify=False)
        except Exception as e:
            print(e)
            return ""
        return html.json()

    x = requests.get('https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Chi'
                     'lds=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-'
                     '1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false'
                     '&TracingNo=-1&search=false', verify=False)



    js = x.json()
    ls = js['Letters']

    for a in ls:
        if a['HasExcel'] == True:
            print("==============================================")
            print(a)
            url = a['ExcelUrl']
            title = a['Title']
            company_name = a['CompanyName']
            symbol = a['Symbol']
            publish_date_time = a['PublishDateTime']
            print(title, company_name)
            r = requests.get(url, verify=False)

            with open(f'codal{symbol}.xls', 'wb') as f:
                f.write(r.content)

        if a['HasHtml'] == True & a['HasExcel'] == True:
            print("==============================================")
            url = a['Url']
            url = "https://www.codal.ir/" + url
            print(url)
            r = requests.get(url, verify=False)
