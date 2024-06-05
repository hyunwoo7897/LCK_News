import streamlit as st
import requests
from urllib.parse import quote
import os

# Define the base URL of your FastAPI backend
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Function to make a POST request to create a new item


def create_item(category_choice, subcategory_choice):
    try:
        url = f"{BASE_URL}/items/"
        data = {"category_choice": category_choice, "subcategory_choice": subcategory_choice}
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException:
        st.error("저장된 기사가 없습니다. 기사 크롤링을 진행해주세요.")
        return None




# Function to make a GET request to retrieve an item by ID
def get_item(item_id):
    try:
        url = f"{BASE_URL}/items/{item_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException:
        st.error("저장된 기사가 없습니다. 기사 크롤링을 진행해주세요.")
        return None

# Function to make a GET request to retrieve all items
def get_all_items():
    try:
        url = f"{BASE_URL}/items/"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException:
        return None

# Function to make a GET request to retrieve items by category
def get_items_by_category(category):
    try:
        url = f"{BASE_URL}/items/category/?category={quote(category)}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException:
        st.error("저장된 기사가 없습니다. 기사 크롤링을 진행해주세요.")
        return None

# Function to make a GET request to retrieve items by category and subcategory
def get_items_by_category_and_subcategory(category, subcategory):
    try:
        url = f"{BASE_URL}/items/category/subcategory/?category={quote(category)}&subcategory={quote(subcategory)}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException:
        return None

# Function to display item details
def display_item(item):
    st.write(f"카테고리 : {item['category']} - {item['subcategory']}")
    st.write(f"새 제목  : {item['new_title']}")
    st.write(f"기사 요약: {item['summary']}")
    
    with st.expander("원제목/원문 보기"):
        st.write(f"원제목 : {item['original_title']}")
        st.write(f"기사 원문 : {item['news_body']}")
    
    with st.expander("링크 보기"):
        st.markdown(f"[News Link]({item['news_link']})")

# Custom CSS to style the navigation bar
st.markdown("""
    <style>
    .nav-bar {
        display: flex;
        justify-content: center;
        background-color: #f8f8f8;
        padding: 10px;
        border-bottom: 1px solid #e7e7e7;
        margin-bottom: 10px;
    }
    .nav-bar-item {
        margin: 0 15px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }
    .nav-bar-item:hover {
        color: #007BFF;
    }
    .nav-bar-item.selected {
        color: #FFFFFF;
        background-color: #007BFF;
        padding: 5px 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI elements for creating a new item
st.markdown("<h1 style='text-align: center; color: #FF6347;'>LCK NEWS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4682B4;'>더 정확한 뉴스 전달 매체</h3>", unsafe_allow_html=True)

st.header("1. 요약하고 싶은 기사의 카테고리 선택")
# Navigation bar for Category selection
categories = {
    1: '정치', 2: '경제', 3: '사회', 4: '생활/문화', 5: '세계', 6: 'IT/과학'
}
subcategories = {
    '정치': {1: '대통령실', 2: '국회/정당', 3: '북한', 4: '행정', 5: '국방/외교', 6: '정치일반'},
    '경제': {1: '금융', 2: '증권', 3: '산업/재계', 4: '중기/벤처', 5: '부동산', 6: '글로벌 경제', 7: '생활경제', 8: '경제일반'},
    '사회': {1: '사건사고', 2: '교육', 3: '노동', 4: '언론', 5: '환경', 6: '인권/복지', 7: '식품/의료', 8: '지역', 9: '인물', 10: '사회일반'},
    '생활/문화': {1: '건강정보', 2: '자동차/시승기', 3: '도로/교통', 4: '여행/레저', 5: '음식/맛집', 6: '패션/뷰티', 7: '공연/전시', 8: '책', 9: '종교', 10: '날씨', 11: '생활문화 일반'},
    '세계': {1: '아시아/호주', 2: '미국/중남미', 3: '유럽', 4: '중동/아프리카', 5: '세계 일반'},
    'IT/과학': {1: '모바일', 2: '인터넷/SNS', 3: '통신/뉴미디어', 4: 'IT 일반', 5: '보안/해킹', 6: '컴퓨터', 7: '게임/리뷰', 8: '과학 일반'}
}

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

if 'selected_subcategory' not in st.session_state:
    st.session_state.selected_subcategory = None

if 'selected_retrieve_category' not in st.session_state:
    st.session_state.selected_retrieve_category = None

if 'selected_retrieve_cat_subcat_category' not in st.session_state:
    st.session_state.selected_retrieve_cat_subcat_category = None

if 'selected_retrieve_cat_subcat_subcategory' not in st.session_state:
    st.session_state.selected_retrieve_cat_subcat_subcategory = None

# Display navigation bar for creating items
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
category_columns = st.columns(len(categories))
for i, (key, value) in enumerate(categories.items()):
    with category_columns[i]:
        if st.button(value, key=f"category_{key}"):
            st.session_state.selected_category = key
            st.session_state.selected_subcategory = None  # Reset subcategory when a new category is selected
st.markdown('</div>', unsafe_allow_html=True)

# Display the selected category
if st.session_state.selected_category:
    selected_category_name = categories[st.session_state.selected_category]
    st.markdown(f"<h4>- 카테고리: {selected_category_name}</h4>", unsafe_allow_html=True)
    
    if selected_category_name in subcategories:
        st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
        subcategory_columns = st.columns(len(subcategories[selected_category_name]))
        for i, (key, value) in enumerate(subcategories[selected_category_name].items()):
            with subcategory_columns[i]:
                if st.button(value, key=f"subcategory_{st.session_state.selected_category}_{key}"):
                    st.session_state.selected_subcategory = key
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.selected_subcategory:
            selected_subcategory_name = subcategories[selected_category_name][st.session_state.selected_subcategory]
            st.markdown(f"<h4>- 서브 카테고리: {selected_subcategory_name}</h4>", unsafe_allow_html=True)
            
            if st.button("기사 생성", key="create_button"):
                response = create_item(st.session_state.selected_category, st.session_state.selected_subcategory)
                if response:
                    st.success("기사 생성 완료!")
                    for item in response:
                        display_item(item)

st.header("2. 모든 기사 가져오기")
show_all_items = st.checkbox("모든 기사 보기")
if show_all_items:
    items = get_all_items()
    if items:
        for item in items:
            display_item(item)
            st.write("---")
    else:
        st.error("저장된 기사가 없습니다. 기사 크롤링을 진행해주세요.")

st.header("3. 카테고리별 기사 가져오기")
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
retrieve_category_columns = st.columns(len(categories))
for i, (key, value) in enumerate(categories.items()):
    with retrieve_category_columns[i]:
        if st.button(value, key=f"retrieve_category_{key}"):
            st.session_state.selected_retrieve_category = key
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.selected_retrieve_category:
    retrieve_category_name = categories[st.session_state.selected_retrieve_category]
    st.markdown(f"<h4>- 카테고리: {retrieve_category_name}</h4>", unsafe_allow_html=True)
    if st.button(f"{retrieve_category_name} 기사 가져오기", key=f"retrieve_category_button_{retrieve_category_name}"):
        items = get_items_by_category(retrieve_category_name)
        if items:
            for item in items:
                display_item(item)
                st.write("---")

st.header("4. 세부 카테고리별 기사 가져오기")
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
retrieve_category_columns = st.columns(len(categories))
for i, (key, value) in enumerate(categories.items()):
    with retrieve_category_columns[i]:
        if st.button(value, key=f"retrieve_cat_subcat_category_{key}"):
            st.session_state.selected_retrieve_cat_subcat_category = key
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.selected_retrieve_cat_subcat_category:
    retrieve_category_name = categories[st.session_state.selected_retrieve_cat_subcat_category]
    st.markdown(f"<h4>- 카테고리: {retrieve_category_name}</h4>", unsafe_allow_html=True)
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    subcategory_columns = st.columns(len(subcategories[retrieve_category_name]))
    for i, (key, value) in enumerate(subcategories[retrieve_category_name].items()):
        with subcategory_columns[i]:
            if st.button(value, key=f"retrieve_cat_subcat_subcategory_{retrieve_category_name}_{key}"):
                st.session_state.selected_retrieve_cat_subcat_subcategory = key
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.selected_retrieve_cat_subcat_subcategory:
        subcategory_name = subcategories[retrieve_category_name][st.session_state.selected_retrieve_cat_subcat_subcategory]
        st.markdown(f"<h4>- 서브 카테고리: {subcategory_name}</h4>", unsafe_allow_html=True)
        if st.button(f"{subcategory_name} 기사 가져오기", key=f"retrieve_cat_subcat_subcategory_button_{retrieve_category_name}_{subcategory_name}"):
            items = get_items_by_category_and_subcategory(retrieve_category_name, subcategory_name)
            if items:
                for item in items:
                    display_item(item)
                    st.write("---")
            else:
                st.warning("저장된 기사가 없습니다. 기사 크롤링을 진행해주세요.")
