"""
Flask API để serve giá cà phê
Đọc từ file được cập nhật bởi Cron Job
"""
from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

CACHE_FILE = "coffee_prices_latest.json"


def load_data():
    """Load dữ liệu từ file"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    return None


def save_data(data):
    """Lưu dữ liệu vào file"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


@app.route('/')
def home():
    """Home page"""
    data = load_data()
    last_update = data.get('date') if data else 'Chưa có dữ liệu'
    
    return jsonify({
        "message": "Coffee Price API",
        "last_update": last_update,
        "endpoints": {
            "/api/coffee-prices": "Get latest coffee prices",
            "/api/health": "Health check",
            "/update": "Update prices (POST, internal use)"
        }
    })


@app.route('/api/coffee-prices')
def get_prices():
    """API endpoint trả về giá cà phê"""
    data = load_data()
    
    if data is None:
        return jsonify({
            "error": "Dữ liệu chưa sẵn sàng. Vui lòng thử lại sau vài phút."
        }), 503
    
    return jsonify(data)


@app.route('/api/health')
def health():
    """Health check endpoint"""
    data = load_data()
    
    return jsonify({
        "status": "ok",
        "last_update": data.get('date') if data else None,
        "has_data": data is not None
    })


@app.route('/update', methods=['POST'])
def update_prices():
    """Endpoint để cron job update giá (internal use)"""
    try:
        data = request.get_json()
        if save_data(data):
            return jsonify({
                "status": "success",
                "message": "Đã cập nhật giá"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Không thể lưu dữ liệu"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
