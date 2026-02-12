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
    
    # Thử tối đa 3 lần
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await _scrape_once(url, attempt + 1)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10
                print(f"Lần thử {attempt + 1} thất bại. Chờ {wait_time}s rồi thử lại...")
                await asyncio.sleep(wait_time)
            else:
                raise e


async def _scrape_once(url, attempt_num):
    """Thực hiện scrape một lần"""
    print(f"\n--- Lần thử {attempt_num} ---")
    
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
            
            # Chờ lâu hơn cho GitHub Actions
            print("Chờ Cloudflare...")
            await asyncio.sleep(20)
            
            # Chờ network idle
            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
            
            # Scroll để trigger events
            await page.evaluate("window.scrollTo(0, 500)")
            await asyncio.sleep(3)
            await page.evaluate("window.scrollTo(0, 1000)")
            await asyncio.sleep(2)
            
            # Screenshot để debug
            await page.screenshot(path=f"debug_screenshot_{attempt_num}.png")
            
            # Phương pháp 1: Lấy CSS content
            print("Đang lấy CSS content...")
            css_content = await page.evaluate("""
                () => {
                    const styles = Array.from(document.querySelectorAll('style'));
                    return styles.map(s => s.textContent).join('\\n');
                }
            """)
            
            # Tìm giá trong CSS
            pattern = re.compile(r"::after\s*{\s*content:\s*['\"]([^'\"]+)['\"]")
            values = pattern.findall(css_content)
            
            print(f"Phương pháp 1 (CSS): Tìm thấy {len(values)} giá trị")
            
            # Phương pháp 2: Lấy trực tiếp từ computed style
            if len(values) < 8:
                print("Thử phương pháp 2 (Computed Style)...")
                values = await page.evaluate("""
                    () => {
                        const results = [];
                        const elements = document.querySelectorAll('.price-value, .price-change, [class*="price"]');
                        
                        elements.forEach(el => {
                            // Lấy ::after content
                            const after = window.getComputedStyle(el, '::after').content;
                            if (after && after !== 'none' && after !== '""') {
                                results.push(after.replace(/['"]/g, ''));
                            }
                            
                            // Lấy text content
                            const text = el.textContent.trim();
                            if (text && text.match(/[\d,\.\-\+]+/)) {
                                results.push(text);
                            }
                        });
                        
                        return results;
                    }
                """)
                print(f"Phương pháp 2: Tìm thấy {len(values)} giá trị")
            
            # Phương pháp 3: Tìm tất cả elements có class chứa "price"
            if len(values) < 8:
                print("Thử phương pháp 3 (All price elements)...")
                all_text = await page.evaluate("""
                    () => {
                        const results = [];
                        const allElements = document.querySelectorAll('*');
                        
                        allElements.forEach(el => {
                            const className = el.className || '';
                            if (typeof className === 'string' && className.toLowerCase().includes('price')) {
                                const after = window.getComputedStyle(el, '::after').content;
                                if (after && after !== 'none' && after !== '""') {
                                    results.push(after.replace(/['"]/g, ''));
                                }
                            }
                        });
                        
                        return results;
                    }
                """)
                values.extend(all_text)
                print(f"Phương pháp 3: Tổng cộng {len(values)} giá trị")
            
            if len(values) < 8:
                # Lưu HTML để debug
                html = await page.content()
                debug_file = f"debug_fail_attempt_{attempt_num}.html"
                with open(debug_file, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Đã lưu HTML vào {debug_file}")
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
