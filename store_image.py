from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import urllib
import time
import sys
import re
import sqlite3
import shutil
import threading

def create_dir(dir_name): # 폴더가 없으면 생성하고 1 반환, 이미 있으면 0 반환
    if not os.path.exists(dir_name):
        print("create directory : " + dir_name)
        os.makedirs(dir_name)
        return 1
    else:
        return 0

def remove_dir(dir_name):
    shutil.rmtree(dir_name)

def download_web_image(url, num, dir_name): # url을 통해 지정한 폴더에 이미지를 저장하는 함수
    full_name = str(num) + ".jpg"
    print(full_name)

    fullfilename = os.path.join(dir_name, full_name)
    urllib.request.urlretrieve(url, fullfilename)


def download_scroll_images(container, dir_name, title, browser): # 해당 thumbnail container(div) 안에 존재하는 모든 이미지를 스크롤을 내리며 저장
    delay = 5
    sym_sub_title = re.sub('[\/:*?<>|]', '_', title) # 폴더명에 사용할 수 없는 특수문자는 '_'로 변환
    directory = dir_name + "\\" + sym_sub_title
    create_dir(directory)

    print("[start name]" + title)

    if "none" in container.find_element_by_css_selector(".scrollbar").get_attribute("style"): # 스크롤이 없는 경우 : 이미지는 단 한장
        print("scroll none")
        image = container.find_element_by_css_selector("#offline-workflow-study-large-image")
        src = image.get_attribute('src')
        download_web_image(src, "0", directory)
    else: # 스크롤이 있을 경우 : 위 화살표 버튼을 눌러 스크롤이 가장 상단에 위치하도록 함
        up = WebDriverWait(container, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, "up")))
        for i in range(0, 200):
            browser.execute_script('arguments[0].click()', up)

        # 아래 화살표를 down 변수로 사용
        down = WebDriverWait(container, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, "down")))

        temp = ""
        for i in range(0, 200):
            image = container.find_element_by_css_selector("#offline-workflow-study-large-image")
            src = image.get_attribute('src')

            if src == temp: # 같을 경우 같은 이미지으므로 for를 빠져나온다
                break
            temp = src

            download_web_image(src, i, directory) #한장씩 이미지를 다운로드한다
            browser.execute_script('arguments[0].click()', down) # down 버튼을 클릭한다

    print("[success name]" + title)



def download_page_images(page_name, browser): # 해당 페이지에 존재하는 모든 이미지를 저장
    d = rootdir + "\\" + page_name[30:] #url 이용하여 폴더 경로 지정, 앞 30자리는 기존 주소이므로 무시한다.
    if create_dir(d) == 0:
        remove_dir(d)
        create_dir(d)

    time.sleep(20)

    file_path = d + '\\path.txt' # 폴더안에 url주소 텍스트 파일을 저장한다.
    fw = open(file_path, 'w')
    fw.write(page_name)
    fw.close()

    for container in browser.find_elements_by_css_selector(".well.case-section.case-study"): # container(div)별로 분류
        title = container.find_element_by_css_selector(".label.label--grey.spaced-caps.right").text #MRI or CT
        ddir =  d + "\\" + title # 최종경로
        create_dir(ddir)

        print("Search thumbnail")
        if container.find_elements_by_css_selector(".thumbnail"): #thumbnail이 있을 경우
            print("thumbnail")
            for item in container.find_elements_by_css_selector(".thumbnail"):
                span = item.find_element_by_css_selector("span").text
                span_lower = span.lower()   # 소문자로 바꾼다
                if "ax" in span_lower: # thumbnail 중에서 ax를 포함하는 span을 찾는다 (Axial만 찾아 저장하기 위함)
                    browser.execute_script('arguments[0].click()', item)
                    download_scroll_images(container, ddir, span, browser)
        else:   # thumbnail이 없을 경우
            print("not thumbnail")
            span = container.find_elements_by_css_selector(".title")
            span_name = title
            if len(span) != 0: # 개수가 0개 아니면 span 안에 text가 있으므로
                span_name = span[0].text
            download_scroll_images(container, ddir, span_name, browser)
    print("--------------------suceess page!----------------")
    browser.back()




def workPage():
    print("working thread")
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()

    #sem.acquire()
    cur.execute('SELECT * FROM Locations')  # DB query문 실행,timeout=1
    #sem.release()

    try:
        browser = webdriver.Chrome()
        count = 0

        for row in cur:
            count = count + 1
            current = row[0]
            state = row[1]

            sem.acquire()  # critical section----------------------------------------
            if state != "NO" or links[count] == 1:
                sem.release()
                continue
            links[count] = 1
            sem.release()  # --------------------------------------------------------

            print(current, "1")
            cur.execute("UPDATE Locations SET state = 'ING' WHERE address = ?", (current,))
            print(current, "2")

            conn.commit()
            print(current, "3")

            url = "https://radiopaedia.org" + current  # row[1]은 address에 대한 json 값
            print("--CT and MRI-- browser move---")
            print(url)
            browser.get(url)
            download_page_images(url, browser)

            cur.execute("UPDATE Locations SET state = 'YES' WHERE address = ?", (current,))
            conn.commit()

        print("--------------------suceess finish!----------------")
    except sqlite3.OperationalError:
        print("database locked")
    except Exception  as e:
        cur.execute("UPDATE Locations SET state = 'NO' WHERE address = ?", (current,))
        conn.commit()

        print(e)
        print("exit")

    cur.close()


#-------------------------------------------------------------------------------------------

rootdir = "C:\\radiopaedia" #저장 위치
create_dir(rootdir) # 폴더 생성


links = [0]*10000 # 최대 링크 10000개까지 가능
threads = []
sem = threading.Lock()

print("thread의 개수를 입력하세요 (클수록 빠르지만 컴퓨터 자원이 많이 필요합니다.")
thread_count = int(input("입력 :"))

for num in range(1, thread_count+1):
    thread = threading.Thread(target=workPage)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
