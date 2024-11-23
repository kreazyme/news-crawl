import requests
import time

def download_and_save(url):
    download_count = 0
    while download_count < 20:
        try:
            response = requests.get(url)
            status_code = response.status_code
            if status_code != 200:
                raise Exception("Failed to download, status code:", status_code)
            file_data = response.content
            file_name = url.split("/")[-1]
            with open(file_name,"wb") as file:
                file.write(file_data)
            print("Downloaded", file_name)
            return file_name
        except Exception as e:
            print("Download failed:", e)
            download_count += 1
            time.sleep(2)
