# Hướng dẫn Deploy lên Railway.app

## Bước 1: Tạo tài khoản Railway

1. Vào https://railway.app
2. Sign up bằng GitHub account
3. Verify email

## Bước 2: Deploy từ GitHub

1. Click "New Project"
2. Chọn "Deploy from GitHub repo"
3. Chọn repository: `Phusssss/caogiacaphe`
4. Railway sẽ tự động detect và deploy

## Bước 3: Cấu hình

Railway sẽ tự động:
- Cài đặt Python dependencies
- Cài đặt Playwright và Chromium
- Start Flask app với Gunicorn
- Scraper sẽ chạy mỗi 10 phút tự động

## Bước 4: Lấy URL API

1. Sau khi deploy xong, vào tab "Settings"
2. Scroll xuống "Domains"
3. Click "Generate Domain"
4. Copy URL (ví dụ: `https://caogiacaphe-production.up.railway.app`)

## Bước 5: Test API

Mở browser và test các endpoint:

- **Home**: `https://your-app.railway.app/`
- **Giá cà phê**: `https://your-app.railway.app/api/coffee-prices`
- **Health check**: `https://your-app.railway.app/api/health`
- **Scrape ngay**: `https://your-app.railway.app/api/scrape-now`

## Bước 6: Cập nhật Google Apps Script

Mở file `botgiacaphe/code.gs` và update API URL:

```javascript
function getCoffeePrice() {
  const apiUrl = "https://your-app.railway.app/api/coffee-prices";
  // ... rest of code
}
```

## API Endpoints

### GET /api/coffee-prices

Trả về giá cà phê mới nhất:

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

### GET /api/health

Kiểm tra trạng thái:

```json
{
  "status": "ok",
  "last_update": "2026-02-11T14:29:24",
  "has_data": true
}
```

### GET /api/scrape-now

Trigger scrape ngay lập tức (không cần chờ 10 phút).

## Lưu ý

- Railway free tier: 500 giờ/tháng (đủ để chạy 24/7)
- App sẽ tự động scrape mỗi 10 phút
- Dữ liệu được cache để API response nhanh
- Nếu Railway sleep, lần request đầu tiên sẽ wake up app

## Troubleshooting

### App không start

1. Vào tab "Deployments"
2. Click vào deployment mới nhất
3. Xem logs để debug

### Scraper bị lỗi

1. Vào tab "Deployments" > "View Logs"
2. Tìm error message
3. Có thể Cloudflare vẫn chặn - thử tăng delay trong `scraper.py`

### Thay đổi tần suất scrape

Sửa trong `app.py`:

```python
time.sleep(600)  # 600 = 10 phút, 1800 = 30 phút
```
