# Coffee Price Scraper

Tool cào giá cà phê từ giacaphe.com sử dụng Playwright để bypass Cloudflare protection.

## Cài đặt

1. Cài đặt Python dependencies:
```bash
py -m pip install -r requirements.txt
```

2. Cài đặt Chromium browser cho Playwright:
```bash
py -m playwright install chromium
```

## Sử dụng

Chạy scraper:
```bash
py scraper.py
```

Kết quả sẽ được:
- In ra console
- Lưu vào file JSON với tên `coffee_prices_YYYYMMDD_HHMMSS.json`

## Dữ liệu trả về

```json
{
  "source": "giacaphe.com",
  "prices": {
    "Đắk Lắk": "95,300",
    "Lâm Đồng": "94,000",
    "Gia Lai": "95,300",
    "Đắk Nông": "95,500"
  },
  "changes": {
    "Đắk Lắk": "-1,000",
    "Lâm Đồng": "-1,200",
    "Gia Lai": "-1,000",
    "Đắk Nông": "-1,000"
  },
  "timestamp": 1707638964,
  "date": "2026-02-11 14:29:24",
  "unit": "VNĐ/kg"
}
```

## Lưu ý

- Website sử dụng Cloudflare protection, scraper cần khoảng 8-10 giây để bypass
- Giá được ẩn trong CSS `::after` content để chống scraper thông thường
- Nếu bị lỗi 403, thử chạy lại sau vài phút
