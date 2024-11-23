import crawl
import slideshow
import cv2
import urllib.request
import numpy as np
import download
from moviepy.editor import AudioFileClip

def crawler(article_url):
    print("Crawling article from:", article_url)
    article_text,image_urls = crawl.CrawlVNExpress(article_url)
    sumarized_text = crawl.AskGemini(article_text)
    audio_url = crawl.TTS(sumarized_text)
    audio_saved_path = download.download_and_save(audio_url)
    slideshow.create_video_from_images(image_urls,audio_saved_path, output_file="audio.mp4")

article_url = 'https://vnexpress.net/nhieu-xe-container-o-tp-hcm-lap-camera-xoa-diem-mu-tranh-tai-nan-4817333.html'
crawler(article_url)

# url = crawl.TTS('Xin chào, tôi sẽ giúp bạn tạo video từ bài viết trên VnExpress')
# file_name = download.download_and_save(url)
# print(file_name)

# Tải tệp audio