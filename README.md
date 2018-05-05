## Crawler
교육 웹 리소스인 [Radiopaedia](https://radiopaedia.org/cases/)에서 image를 조건에 맞게 자동으로 다운 받을 수 있는 web crawler

### Functionality
- 아래 조건에 맞는 사진을 저장 
    - Lable : CT & MRI
    - File name : Axial
 
### Requirements
- Fast network speed
- Python 3.5
- Selenium
    - 웹앱을 테스트하는 framework
    - webdriver api를 통해 운영체제에 설치된 chrome 등의 브라우저를 제어
    - js로 렌더링이 완료된 후의 dom 결과물에 대해 접근이 가능

### Guide
- download_list.py
    - 실행 시 사진을 저장할 페이지를 매개변수로 시작 페이지, 마지막 페이지를 입력
        - ex) python list_crawler.py 1 10 (1 ~ 10page까지의 모든 사진을 저장합니다)
    - code내에 입력 된 rootdir에 사진이 분류되어 저장

- download_page.py
    - 매개변수로 크롤링할 page 주소를 입력
