"""
Flask API để serve giá cà phê
"""
from flask import Flask, jsonify
import json
import os
from datetime import datetime
import asyncio
from scraper import get_coffee_prices
import threading
import time

app = Flask(__name__)

# Cache dữ liệu
cache = {
    "data": None,
    "last_update": None
}

CACHE_FILE = "coffee_prices_latest.json"


def load_cache():
    """Load cache từ file"""
    global cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache["data"] = json.load(f)
                cache["last_update"] = datetime.now()
                print(f"Loaded cache from {CACHE_FILE}")
        except Exception as e:
            print(f"Error loading cache: {e}")


def save_cache(data):
    """Lưu cache vào file"""
    global cache
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        cache["data"] = data
        cache["last_update"] = datetime.now()
        print(f"Saved cache to {CACHE_FILE}")
    except Exception as e:
        print(f"Error saving cache: {e}")


async def scrape_prices():
    """Scrape giá cà phê"""
    try:
        print(f"\n{'='*60}")
        print(f"Scraping at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        data = await get_coffee_prices()
        save_cache(data)
        
        print("\n--- Giá cập nhật ---")
        for province, price in data["prices"].items():
            change = data["changes"][province]
            print(f"{province:15} | {price:>10} | {change:>10}")
        
        return data
    except Exception as e:
        print(f"Error scraping: {e}")
        return None


def scrape_job():
    """Background job chạy mỗi 10 phút"""
    while True:
        try:
            asyncio.run(scrape_prices())
        except Exception as e:
            print(f"Scrape job error: {e}")
        
        # Chờ 10 phút
        print(f"\nChờ 10 phút đến lần scrape tiếp theo...")
        time.sleep(600)  # 600 seconds = 10 minutes


@app.route('/')
def home():
    """Home page"""
    return jsonify({
        "message": "Coffee Price API",
        "endpoints": {
            "/api/coffee-prices": "Get latest coffee prices",
            "/api/health": "Health check"
        }
    })


@app.route('/api/coffee-prices')
def get_prices():
    """API endpoint trả về giá cà phê"""
    if cache["data"] is None:
        return jsonify({
            "error": "Dữ liệu chưa sẵn sàng. Vui lòng thử lại sau vài phút."
        }), 503
    
    return jsonify(cache["data"])


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "last_update": cache["last_update"].isoformat() if cache["last_update"] else None,
        "has_data": cache["data"] is not None
    })


@app.route('/api/scrape-now')
def scrape_now():
    """Trigger scrape ngay lập tức"""
    try:
        data = asyncio.run(scrape_prices())
        if data:
            return jsonify({
                "status": "success",
                "data": data
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Không thể scrape dữ liệu"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    # Load cache khi start
    load_cache()
    
    # Start background scraping job
    scrape_thread = threading.Thread(target=scrape_job, daemon=True)
    scrape_thread.start()
    
    # Start Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
