from flask import Flask, jsonify, request
from db_setup import CrawledData, engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database setup
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def home():
    return "Tor Crawler Web Interface"

@app.route('/data', methods=['GET'])
def get_data():
    data = session.query(CrawledData).all()
    return jsonify([{'url': item.url, 'content': item.content} for item in data])

@app.route('/restart', methods=['POST'])
def restart_crawler():
    # Implement crawler restart logic
    return "Crawler restarted", 200

@app.route('/export', methods=['GET'])
def export_data():
    format = request.args.get('format', 'csv')
    if format in ['csv', 'json', 'xml', 'parquet']:
        # Call export function from crawler module
        from crawler import export_data
        export_data(format)
        return f"Data exported as {format}", 200
    else:
        return "Invalid format", 400

if __name__ == "__main__":
    app.run(host=os.getenv('WEB_HOST', '127.0.0.1'), port=int(os.getenv('WEB_PORT', 5000)))
