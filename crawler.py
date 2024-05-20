import requests
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import threading
import time
import yaml
import os
from queue import Queue
import logging
from sqlalchemy.orm import sessionmaker
from db_setup import CrawledData, engine
from dotenv import load_dotenv
from prometheus_client import start_http_server, Counter
from fake_useragent import UserAgent
from cache import Cache
from nlp_processor import process_text
from file_handler import handle_files
from api_integrations import enrich_data
from auth_handler import authenticate
from notifications import send_slack_notification
import schedule

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Database setup
Session = sessionmaker(bind=engine)
session = Session()

# Metrics
crawled_pages = Counter('crawled_pages', 'Number of pages crawled')

# URL queue and visited set
url_queue = Queue()
visited_urls = set()

# Fake User-Agent
ua = UserAgent()

# Cache
cache = Cache()

def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=os.getenv("TOR_PASSWORD"))
        controller.signal(Signal.NEWNYM)
        logging.info("IP renewed")

def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    session.headers.update({'User-Agent': ua.random})
    return session

def store_data(url, content):
    new_entry = CrawledData(url=url, content=content)
    session.add(new_entry)
    session.commit()

def crawl_onion_site():
    while not url_queue.empty():
        url, current_depth = url_queue.get()
        if url in visited_urls or current_depth > config['crawler']['max_depth']:
            url_queue.task_done()
            continue

        if config['crawler']['cache_enabled'] and cache.exists(url):
            logging.info(f"Cache hit for {url}")
            content = cache.get(url)
        else:
            session = get_tor_session()
            try:
                response = session.get(url, timeout=config['request']['timeout'])
                if response.status_code == 200:
                    content = response.text
                    soup = BeautifulSoup(content, 'html.parser')
                    content = process_text(content)
                    handle_files(soup, url)
                    enrich_data(content)
                    store_data(url, content)
                    if config['crawler']['cache_enabled']:
                        cache.set(url, content)
                    visited_urls.add(url)
                    logging.info(f"Crawled: {url}")
                    crawled_pages.inc()

                    if current_depth < config['crawler']['max_depth']:
                        for link in soup.find_all('a', href=True):
                            link_url = link['href']
                            if link_url.startswith('http://') or link_url.startswith('https://'):
                                url_queue.put((link_url, current_depth + 1))
                else:
                    logging.warning(f"Failed to retrieve {url}, status code: {response.status_code}")
            except requests.RequestException as e:
                logging.error(f"Error crawling {url}: {e}")
            finally:
                url_queue.task_done()
                time.sleep(config['request']['delay'])

def export_data(format):
    if format == 'csv':
        export_csv()
    elif format == 'json':
        export_json()
    elif format == 'xml':
        export_xml()
    elif format == 'parquet':
        export_parquet()

def export_csv():
    import csv
    with open('crawled_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['url', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in session.query(CrawledData).all():
            writer.writerow({'url': data.url, 'content': data.content})

def export_json():
    import json
    data = [{'url': data.url, 'content': data.content} for data in session.query(CrawledData).all()]
    with open('crawled_data.json', 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def export_xml():
    import dicttoxml
    data = [{'url': data.url, 'content': data.content} for data in session.query(CrawledData).all()]
    xml_data = dicttoxml.dicttoxml(data)
    with open('crawled_data.xml', 'wb') as xmlfile:
        xmlfile.write(xml_data)

def export_parquet():
    import pandas as pd
    data = [{'url': data.url, 'content': data.content} for data in session.query(CrawledData).all()]
    df = pd.DataFrame(data)
    df.to_parquet('crawled_data.parquet')

if __name__ == "__main__":
    # Load initial URLs
    for initial_url in config['start_urls']:
        url_queue.put((initial_url, 0))
    
    # Start Tor IP renewal thread
    def renew_ip_periodically():
        while True:
            renew_tor_ip()
            time.sleep(config['tor']['renewal_interval'])

    threading.Thread(target=renew_ip_periodically, daemon=True).start()

    # Start metrics server
    start_http_server(8000)

    # Start crawling threads
    threads = []
    for _ in range(config['crawler']['num_threads']):
        thread = threading.Thread(target=crawl_onion_site)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    logging.info("Crawling complete")

    # Export data
    for format in config['data_export']['formats']:
        export_data(format)
