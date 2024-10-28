import os
import sys
import urllib.request
import datetime
import time
import json


# client id, pw를 JSON 파일에서 읽어오기
def load_client_info(filename='naver_client.json'):
    with open(filename, 'r') as f:
        credentials = json.load(f)
    return credentials['client_id'], credentials['client_secret']


# client 정보 로드
client_id, client_pw = load_client_info()


def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_pw)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)


def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d')

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description, 'link': link, 'pDate': pDate})
    return


def main():
    node = 'news'
    topic = "축제"

    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, topic, 1, 100)
    total = jsonResponse['total']

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)

        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, topic, start, 100)

    print('전체 검색 : %d 건' % total)

    output_file = '%s_naver_%s.json' % (topic, node)

    with open(output_file, 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    print('데이터 크롤링 완료' % (topic, node))


if __name__ == '__main__':
    main()
