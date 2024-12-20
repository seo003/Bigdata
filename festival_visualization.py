# -*- coding: utf-8 -*-
"""festival_visualization_최종.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vkwup1Ka8WaXOj4-lrUKDnJFpLldze8B
"""

!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

import matplotlib.pyplot as plt

plt.rc('font', family='NanumBarunGothic')

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import seaborn as sns
import matplotlib.font_manager as fm

"""csv에서 읽어들여 필요한 정보만 저장 후 딕셔너리에 저장"""

start_year = 2003
end_year = 2024

seoul = pd.read_csv('seoul_festivals.csv')[['year', 'month', 'refined_festival_name']]
incheon = pd.read_csv('incheon_festivals.csv')[['year', 'month', 'refined_festival_name']]
gyeonggi = pd.read_csv('gyeonggi_festivals.csv')[['year', 'month', 'refined_festival_name']]
df_dict = {'서울': seoul, '인천': incheon, '경기': gyeonggi}

for region, df in df_dict.items():
    print(f"================={region}=================")
    print(df.head())

"""축제 만 들어있으면 삭제"""

for region, df in df_dict.items():
    df_dict[region] = df[df['refined_festival_name'] != '축제'].reset_index(drop=True)

    print(f"================={region}=================")
    print(df_dict[region].head())

# 각 지역에 대해 데이터 시각화
plt.figure(figsize=(8, 5))

# 각 지역에 대한 선 그래프 추가
for region, df in df_dict.items():
    yearly_counts = df['year'].value_counts().sort_index()

    # 시작 연도와 끝 연도 정의
    start_year = yearly_counts.index.min()
    end_year = yearly_counts.index.max()

    # 선 그래프 그리기
    plt.plot(yearly_counts.index, yearly_counts.values, marker='o', label=region)

# 제목, 라벨 설정
plt.title("연도별 축제 개수 비교 (지역별)", fontsize=14)
plt.xlabel("년도", fontsize=12)
plt.ylabel("축제 개수", fontsize=12)

# x축, y축 설정
plt.xticks(range(start_year, end_year + 1, 2), rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 범례 추가
plt.legend(title="지역", fontsize=10)

# 그래프 표시
plt.tight_layout()
plt.show()

# 월별 축제 분포 시각화
plt.figure(figsize=(8, 5))

# 각 지역에 대한 선 그래프 추가
for region, df in df_dict.items():
    monthly_counts = df['month'].value_counts().sort_index()

    # 월별 축제 개수를 리스트로 저장
    monthly_counts_list = [monthly_counts.get(month, 0) for month in range(1, 13)]

    # 선 그래프 그리기
    plt.plot(range(1, 13), monthly_counts_list, marker='o', label=region)

# 제목, 라벨 설정
plt.title("월별 축제 분포 비교 (지역별)", fontsize=14)
plt.xlabel("월", fontsize=12)
plt.ylabel("축제 개수", fontsize=12)

# x축, y축 설정
plt.xticks(range(1, 13))
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 범례 추가
plt.legend(title="지역", fontsize=10)

# 그래프 표시
plt.tight_layout()
plt.show()

for region, df in df_dict.items():
    heatmap_data = pd.crosstab(df['year'], df['month'])
    plt.figure(figsize=(6, 3))
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=False, cbar=True)
    plt.title(f"{region} - 연도 및 월별 축제 분포 히트맵", fontsize=14)
    plt.xlabel("월", fontsize=12)
    plt.ylabel("년도", fontsize=12)
    plt.show()

# NanumBarunGothic 폰트 경로 설정 (필요시 경로 수정)
font_path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'

# 워드클라우드 생성
plt.figure(figsize=(18, 6))  # 전체 그래프의 크기 설정

for idx, (region, df) in enumerate(df_dict.items()):
    # '축제', '박람회', '콘테스트' 단어를 제외한 텍스트 생성
    words = ' '.join(df['refined_festival_name'].dropna())
    words = words.replace('축제', '').replace('박람회', '').replace('콘테스트', '')

    # 축제 이름의 빈도수 계산
    word_freq = Counter(words.split())

    # 서브플롯 생성 (가로로 나열)
    plt.subplot(1, len(df_dict), idx + 1)
    wordcloud = WordCloud(font_path=font_path, background_color="white", width=800, height=600).generate_from_frequencies(word_freq)

    # 워드클라우드 시각화
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"{region} - 축제 워드클라우드", fontsize=16)

# 워드클라우드 출력
plt.tight_layout()
plt.show()

from collections import Counter
import matplotlib.pyplot as plt

# 텍스트 데이터 전처리
def preprocess_text(dataframe):
    text_data = ' '.join(dataframe['refined_festival_name'].dropna())
    text_data = text_data.replace('축제', '')  # '축제' 단어 제거
    tokens = text_data.split()  # 간단히 단어 단위로 분리
    return tokens

top_n = 15
for region, df in df_dict.items():
    tokens = preprocess_text(df)
    word_counts = Counter(tokens).most_common(top_n)
    words, counts = zip(*word_counts)

    plt.figure(figsize=(8, 4))
    plt.bar(words, counts, color='lightblue')
    plt.title(f"{region} - 상위 {top_n} 단어 빈도수", fontsize=14)
    plt.xlabel("단어", fontsize=12)
    plt.ylabel("빈도 수", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()