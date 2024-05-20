import os
import requests
from PIL import Image
from io import BytesIO

def handle_files(soup, base_url):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    for img_tag in soup.find_all('img', src=True):
        img_url = img_tag['src']
        if img_url.startswith('http'):
            try:
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                img_format = img.format.lower()
                img_name = os.path.basename(img_url)
                img.save(f'downloads/{img_name}', format=img_format)
            except Exception as e:
                print(f"Failed to download image {img_url}: {e}")

    for link in soup.find_all('a', href=True):
        file_url = link['href']
        if file_url.startswith('http'):
            try:
                response = requests.get(file_url)
                file_name = os.path.basename(file_url)
                with open(f'downloads/{file_name}', 'wb') as file:
                    file.write(response.content)
            except Exception as e:
                print(f"Failed to download file {file_url}: {e}")
