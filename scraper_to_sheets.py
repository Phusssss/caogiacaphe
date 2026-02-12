"""
Scraper gửi dữ liệu lên Google Apps Script
Chạy trên máy local hoặc GitHub Actions
"""
import asyncio
import json
import requests
import os
from datetime import datetime
from scraper import get_coffee_prices
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# URL của Google Apps Script Web App
APPS_SCRIPT_URL = os.environ.get('APPS_SCRIPT_URL', '')


async def main():
    print("="*60)
    print(f"Scraping at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    try:
        # Scrape giá
        data = await get_coffee_prices()
        
        # In kết quả
        print("\n--- Giá cà phê ---")
        for province, price in data["prices"].items():
            change = data["changes"][province]
            print(f"{province:15} | {price:>10} | {change:>10}")
        
        # Lưu vào file local
        output_file = "coffee_prices_latest.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Đã lưu vào {output_file}")
        
        # Gửi lên Google Apps Script
        if APPS_SCRIPT_URL:
            try:
                print(f"\nĐang gửi dữ liệu lên Google Sheets...")
                response = requests.post(
                    APPS_SCRIPT_URL,
                    json=data,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('status') == 'success':
                        print("✓ Đã gửi dữ liệu lên Google Sheets")
                    else:
                        print(f"⚠ Lỗi: {result.get('message')}")
                else:
                    print(f"⚠ HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"⚠ Không thể gửi lên Google Sheets: {e}")
        else:
            print("\n⚠ Chưa cấu hình APPS_SCRIPT_URL")
            print("Thêm vào environment variable hoặc file .env")
        
        print("\n✓ Hoàn thành!")
        
    except Exception as e:
        print(f"✗ Lỗi: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
