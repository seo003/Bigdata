# -*- coding: utf-8 -*-
"""festival_analyze.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sALKPWsbmFRriuhEoHPdu-9hDhWWfJiF
"""

!pip install konlpy

import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
from konlpy.tag import Okt

# 축제 이름 추출
def get_festival_name(region_list):
    festival_dict = {}  # 지역별로 축제 목록 저장

    # 축제 명칭 패턴 정의
    pattern = re.compile(r'(?<!\S)([가-힣\s]+)(축제|박람회|콘테스트)(?!\S)')

    def process_region(region):
        filename = f"{region}_2003_2024_news.csv"
        region_festivals = []

        try:
            # pandas로 CSV 파일 읽기
            cases = pd.read_csv(filename, encoding='utf8')
            for _, row in cases.iterrows():
                try:
                    year = row['year']
                    month = row['month']
                    title = row.get('title', '')
                    description = row.get('description', '')

                    # 축제 찾기
                    match = pattern.search(title)
                    if not match:
                        match = pattern.search(description)

                    if match:
                        festival_name = match.group(0).strip()
                        region_festivals.append((year, month, festival_name))
                        print(f"추출된 축제 이름: {festival_name}")
                    else:
                        print("축제 이름을 찾을 수 없습니다.")
                except KeyError:
                    print("필요한 키가 없습니다. 무시하고 진행합니다.")
        except FileNotFoundError:
            print(f"{filename} 파일이 없습니다.")
            return region, region_festivals

        print(f"{region} 지역 축제 이름 {len(region_festivals)}개 추출 완료")
        return region, region_festivals

    # 병렬로 각 지역 처리
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_region, region_list)

    for region, festivals in results:
        if festivals:
            festival_dict[region] = festivals

    # 추출한 축제 이름 출력
    print("축제 이름 추출 결과:", festival_dict)
    return festival_dict


# 형태소 분석 및 정제
def refine_festival_name(festival_name):
    # '및' 이후 삭제
    if '및' in festival_name:
        festival_name = festival_name.split('및', 1)[0].strip()

    # 형태소 분석 및 명사 추출
    okt = Okt()
    pos_tags = okt.pos(festival_name)
    filtered_name = []
    found_noun = False

    for word, pos in reversed(pos_tags):
        if pos == 'Noun':
            filtered_name.insert(0, word)
            found_noun = True
        elif found_noun:
            break

    # 정제된 축제 이름만 반환 (축제는 제외)
    final_name = " ".join(filtered_name)

    return final_name


# CSV로 저장하지 않고 DataFrame으로 처리
def analyze_festival_names(festival_dict):
    refined_dict = {}  # 정제된 축제 이름을 저장할 딕셔너리

    for region, festivals in festival_dict.items():
        # pandas DataFrame으로 변환
        df = pd.DataFrame(festivals, columns=['year', 'month', 'festival_name'])

        # 정제된 축제 이름 컬럼 생성
        df['refined_festival_name'] = df['festival_name'].apply(refine_festival_name)

        # 정제된 DataFrame을 딕셔너리에 저장
        refined_dict[region] = df[['year', 'month', 'festival_name', 'refined_festival_name']]

        print(f"{region}_festival.csv의 정제 결과:")
        print(refined_dict[region].head())  # 정제된 축제 이름의 첫 5개 출력

    return refined_dict


# 메인 함수
if __name__ == '__main__':
    regions = ['seoul', 'incheon', 'gyeonggi']

    # 축제 이름 추출
    festival_dict = get_festival_name(regions)

    # 축제 이름을 정제하여 DataFrame으로 반환
    refined_festivals = analyze_festival_names(festival_dict)

    # DataFrame을 CSV로 저장
    for region, df_refined in refined_festivals.items():
        refined_filename = f"{region}_festivals.csv"
        df_refined.to_csv(refined_filename, index=False, encoding='utf-8')
        print(f"정제된 축제 이름이 '{refined_filename}'에 저장되었습니다.")