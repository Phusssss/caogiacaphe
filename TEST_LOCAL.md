# Test Scraper trên máy Local

## Cài đặt

```bash
py -m pip install -r requirements.txt
py -m playwright install chromium
```

## Test cả 2 phương pháp

```bash
py test_scraper.py
```

Script sẽ test:
1. Playwright (bypass Cloudflare)
2. Simple requests (nhanh hơn)

## Test từng phương pháp

### Test Playwright

```bash
py scraper.py
```

### Test Simple Requests

```bash
py scraper_simple.py
```

## Kết quả

- File JSON: `coffee_prices_latest.json`
- Debug HTML: `debug_*.html`
- Screenshot: `debug_screenshot_*.png`

## Gửi lên Google Sheets

```bash
# Tạo file .env
copy .env.example .env

# Sửa .env và thêm APPS_SCRIPT_URL

# Chạy
py scraper_to_sheets.py
```

## Troubleshooting

### Lỗi: "Không tìm đủ dữ liệu"

1. Mở file `debug_screenshot_1.png` - Xem trang web có load đúng không
2. Mở file `debug_fail_attempt_1.html` - Xem HTML source
3. Website có thể đã thay đổi cấu trúc

### Lỗi: Playwright không cài được

```bash
# Thử cài manual
py -m playwright install chromium --with-deps
```

### Lỗi: Module not found

```bash
# Cài lại dependencies
py -m pip install -r requirements.txt --force-reinstall
```
