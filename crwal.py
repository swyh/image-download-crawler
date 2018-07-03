import urllib.request
from bs4 import BeautifulSoup
import sqlite3

url_list = []
cnt = 0

print("DB를 초기화하고 새로 크롤링할 링크를 DB에 저장합니다.")
start = int(input("링크 저장할 시작 페이지 입력 : "))
end = int(input("링크 저장할 마지막 페이지 입력 : "))


conn = sqlite3.connect('data15.sqlite')
cur = conn.cursor()


cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, state TEXT)''')

cur.execute("delete from Locations")



for i in range(start, end+1):  # page 내에 CT와 MRI tag를 갖고 있는 모든 page들의 url을 url_list에 삽입한다.
    req = urllib.request.Request(
        "https://radiopaedia.org/encyclopaedia/cases/central-nervous-system?page=" + str(i))
    data = urllib.request.urlopen(req).read()
    bs = BeautifulSoup(data, 'html.parser')

    for container in bs.select(".search-result.search-result-case"):  # container별로 분류
        label = container.select(".label.label--grey")
        if (len(label) == 2) and ((label[0].text == "CT" and label[1].text == "MRI") or (
                label[1].text == "CT" and label[0].text == "MRI")):  # CT & MRI

            url = container.get('href')
            url_list.append(url)
            print("[", i, "] list append (", cnt, ") : ", url)
            cur.execute("INSERT INTO Locations (address, state) VALUES (?,'NO') ", (url,))
            conn.commit()

            cnt = cnt + 1

conn.close()

print("저장 완료")