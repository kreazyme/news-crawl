import requests
from bs4 import BeautifulSoup
import requests
import json

def CrawlVNExpress(article_url):
    url = article_url
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.title.string
    print("Tiêu đề bài báo:", title)
    article_content = soup.find("article", class_="fck_detail")
    if article_content:
            paragraphs = article_content.find_all("p")
            article_text = "\n".join([p.get_text() for p in paragraphs])
            print("Nội dung bài báo:\n", article_text)
    else:
            print("Không tìm thấy nội dung bài báo.")
    image_tags = soup.find_all("img", itemprop="contentUrl")
    image_urls = [img.get("data-src") for img in image_tags]
    for idx, image_url in enumerate(image_urls):
            print(f"Hình ảnh {idx + 1}: {image_url}")
    return article_text,image_urls

def TTS(text):
    url = 'https://api.fpt.ai/hmi/tts/v5'
    api_key = 'EtXKMIjaJcF1K5O7ELmYUFZl55KIi2uW'
    headers = {
            'api-key': api_key,
            'speed': '',
            'voice': 'banmai',
            'Content-Type': 'text/plain'
    }
    response = requests.post(url, headers=headers, data=text.encode('utf-8'))
    if response.status_code == 200:
            print('Response:', response.json())
            return response.json()['async']
    else:
            print('Error:', response.status_code, response.text)

def AskGemini(text):
    print('Start asking Gemini...')
    api_key = 'AIzaSyDOMPDl6R4ooRAb6_BX24Bju6x820OfqEk'
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
    headers = {
            'Content-Type': 'application/json'
    }

    data = {
            "contents": [
                    {
                            "parts": [
                                    {
                                            "text": "Tóm tắt đoạn báo sau thành đúng 50 từ: \n" + text
                                    }
                            ]
                    }
            ]
    }
    response = requests.post(f'{url}?key={api_key}', headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                text_output = candidate['content']['parts'][0]['text']
                print('Output Text:', text_output)
                return text_output
    else:
            print('Error:', response.status_code, response.text)
