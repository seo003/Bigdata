import urllib.request
import datetime
import json

# client id, pw를 JSON 파일에서 읽어오기
def load_client_info(filename='naver_client.json'):
    with open(filename, 'r') as f:
        credentials = json.load(f)
    return credentials['client_id'], credentials['client_secret']


# 네이버 뉴스 API 호출 및 데이터 가져오기
def get_naver_search(client_id, client_secret, query, start=1, display=100):
    url = f"https://openapi.naver.com/v1/search/news.json?query={urllib.parse.quote(query)}&start={start}&display={display}"
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        # API 요청 전송 및 응답 확인
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print(f"[{datetime.datetime.now()}] Url Request Success")
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        # 오류
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")
        return None


# 뉴스 데이터 추출 및 저장
def fetch_and_save_news(client_id, client_secret, region):
    query = f"{region} 축제"
    json_result = []
    start, cnt = 1, 0

    while True:
        response = get_naver_search(client_id, client_secret, query, start)
        if response is None or response['display'] == 0:
            break  # 데이터가 없으면 반복 종료

        for post in response['items']:
          if cnt >= 500:  # 500개만 저장
                break
          cnt += 1
          json_result.append({
                'cnt': cnt,
                'title': post['title'],
                'description': post['description']
          })

        start += response['display']

    # JSON 파일로 저장
    region_file_map = {
        "인천": "incheon",
        "서울": "seoul",
        "경기": "gyeonggi"
    }
    output_file = f"{region_file_map[region]}_naver_news.json"
    with open(output_file, 'w', encoding='utf8') as outfile:
        json.dump(json_result, outfile, indent=4, ensure_ascii=False)
    print(f"{query} 크롤링 완료")


# 메인 함수
if __name__ == '__main__':
    client_id, client_secret = load_client_info()
    regions = ["인천", "서울", "경기"]
    for region in regions:
        fetch_and_save_news(client_id, client_secret, region)