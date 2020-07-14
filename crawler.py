import requests


requests.packages.urllib3.disable_warnings()

num = 1
while num < 2:
    x = requests.get('https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Chi'
                     'lds=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-'
                     '1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={}&Publisher=false'
                     '&TracingNo=-1&search=false'.format(num), verify=False)
    num = num + 1
    js = x.json()
    ls = js['Letters']

    for a in ls:
       if a['HasExcel'] == True:
           print("==============================================")
           print(a)
           url = a['ExcelUrl']
           title = a['Title']
           CompanyName = a['CompanyName']
           Symbol = a['Symbol']
           PublishDateTime = a['PublishDateTime']
           print(title , CompanyName)
           r = requests.get(url, verify=False)

           with open(f'codal{Symbol}.xlsx', 'wb') as f:
               f.write(r.content)



       if a['HasHtml'] == True & a['HasExcel'] == True:
           print("==============================================")
           url = a['Url']
           url = "https://www.codal.ir/"+ url
           print(url)
           r = requests.get(url,verify = False)