"""
Tool cào giá cà phê và gửi đến API
"""
import asyncio
from playwright.async_api import async_playwright
import json
import re
import time
import requests
import os


async def get_coffee_prices():
    """Lấy giá cà phê từ giacaphe.com"""
    url = "https://giacaphe.com/gia-ca-phe-noi-dia/"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
        )
        
        page = await context.new_page()
        
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        try:
            print("Đang truy cập trang...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(8)
            
            css_content = await page.evaluate("""
                () => {
                    const styles = Array.from(document.querySelectorAll('style'));
                    return styles.map(s => s.textContent).join('\\n');
                }
            """)
            
            pattern = re.compile(r"::after\s*{\s*content:\s*'([^']+)'")
            values = pattern.findall(css_content)
            
            print(f"Tìm thấy {len(values)} giá trị")
            
            if len(values) < 8:
                raise Exception(f"Không tìm đủ dữ liệu giá")
            
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
            
        finally:
            await browser.close()


def send_to_api(data):
    """Gửi dữ liệu đến API endpoint"""
    api_url = os.environ.get('API_ENDPOINT', 'https://your-api.com/update')
    
    try:
        response = requests.post(api_url, json=data, timeout=10)
        response.raise_for_status()
        print(f"✓ Đã gửi dữ liệu đến API: {api_url}")
        return True
    except Exception as e:
        print(f"✗ Lỗi khi gửi đến API: {e}")
        return False


async def main():
    print("="*60)
    print("Đang cào giá cà phê từ giacaphe.com...")
    print("="*60)
    
    try:
        data = await get_coffee_prices()
        
        print("\n--- Giá trong nước ---")
        for province, price in data["prices"].items():
            change = data["changes"][province]
            print(f"{province:15} | {price:>10} | {change:>10}")
        
        # Lưu vào file
        output_file = f"coffee_prices_latest.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Đã lưu vào {output_file}")
        
        # Gửi đến API (nếu có)
        if os.environ.get('API_ENDPOINT'):
            send_to_api(data)
        
    except Exception as e:
        print(f"✗ Lỗi: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
