# ☕ Coffee Price Scraper

Tool cào giá cà phê từ giacaphe.com - **Tự động chạy mỗi ngày và lưu vào Google Sheets**

## 🚀 Setup Tự động (Khuyên dùng)

**Đọc file: `HUONG_DAN_TU_DONG.md`** - Chỉ 3 bước, 8 phút setup xong!

Hệ thống sẽ:
- ✅ Tự động scrape mỗi ngày lúc 8:00 sáng
- ✅ Lưu vào Google Sheets
- ✅ Hoàn toàn miễn phí (GitHub Actions + Google Apps Script)
- ✅ Không cần server, không cần hosting

## 📁 Files quan trọng

- **`HUONG_DAN_TU_DONG.md`** - Hướng dẫn setup tự động (ĐỌC FILE NÀY!)
- `scraper_to_sheets.py` - Script chính gửi dữ liệu lên Google Sheets
- `google-apps-script/api-only.gs` - Code Google Apps Script
- `.github/workflows/scrape-coffee-prices.yml` - GitHub Actions workflow

---

## 💻 Chạy thủ công trên máy local

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
