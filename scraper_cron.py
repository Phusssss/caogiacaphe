"""
Scraper cho Render Cron Job
Chạy mỗi 10 phút, lưu kết quả và gửi đến API nếu có
"""
import asyncio
import json
import os
import requests
from datetime import datetime
from scraper import get_coffee_prices


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
        
        # Lưu vào file
        output_file = "coffee_prices_latest.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Đã lưu vào {output_file}")
        
        # Gửi đến API endpoint nếu có
        api_endpoint = os.environ.get('API_ENDPOINT')
        if api_endpoint:
            try:
                response = requests.post(
                    f"{api_endpoint}/update",
                    json=data,
                    timeout=10
                )
                if response.status_code == 200:
                    print(f"✓ Đã gửi dữ liệu đến API")
                else:
                    print(f"⚠ API trả về status {response.status_code}")
            except Exception as e:
                print(f"⚠ Không thể gửi đến API: {e}")
        
        print("\n✓ Hoàn thành!")
        
    except Exception as e:
        print(f"✗ Lỗi: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
