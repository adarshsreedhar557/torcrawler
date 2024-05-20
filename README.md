Tor Crawler
Tor Crawler is a robust and feature-rich web crawler designed for research purposes. It efficiently crawls .onion websites, providing advanced data processing, caching, and export functionalities. This crawler is built with scalability, distributed crawling, and advanced data processing in mind.

Features
Distributed Crawling: Utilize multiple instances for distributed crawling.
Caching: Redis-based caching to avoid redundant crawling.
NLP Processing: Extract insights using NLTK.
Image and File Handling: Download and process images and files from crawled pages.
API Integration: Enrich data using external APIs.
Authentication Handling: Support for sites requiring authentication.
Robust Error Handling: Detailed error logging and retry mechanisms.
Analytics Dashboard: Advanced analytics and visualization of crawled data.
Data Anonymization: Ensure privacy by anonymizing sensitive information.
Security Features: Implement security checks to avoid potential vulnerabilities.
Modular Design: Facilitates the addition of new features.
Advanced Scheduling: Schedule crawling jobs with advanced scheduling capabilities.
Machine Learning: Integrate machine learning models for content classification.
Content Filtering: Crawl specific types of content.
Multi-language Support: Handle multilingual content.
Notifications: Slack notifications for important events.
Rate Limiting: Sophisticated rate limiting and adaptive delays.
Data Export: Export data in multiple formats (CSV, JSON, XML, Parquet).
Configurable Pipelines: Customizable data processing pipelines.
Test Coverage: Unit tests and integration tests for robustness.
Project Structure


tor_crawler/
├── crawler.py
├── config.yaml
├── .env
├── db_setup.py
├── requirements.txt
├── web_interface.py
├── cache.py
├── nlp_processor.py
├── file_handler.py
├── api_integrations.py
├── auth_handler.py
├── notifications.py
├── scheduler.py
└── README.md
Installation
Clone the repository:

git clone https://github.com/yourusername/tor_crawler.git
cd tor_crawler
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:


pip install -r requirements.txt
Setup environment variables:

Create a .env file in the root directory with the following content:


TOR_PASSWORD=your_password
DATABASE_URL=postgresql://user:password@localhost:5432/crawler_db
WEB_HOST=127.0.0.1
WEB_PORT=5000
REDIS_URL=redis://localhost:6379/0
SLACK_TOKEN=your_slack_token
Setup database:

Ensure you have PostgreSQL installed and running. Create a database and update the DATABASE_URL in the .env file accordingly.

Run the following script to set up the database schema:


python db_setup.py
Start Tor:

Make sure Tor is installed and running:


tor
Usage
Start the Crawler:


python crawler.py
Start the Web Interface:


python web_interface.py
Monitor and Manage Crawling:

Access the web interface at http://127.0.0.1:5000 to monitor and manage the crawler.

Configuration
Edit the config.yaml file to customize the crawler settings:

tor:
  renewal_interval: 600  # IP renewal interval in seconds

request:
  timeout: 30  # Request timeout in seconds
  delay: 5     # Delay between requests in seconds
  rate_limit: 10  # Maximum number of requests per minute

crawler:
  num_threads: 10  # Number of concurrent threads
  max_depth: 3  # Maximum depth for crawling
  cache_enabled: true  # Enable or disable caching
  auth_required: false  # Enable or disable authentication

start_urls:
  - 'http://exampleonion.onion'  # Add your initial .onion URLs here

data_export:
  formats: ['csv', 'json', 'xml', 'parquet']  # Data export formats

web:
  host: '127.0.0.1'
  port: 5000

notifications:
  enabled: true  # Enable or disable notifications
  slack_channel: '#crawler-alerts'  # Slack channel for notifications
Advanced Features
Caching
The crawler uses Redis for caching. Ensure Redis is installed and running. Update the REDIS_URL in the .env file accordingly.

NLP Processing
The nlp_processor.py module uses NLTK to process text. Ensure NLTK data is downloaded:


import nltk
nltk.download('punkt')
nltk.download('stopwords')
Notifications
Enable Slack notifications by setting the SLACK_TOKEN and slack_channel in the .env and config.yaml files.

Scheduling
Use the scheduler.py module for advanced scheduling of crawling jobs:


import schedule
import time

def job():
    print("Running scheduled job...")
    # Add your scheduled job logic here

schedule.every().day.at("01:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
Contributing
Contributions are welcome! Please create a pull request with your enhancements.

License
This project is licensed under the MIT License.
