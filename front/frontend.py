import streamlit as st
import requests

# Define the base URL of your FastAPI backend
BASE_URL = "http://localhost:8000"

# Function to make a POST request to create a new item
def create_item(category_choice, subcategory_choice):
    try:
        url = f"{BASE_URL}/items/"
        data = {"category_choice": category_choice, "subcategory_choice": subcategory_choice}
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to create item: {str(e)}")
        return None

# Function to make a GET request to retrieve an item by ID
def get_item(item_id):
    try:
        url = f"{BASE_URL}/items/{item_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to retrieve item: {str(e)}")
        return None

# Streamlit UI elements for creating a new item
st.title("FastAPI Backend with Streamlit Frontend")
st.header("Create a New Item")

# Category and Subcategory selection
categories = {
    1: '정치', 2: '경제', 3: '사회', 4: '생활/문화', 5: '세계', 6: 'IT/과학'
}
selected_category = st.selectbox("Select Category", options=list(categories.keys()), format_func=lambda x: categories[x])

subcategories = {
    '정치': {1: '대통령실', 2: '국회/정당', 3: '북한', 4: '행정', 5: '국방/외교', 6: '정치일반'},
    '경제': {1: '금융', 2: '증권', 3: '산업/재계', 4: '중기/벤처', 5: '부동산', 6: '글로벌 경제', 7: '생활경제', 8: '경제일반'},
    '사회': {1: '사건사고', 2: '교육', 3: '노동', 4: '언론', 5: '환경', 6: '인권/복지', 7: '식품/의료', 8: '지역', 9: '인물', 10: '사회일반'},
    '생활/문화': {1: '건강정보', 2: '자동차/시승기', 3: '도로/교통', 4: '여행/레저', 5: '음식/맛집', 6: '패션/뷰티', 7: '공연/전시', 8: '책', 9: '종교', 10: '날씨', 11: '생활문화 일반'},
    '세계': {1: '아시아/호주', 2: '미국/중남미', 3: '유럽', 4: '중동/아프리카', 5: '세계 일반'},
    'IT/과학': {1: '모바일', 2: '인터넷/SNS', 3: '통신/뉴미디어', 4: 'IT 일반', 5: '보안/해킹', 6: '컴퓨터', 7: '게임/리뷰', 8: '과학 일반'}
}
selected_subcategory = st.selectbox("Select Subcategory", options=list(subcategories[categories[selected_category]].keys()), format_func=lambda x: subcategories[categories[selected_category]][x])

if st.button("Create"):
    response = create_item(selected_category, selected_subcategory)
    if response:
        st.success("Items created successfully!")
        for item in response:
            st.write(f"Item ID: {item['id']}")
            """st.write(f"Category: {item['category']}")
            st.write(f"Subcategory: {item['subcategory']}")"""
            st.write(f"Original Title: {item['original_title']}")
            st.write(f"New Title: {item['new_title']}")
            st.write(f"Summary: {item['summary']}")
            st.write(f"News Link: {item['news_link']}")
            st.write(f"News Body: {item['news_body']}")
            st.write("---")
    else:
        st.error("Failed to create item")

st.header("Retrieve an Item by ID")

item_id = st.number_input("Enter Item ID", min_value=1, step=1)

if st.button("Retrieve"):
    item = get_item(item_id)
    if item:
        st.write(f"Item ID: {item['id']}")
        st.write(f"Category: {item['category']}")
        """st.write(f"Subcategory: {item['subcategory']}")
        st.write(f"Original Title: {item['original_title']}")"""
        st.write(f"New Title: {item['new_title']}")
        st.write(f"Summary: {item['summary']}")
        st.write(f"News Link: {item['news_link']}")
        st.write(f"News Body: {item['news_body']}")
    else:
        st.error("Failed to retrieve item")