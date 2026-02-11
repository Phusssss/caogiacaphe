# Hướng dẫn Deploy lên Render.com

## Tổng quan

Setup này bao gồm 2 services:
1. **Cron Job** - Scrape giá mỗi 10 phút
2. **Web Service** - API endpoint để lấy giá

## Bước 1: Tạo tài khoản Render

1. Vào https://render.com
2. Sign up bằng GitHub account
3. Verify email

## Bước 2: Deploy Cron Job (Scraper)

1. Vào Dashboard > **New** > **Cron Job**
2. Connect GitHub repository: `Phusssss/caogiacaphe`
3. Cấu hình:
   - **Name**: `coffee-price-scraper`
   - **Region**: Singapore (gần Việt Nam nhất)
   - **Branch**: `main`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && playwright install chromium && playwright install-deps
     ```
   - **Command**: 
     ```bash
     python scraper_cron.py
     ```
   - **Schedule**: `*/10 * * * *` (mỗi 10 phút)
   - **Plan**: Free

4. Click **Create Cron Job**

## Bước 3: Deploy Web Service (API)

1. Vào Dashboard > **New** > **Web Service**
2. Connect GitHub repository: `Phusssss/caogiacaphe`
3. Cấu hình:
   - **Name**: `coffee-price-api`
   - **Region**: Singapore
   - **Branch**: `main`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && playwright install chromium && playwright install-deps
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app
     ```
   - **Plan**: Free

4. Click **Create Web Service**

## Bước 4: Lấy URL API

1. Sau khi Web Service deploy xong
2. Copy URL (ví dụ: `https://coffee-price-api.onrender.com`)
3. Test: `https://coffee-price-api.onrender.com/api/coffee-prices`

## Bước 5: Kết nối Cron Job với API (Optional)

Nếu muốn Cron Job tự động update API:

1. Vào Cron Job settings
2. Thêm Environment Variable:
   - **Key**: `API_ENDPOINT`
   - **Value**: `https://coffee-price-api.onrender.com`
3. Save changes

## Bước 6: Cập nhật Google Apps Script

Mở Google Apps Script và update:

```javascript
function getCoffeePrice() {
  const apiUrl = "https://coffee-price-api.onrender.com/api/coffee-prices";
  
  try {
    const response = UrlFetchApp.fetch(apiUrl, { muteHttpExceptions: true });
    
    if (response.getResponseCode() !== 200) {
      Logger.log(`Lỗi API: ${response.getContentText()}`);
      return "Không thể lấy dữ liệu giá cà phê vào lúc này.";
    }
    
    const data = JSON.parse(response.getContentText());
    const prices = data.prices;
    
    let message = "☕ Giá cà phê hôm nay:\n";
    message += `Đắk Lắk: ${prices["Đắk Lắk"]} (${data.changes["Đắk Lắk"]})\n`;
    message += `Lâm Đồng: ${prices["Lâm Đồng"]} (${data.changes["Lâm Đồng"]})\n`;
    message += `Gia Lai: ${prices["Gia Lai"]} (${data.changes["Gia Lai"]})\n`;
    message += `Đắk Nông: ${prices["Đắk Nông"]} (${data.changes["Đắk Nông"]})\n`;
    message += `\n(Nguồn: ${data.source} - ${data.date})`;
    
    return message;
  } catch (e) {
    Logger.log(e.toString());
    return "Đã có lỗi xảy ra khi xử lý dữ liệu.";
  }
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
  "last_update": "2026-02-11 14:29:24",
  "has_data": true
}
```

## Lưu ý quan trọng

### ⚠️ Web Service sẽ sleep

- Free tier của Render sẽ sleep sau 15 phút không có request
- Lần request đầu tiên sau khi sleep sẽ mất 30-60 giây để wake up
- Cron Job không bị sleep

### 💡 Giải pháp

**Option 1**: Dùng UptimeRobot để ping API mỗi 5 phút (giữ cho không sleep)
- Vào https://uptimerobot.com
- Tạo monitor ping đến `https://coffee-price-api.onrender.com/api/health`

**Option 2**: Chấp nhận sleep, request đầu tiên sẽ chậm

### 🔄 Cách hoạt động

1. Cron Job chạy mỗi 10 phút
2. Scrape giá từ giacaphe.com
3. Lưu vào file `coffee_prices_latest.json`
4. (Optional) Gửi đến Web Service API
5. Web Service đọc file và serve qua API

## Troubleshooting

### Cron Job fail

1. Vào Cron Job > Logs
2. Xem error message
3. Có thể Cloudflare vẫn chặn - thử tăng delay trong `scraper.py`

### Web Service không start

1. Vào Web Service > Logs
2. Check build logs và runtime logs

### API trả về 503

- Cron Job chưa chạy lần nào
- Chờ 10 phút để cron job chạy lần đầu
- Hoặc trigger manual deploy của Cron Job

## Thay đổi tần suất scrape

Sửa schedule trong Render dashboard hoặc `render.yaml`:

- Mỗi 5 phút: `*/5 * * * *`
- Mỗi 15 phút: `*/15 * * * *`
- Mỗi 30 phút: `*/30 * * * *`
- Mỗi giờ: `0 * * * *`
- Mỗi ngày lúc 8:00 AM: `0 1 * * *` (UTC, = 8:00 AM UTC+7)
