from bs4 import BeautifulSoup
import requests
import json

s = requests.session()
headers = {
    'Accept-Language': 'en, ja;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
s.headers.update(headers)

#s.get(url='https://jlptsensei.com/')
#print(s.cookies)
#print(s.headers)

nlevel = 5
page_num = 1
kanji_list = []

def scrape():
    URL = f'https://jlptsensei.com/jlpt-n{nlevel}-kanji-list/page/{page_num}/'
    source = requests.get(URL)
    soup = BeautifulSoup(source.content, 'lxml')
    #print(soup.prettify())

    for element in soup.tbody.find_all('tr', class_='jl-row'):
        kanji = element.find('td', class_='jl-td-k').a.get_text(strip=True)
        onyomi = element.find('td', class_='jl-td-on').a.p.get_text(strip=True)
        kunyomi = element.find('td', class_='jl-td-kun').a.p.get_text(strip=True)
        meaning = element.find('td', class_='jl-td-m').get_text(strip=True)

        kanji_list.append({'kanji':kanji, 'onyomi':onyomi, 'kunyomi':kunyomi, 'meaning':meaning, 'jlpt_level':f'n{nlevel}'})

while page_num != 3:
    scrape()
    while(page_num==1) and (nlevel==5):
        nlevel = nlevel-1
        scrape()
    page_num = page_num+1

#print(kanji_list)

with open('kanji_beginner.json', 'w', encoding='utf-8') as write_json:
    json.dump(kanji_list, write_json, indent=4, ensure_ascii=False)

print('successfully write file!')




#from bs4 import BeautifulSoup
#import requests
#import json