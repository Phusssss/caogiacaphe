"""
Tool cào giá cà phê từ giacaphe.com
Sử dụng Playwright với stealth mode
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json
import re
import time


async def get_coffee_prices():
    """Lấy giá cà phê từ giacaphe.com"""
    url = "https://giacaphe.com/gia-ca-phe-noi-dia/"
    
    async with async_playwright() as p:
        # Launch browser với args để bypass detection
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        # Tạo context với user agent thực tế
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='vi-VN',
            timezone_id='Asia/Ho_Chi_Minh'
        )
        
        page = await context.new_page()
        
        # Inject script để ẩn webdriver
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            window.navigator.chrome = {
                runtime: {}
            };
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['vi-VN', 'vi', 'en-US', 'en']
            });
        """)
        
        try:
            print("Đang truy cập trang...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Chờ một chút để Cloudflare check
            print("Chờ Cloudflare...")
            await asyncio.sleep(8)
            
            # Lấy CSS content
            print("Đang lấy CSS content...")
            css_content = await page.evaluate("""
                () => {
                    const styles = Array.from(document.querySelectorAll('style'));
                    return styles.map(s => s.textContent).join('\\n');
                }
            """)
            
            # Tìm giá trong CSS
            pattern = re.compile(r"::after\s*{\s*content:\s*'([^']+)'")
            values = pattern.findall(css_content)
            
            print(f"Tìm thấy {len(values)} giá trị trong CSS")
            
            if len(values) < 8:
                raise Exception(f"Không tìm đủ dữ liệu giá (chỉ tìm thấy {len(values)} giá trị)")
            
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
            
        finally:
            await browser.close()


async def main():
    """Hàm chính"""
    print("Đang cào giá cà phê từ giacaphe.com...")
    print("="*60)
    
    try:
        data = await get_coffee_prices()
        
        # In kết quả ra console
        print("\n" + "="*60)
        print(f"GIÁ CÀ PHÊ HÔM NAY - {data['date']}")
        print("="*60)
        
        print("\n--- Giá trong nước ---")
        for province, price in data["prices"].items():
            change = data["changes"][province]
            print(f"{province:15} | {price:>10} | {change:>10}")
        
        print(f"\nNguồn: {data['source']}")
        print(f"Đơn vị: {data['unit']}")
        
        # Lưu vào file JSON
        output_file = f"coffee_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Đã lưu dữ liệu vào file: {output_file}")
        
    except Exception as e:
        print(f"✗ Lỗi: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
