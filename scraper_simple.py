"""
Scraper đơn giản dùng requests (fallback nếu Playwright không hoạt động)
"""
import requests
import re
import json
import time
from datetime import datetime


def get_coffee_prices_simple():
    """Lấy giá cà phê bằng requests đơn giản"""
    url = "https://giacaphe.com/gia-ca-phe-noi-dia/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        print("Đang lấy dữ liệu từ giacaphe.com...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        html = response.text
        
        # Tìm giá trong CSS
        pattern = re.compile(r"::after\s*{\s*content:\s*['\"]([^'\"]+)['\"]")
        values = pattern.findall(html)
        
        print(f"Tìm thấy {len(values)} giá trị")
        
        if len(values) < 8:
            # Lưu HTML để debug
            with open("debug_simple.html", "w", encoding="utf-8") as f:
                f.write(html)
            raise Exception(f"Không tìm đủ dữ liệu (chỉ có {len(values)} giá trị)")
        
        # Parse dữ liệu
        data = {
            "source": "giacaphe.com",
            "prices": {
                "Đắk Lắk": values[0],
                "Lâm Đồng": values[2],
                "Gia Lai": values[4],
                "Đắk Nông": values[6],
            },
            "changes": {
                "Đắk Lắk": values[1],
                "Lâm Đồng": values[3],
                "Gia Lai": values[5],
                "Đắk Nông": values[7],
            },
            "timestamp": int(time.time()),
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "unit": "VNĐ/kg"
        }
        
        return data
        
    except Exception as e:
        print(f"Lỗi: {e}")
        raise


if __name__ == "__main__":
    try:
        data = get_coffee_prices_simple()
        
        # In kết quả
        print("\n" + "="*60)
        print(f"GIÁ CÀ PHÊ HÔM NAY - {data['date']}")
        print("="*60)
        
        print("\n--- Giá trong nước ---")
        for province, price in data["prices"].items():
            change = data["changes"][province]
            print(f"{province:15} | {price:>10} | {change:>10}")
        
        # Lưu file
        output_file = "coffee_prices_latest.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Đã lưu vào {output_file}")
        
    except Exception as e:
        print(f"✗ Lỗi: {e}")
        exit(1)
