import requests
from bs4 import BeautifulSoup
import pandas as pd
import openai
import os

# OpenAI API key 설정
openai.api_key = os.getenv('OPENAI_API_KEY')
#openai.api_key ='sk-proj-OYPQSYErvElP3Hkl7vqhT3BlbkFJZgKADqTwdsEoqGXBqwrP'

# 카테고리와 세부 카테고리 매핑
categories = {
    1: ('정치', '100'),
    2: ('경제', '101'),
    3: ('사회', '102'),
    4: ('생활/문화', '103'),
    5: ('세계', '104'),
    6: ('IT/과학', '105')
}

subcategories = {
    '정치': {
        1: ('대통령실', '264'),
        2: ('국회/정당', '265'),
        3: ('북한', '268'),
        4: ('행정', '266'),
        5: ('국방/외교', '267'),
        6: ('정치일반', '269')
    },
    '경제': {
        1: ('금융', '259'),
        2: ('증권', '258'),
        3: ('산업/재계', '261'),
        4: ('중기/벤처', '771'),
        5: ('부동산', '260'),
        6: ('글로벌 경제', '262'),
        7: ('생활경제', '310'),
        8: ('경제일반', '263')
    },
    '사회': {
        1: ('사건사고', '249'),
        2: ('교육', '250'),
        3: ('노동', '251'),
        4: ('언론', '254'),
        5: ('환경', '252'),
        6: ('인권/복지', '59b'),
        7: ('식품/의료', '255'),
        8: ('지역', '256'),
        9: ('인물', '276'),
        10: ('사회일반', '257')
    },
    '생활/문화': {
        1: ('건강정보', '241'),
        2: ('자동차/시승기', '239'),
        3: ('도로/교통', '240'),
        4: ('여행/레저', '237'),
        5: ('음식/맛집', '238'),
        6: ('패션/뷰티', '376'),
        7: ('공연/전시', '242'),
        8: ('책', '243'),
        9: ('종교', '244'),
        10: ('날씨', '248'),
        11: ('생활문화 일반', '245')
    },
    '세계': {
        1: ('아시아/호주', '231'),
        2: ('미국/중남미', '232'),
        3: ('유럽', '233'),
        4: ('중동/아프리카', '234'),
        5: ('세계 일반', '322')
    },
    'IT/과학': {
        1: ('모바일', '731'),
        2: ('인터넷/SNS', '226'),
        3: ('통신/뉴미디어', '227'),
        4: ('IT 일반', '230'),
        5: ('보안/해킹', '732'),
        6: ('컴퓨터', '283'),
        7: ('게임/리뷰', '229'),
        8: ('과학 일반', '228')
    }
}

def converter(category_choice, subcategory_choice):
    category_name, category_code = categories[category_choice]
    subcategory_name, subcategory_code = subcategories[category_name][subcategory_choice]

    # URL 생성
    url = f'https://news.naver.com/breakingnews/section/{category_code}/{subcategory_code}'
    header = {"User-Agent": "Mozilla/5.0"}

    print(url)

    # HTTP GET 요청
    html = requests.get(url, headers=header)

    # HTML 파싱
    soup = BeautifulSoup(html.text, 'html.parser')

    # 뉴스 제목과 링크를 저장할 리스트
    news_list = []

    # 첫 번째 섹션 뉴스 제목과 링크 추출
    for i in range(1, 7):
        elements = soup.select(f'#newsct > div.section_latest > div > div.section_latest_article._CONTENT_LIST._PERSIST_META > div:nth-child(1) > ul > li:nth-of-type({i}) > div > div > div.sa_text > a')
        if elements:
            title = elements[0].select_one('strong').text.strip()
            link = elements[0].get('href')
            news_list.append((title, link))

    def extract_news_content(url):
        html = requests.get(url, headers=header)
        soup = BeautifulSoup(html.text, 'html.parser')
        content_div = soup.select_one('#dic_area')
        if content_div:
            return content_div.text.strip()
        else:
            return "본문을 찾을 수 없습니다."

    # 뉴스 본문 요약 함수 (한글)
    def summarize_text(text):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 조수입니다."},
                {"role": "user", "content": f"다음 기사를 요약해 주세요:\n\n{text}\n\n요약:"}
            ],
            max_tokens=150,
            temperature=0.5
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary

    # 뉴스 제목 생성 함수 (한글)
    def generate_title(text):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 조수입니다."},
                {"role": "user", "content": f"다음 기사를 바탕으로 제목을 생성해 주세요:\n\n{text}\n\n제목:"}
            ],
            max_tokens=50,
            temperature=0.5
        )
        title = response['choices'][0]['message']['content'].strip()
        return title

    # 뉴스 데이터를 저장할 리스트
    data = []

    # 추출된 뉴스 제목, 링크와 본문 저장
    for title, link in news_list:
        content = extract_news_content(link)
        if content != "본문을 찾을 수 없습니다." and content.strip() != "":
            summary = summarize_text(content)
            generated_title = generate_title(content)
        else:
            summary = "요약을 할 수 없습니다."
            generated_title = "제목을 생성할 수 없습니다."
        data.append({
            'original_title': title,
            'link': link,
            'content': content,
            'summary': summary,
            'generated_title': generated_title
        })
    return data
