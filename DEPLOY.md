# Hướng dẫn Deploy

## Option 1: GitHub Actions (Miễn phí, Khuyên dùng) ⭐

### Ưu điểm:
- Hoàn toàn miễn phí
- Tự động chạy theo lịch
- Không cần server

### Cách setup:

1. Push code lên GitHub repository

2. Workflow đã được tạo sẵn tại `.github/workflows/scrape-coffee-prices.yml`

3. Workflow sẽ:
   - Chạy mỗi ngày lúc 8:00 AM (giờ Việt Nam)
   - Lưu kết quả vào GitHub Artifacts
   - Có thể commit kết quả vào repo

4. Để chạy thủ công:
   - Vào tab "Actions" trên GitHub
   - Chọn workflow "Scrape Coffee Prices"
   - Click "Run workflow"

### Gửi kết quả đến API:

Thêm vào workflow file (sau bước "Run scraper"):

```yaml
- name: Send to API
  env:
    API_ENDPOINT: ${{ secrets.API_ENDPOINT }}
  run: python scraper_with_api.py
```

Sau đó thêm secret `API_ENDPOINT` trong GitHub Settings > Secrets.

---

## Option 2: Railway.app (Miễn phí 500h/tháng)

### Cách deploy:

1. Tạo tài khoản tại https://railway.app

2. Tạo file `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python scraper.py",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

3. Connect GitHub repo và deploy

4. Thêm Cron Job trong Railway để chạy định kỳ

---

## Option 3: Render.com (Miễn phí có giới hạn)

### Cách deploy:

1. Tạo tài khoản tại https://render.com

2. Tạo "Cron Job" service

3. Connect GitHub repo

4. Cấu hình:
   - Build Command: `pip install -r requirements.txt && playwright install chromium && playwright install-deps`
   - Start Command: `python scraper.py`
   - Schedule: `0 1 * * *` (8:00 AM giờ VN)

---

## Option 4: Chạy local với Task Scheduler (Windows)

### Cách setup:

1. Mở Task Scheduler

2. Tạo Basic Task:
   - Name: "Coffee Price Scraper"
   - Trigger: Daily lúc 8:00 AM
   - Action: Start a program
   - Program: `py`
   - Arguments: `F:\Cong viec\caogiacaphe\scraper.py`
   - Start in: `F:\Cong viec\caogiacaphe`

3. Máy tính phải bật vào thời điểm chạy

---

## Gửi kết quả đến Google Apps Script

Sau khi có API endpoint (từ Railway/Render), cập nhật trong `botgiacaphe/code.gs`:

```javascript
const apiUrl = "https://your-api-url.com/api/coffee-prices";
```

Hoặc tạo API endpoint mới để Google Apps Script gọi đến Railway/Render.
