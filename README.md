## Crawler
교육 웹 리소스인 Radiopaedia에서 image를 조건에 맞게 자동으로 다운 받을 수 있는 web crawler입니다.
python code로 작성하였고, web framework인 Selenium을 이용하였습니다.

### Selenium이란? 
- 웹앱을 테스트하는 framework
- webdriver api를 통해 운영체제에 설치된 chrome 등의 브라우저를 제어함

### selenium을 선택한 이유는?
- js로 렌더링이 완료된 후의 dom 결과물에 대해 접근이 가능
- radiopaedia의 사진은 scroll을 내리며 사진을 동적으로 가져와야했기 때문에 selenium이 적합

Radiopaedia : https://radiopaedia.org
