# 축제 데이터 분석 및 시각화 프로젝트

2003년부터 2024년까지의 네이버 뉴스에서 축제 정보를 크롤링하여 분석하고 시각화한 프로젝트

 
## 🗓️ 개발 기간
2024년 10월 ~ 2024년 11월


## 📚 기술 스택
### Environment 
<img src="https://img.shields.io/badge/googlecolab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white">

### Language
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 


## 📌 사용된 주요 라이브러리
- BeautifulSoup: 네이버 뉴스 크롤링
- KoNLPy (Okt): 축제 이름 정제
- Pandas: 데이터 처리 및 분석
- Matplotlib, Seaborn: 시각화
- WordCloud: 워드클라우드 생성


## 📄 주요 분석 내용
**축제 이름 추출 및 정제**

2003년부터 2024년까지의 네이버 뉴스에서 축제와 관련된 기사에서 축제 이름 추출<br> 
이후, KoNLPy의 Okt 모듈을 사용하여 축제 이름을 정제 및 불필요한 단어 제거


## 📊 시각화

**연도별 지역 축제 개수 비교**<br>
연도 별로 지역 축제 개수를 지역별로 비교 가능하도록 시각화
![image](https://github.com/user-attachments/assets/053c34ff-b5c8-4a44-a520-1d65cb44a021)

**월별 지역 축제 개수 비교** <br>
월 별로 축제 개수를 지역별로 비교 가능하도록 시각화
![image](https://github.com/user-attachments/assets/1df2097c-4c5e-4474-8736-716e9dc58612)

**연도 및 월별 축제 분포 히트맵** <br>
연도별로 월별 축제 분포를 히트맵 형태로 시각화 <br>
각 월에 어떤 지역에서 많은 축제가 있었는지를 한눈에 확인 가능 

| 서울 | 인천 | 
| --- | --- | 
| ![image](https://github.com/user-attachments/assets/e1cc71b6-3b30-4d9a-b2c6-c237c030fae4) | ![image](https://github.com/user-attachments/assets/459f2f24-e290-4d31-8e6b-dbeb8e545899) |
| <center>**경기**</center> |
| ![image](https://github.com/user-attachments/assets/575d84ab-b4d1-4222-81ba-a5a093fb5dd3) |


**지역별 워드클라우드** <br>
각 지역별 축제 이름의 워드클라우드 생성 <br>
해당 지역에서 자주 언급된 축제 이름을 시각적으로 확인

![image](https://github.com/user-attachments/assets/162adeb7-64da-4cf6-8992-98867331ef35)

**지역별 단어 빈도 수** <br>
각 지역별로 축제 이름에 사용된 단어의 빈도 시각화

| 서울 | 인천 | 
| --- | --- | 
| ![image](https://github.com/user-attachments/assets/1aabc0c6-6665-4614-9982-8b01ef694dd8) | ![image](https://github.com/user-attachments/assets/34f1b982-c4c3-4906-89ad-824f7762122e) |
| <center>**경기**</center> |
| ![image](https://github.com/user-attachments/assets/99055157-7bdc-484f-94c3-465b1391673c) |

## 결론

**축제 수의 지역별 비교** <br>
 서울이 수도로서 가장 많은 축제가 있을 것으로 예상되었으나, 실제로는 인천과 경기와의 차이가 크지 않았다.

**축제의 월별 분포** <br>
10월은 전반적으로 축제가 가장 많이 진행되는 달로, 다른 달에 비해 축제 수가 높게 나타났습니다.

**축제의 주제**<br> 
문화 관련 축제가 가장 많이 개최되고 있으며, 다양한 문화적 활동이나 행사가 지역 축제에서 중요한 비중을 차지하고 있음을 알 수 있습니다. 이는 각 지역에서 문화적 특성을 반영한 축제들이 활발하게 열리고 있음을 나타냅니다.
