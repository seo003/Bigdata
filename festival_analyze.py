import json
import re
from konlpy.tag import Okt

def get_festival_name(region_list):
    festival_dict = {}  # 지역별로 축제 목록을 저장할 딕셔너리

    for region in region_list:
        filename = f"{region}_naver_news.json"

        # JSON 파일 읽기
        with open(filename, 'r', encoding='utf8') as f:
            data = json.load(f)

        # 축제 명칭 패턴 정의
        pattern = re.compile(r'(?<!\S)([가-힣]+(?: [가-힣]+)?) (축제|박람회|콘테스트)(?!\S)')

        # 축제 목록 저장 리스트
        festival_names_list = []

        for item in data:
            title = item['title']
            description = item['description']

            # title에서 <b> 태그 제거
            title = re.sub(r'<b>|</b>', '', title)

            # title에서 축제 찾기
            match = pattern.search(title)
            if match:
                festival_name = match.group(0).strip()
                if festival_name not in festival_names_list:  # 리스트에 없는 경우에만 추가
                    festival_names_list.append(festival_name)
                continue

            # title에 축제가 없으면 description에서 찾기
            description_clean = re.sub(r'<b>(.*?)<\/b>', r'\1', description)
            match = pattern.search(description_clean)
            if match:
                festival_name = match.group(0).strip()
                if festival_name not in festival_names_list:  # 리스트에 없는 경우에만 추가
                    festival_names_list.append(festival_name)

        festival_dict[region] = festival_names_list  # 지역별 축제 목록 저장

    return festival_dict

def analyze_festival_name(festival_dict):
    # 형태소 분석기
    okt = Okt()

    # 결과를 저장할 딕셔너리
    analyzed_festivals = {}

    # 지역별 축제 목록 분석
    for region, festivals in festival_dict.items():
        analyzed_festivals[region] = []  # 각 지역에 대한 축제 이름 리스트

        for festival_name in festivals:
            # '및' 다음부터의 문자열만 저장
            if '및' in festival_name:
                festival_name = festival_name.split('및', 1)[1].strip()

            # 형태소 분석 및 품사 태깅
            pos_tags = okt.pos(festival_name)

            # 마지막에 나오는 명사 구만 남기기
            filtered_name = []
            found_noun = False
            for word, pos in reversed(pos_tags):
                if pos == 'Noun':
                    filtered_name.insert(0, word)  # 명사를 만나면 filtered_name에 추가
                    found_noun = True
                elif found_noun:
                    # 명사 이후 수식어는 무시
                    break

            # 축제 이름이 '축제' 하나만 남은 경우 제외
            final_name = " ".join(filtered_name)
            if final_name and final_name not in ["축제", "박람회", "콘테스트"]:
                # 중복 체크
                if final_name not in analyzed_festivals[region]:
                    analyzed_festivals[region].append(final_name)

    return analyzed_festivals

# 메인 함수
if __name__ == '__main__':
    region_list = ['seoul', 'incheon', 'gyeonggi']
    festival_dict = get_festival_name(region_list)
    analyze_festival = analyze_festival_name(festival_dict)
    for key, value in festival_dict.items():
        print(f"{key}")
        for v in value:
            print(f"{v}")
    print("="*100)
    for key, value in analyze_festival.items():
        print(f"{key}")
        print("-"*10)
        for v in value:
            print(f"{v}")