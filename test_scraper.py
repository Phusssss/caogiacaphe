"""
Script test scraper - Thử cả 2 phương pháp
"""
import asyncio
import sys


async def test_playwright():
    """Test Playwright scraper"""
    print("\n" + "="*60)
    print("TEST PHƯƠNG PHÁP 1: PLAYWRIGHT")
    print("="*60)
    
    try:
        from scraper import get_coffee_prices
        data = await get_coffee_prices()
        
        print("\n✓ Playwright thành công!")
        print(f"Giá Đắk Lắk: {data['prices']['Đắk Lắk']}")
        return True
        
    except Exception as e:
        print(f"\n✗ Playwright thất bại: {e}")
        return False


def test_simple():
    """Test simple requests scraper"""
    print("\n" + "="*60)
    print("TEST PHƯƠNG PHÁP 2: SIMPLE REQUESTS")
    print("="*60)
    
    try:
        from scraper_simple import get_coffee_prices_simple
        data = get_coffee_prices_simple()
        
        print("\n✓ Simple requests thành công!")
        print(f"Giá Đắk Lắk: {data['prices']['Đắk Lắk']}")
        return True
        
    except Exception as e:
        print(f"\n✗ Simple requests thất bại: {e}")
        return False


async def main():
    """Test cả 2 phương pháp"""
    print("ĐANG TEST SCRAPER...")
    
    # Test Playwright
    playwright_ok = await test_playwright()
    
    # Test Simple
    simple_ok = test_simple()
    
    # Kết quả
    print("\n" + "="*60)
    print("KẾT QUẢ")
    print("="*60)
    print(f"Playwright:      {'✓ OK' if playwright_ok else '✗ FAILED'}")
    print(f"Simple Requests: {'✓ OK' if simple_ok else '✗ FAILED'}")
    
    if playwright_ok or simple_ok:
        print("\n✓ Ít nhất 1 phương pháp hoạt động!")
        sys.exit(0)
    else:
        print("\n✗ Cả 2 phương pháp đều thất bại!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
