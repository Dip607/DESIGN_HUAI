# core/utils.py

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from transformers import pipeline
import requests


 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up HuggingFace ViT model
image_classifier = pipeline("image-classification", model="google/vit-base-patch16-224")




def fetch_pinterest_images(query, max_images=6):
    options = Options()
    options.add_argument("--headless")  # Run headless
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    search_url = f"https://www.pinterest.com/search/pins/?q={query}"
    driver.get(search_url)
    time.sleep(5)  # Let JS content load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    image_data = []
    for img in soup.find_all('img', src=True):
        if "pinimg.com" in img['src']:
            image_data.append({
                'image': img['src'],
                'url': search_url,
                'source': 'Pinterest'
            })
            if len(image_data) == max_images:
                break

    return image_data
def search_freepik_resources(query, num_results=5):
    API_KEY = 'FPSXd8057917f71e8e192cd4098f1170f109'
    url = 'https://api.freepik.com/v1/resources'
    params = {
        'term': query,
        'limit': num_results,
        'order': 'relevance'
    }
    headers = {'x-freepik-api-key': API_KEY}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json().get('data', [])
    images = []
    for item in data:
        img = item.get('image', {}).get('source', {}).get('url')
        page_url = item.get('url')
        if img and page_url:
            images.append({'image': img, 'url': page_url, 'source': 'Freepik'})
    return images
def get_dominant_colors(image_path, n_colors=5):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((150, 150))  # Resize for faster clustering
    img_array = np.array(image).reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, n_init=10)
    kmeans.fit(img_array)
    colors = kmeans.cluster_centers_.astype(int)

    hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in colors]
    return hex_colors

def get_image_labels(image_path, top_k=5):
    results = image_classifier(image_path, top_k=top_k)
    return [label["label"] for label in results]

def search_pixabay_images(query, num_results=5):
    API_KEY = '38796201-acece3314313f8e920e1e3032'
    url = 'https://pixabay.com/api/'
    params = {
        'key': API_KEY,
        'q': query,
        'image_type': 'photo',
        'per_page': num_results
    }
    response = requests.get(url, params=params)
    data = response.json()
    images = []
    for hit in data.get('hits', []):
        images.append({
            'image': hit['webformatURL'],
            'url': hit['pageURL'],
            'source': 'Pixabay'
        })
    return images
