# Setup Cuối Cùng - MIỄN PHÍ 100%

## Kiến trúc

```
Python Scraper (Local/GitHub Actions)
    ↓ (POST dữ liệu)
Google Apps Script
    ↓ (Lưu vào)
Google Sheets
    ↓ (Đọc từ)
API Endpoint (GET)
```

## Bước 1: Setup Google Apps Script

1. Mở Google Sheet: https://docs.google.com/spreadsheets/d/1Ril0Srxm4mfzd-lWs2a6bONaVPM4kBIDRJmSMaFzmH8/edit
2. **Extensions** > **Apps Script**
3. **XÓA HẾT** code cũ
4. Copy code từ file `api-only.gs`
5. Paste vào Apps Script
6. **Save** (Ctrl+S)

## Bước 2: Deploy Web App

1. Click **Deploy** > **New deployment**
2. Click ⚙️ > **Web app**
3. Cấu hình:
   - Description: `Coffee Price API`
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Click **Deploy**
5. **Copy Web app URL** (quan trọng!)
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```

## Bước 3: Test API (GET)

Mở browser, truy cập URL vừa copy:
```
https://script.google.com/macros/s/AKfycby.../exec
```

Lần đầu sẽ báo lỗi "Chưa có dữ liệu" - đây là bình thường.

## Bước 4: Chạy Python Scraper

### Option A: Chạy trên máy local

1. Mở terminal/cmd
2. Set environment variable:
   ```cmd
   set APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycby.../exec
   ```
3. Chạy scraper:
   ```cmd
   py scraper_to_sheets.py
   ```

### Option B: GitHub Actions (Tự động mỗi 10 phút)

1. Vào GitHub repo: https://github.com/Phusssss/caogiacaphe
2. **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Thêm secret:
   - Name: `APPS_SCRIPT_URL`
   - Value: `https://script.google.com/macros/s/AKfycby.../exec`
5. Click **Add secret**

Workflow đã được tạo sẵn, sẽ tự động chạy mỗi 10 phút.

## Bước 5: Kiểm tra kết quả

1. Sau khi chạy scraper, vào Google Sheet
2. Bạn sẽ thấy 2 sheet:
   - **Prices** - Lịch sử tất cả giá
   - **Latest** - Giá mới nhất
3. Test API lại:
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```
   Bây giờ sẽ trả về JSON với giá cà phê

## Bước 6: Sử dụng API

### Trong Telegram Bot (Google Apps Script):

```javascript
function getCoffeePrice() {
  const apiUrl = "https://script.google.com/macros/s/AKfycby.../exec";
  
  try {
    const response = UrlFetchApp.fetch(apiUrl);
    const data = JSON.parse(response.getContentText());
    
    let message = "☕ Giá cà phê hôm nay:\n";
    message += `Đắk Lắk: ${data.prices["Đắk Lắk"]} (${data.changes["Đắk Lắk"]})\n`;
    message += `Lâm Đồng: ${data.prices["Lâm Đồng"]} (${data.changes["Lâm Đồng"]})\n`;
    message += `Gia Lai: ${data.prices["Gia Lai"]} (${data.changes["Gia Lai"]})\n`;
    message += `Đắk Nông: ${data.prices["Đắk Nông"]} (${data.changes["Đắk Nông"]})\n`;
    message += `\n(Cập nhật: ${data.date})`;
    
    return message;
  } catch (e) {
    return "Không thể lấy giá cà phê lúc này.";
  }
}
```

## Tóm tắt

✅ **Hoàn toàn miễn phí**
- Python scraper bypass được Cloudflare
- Google Apps Script làm API miễn phí
- Google Sheets lưu dữ liệu miễn phí

✅ **Tự động**
- GitHub Actions chạy mỗi 10 phút
- Hoặc Task Scheduler trên Windows

✅ **Đơn giản**
- Không cần server
- Không cần database
- Chỉ cần Google Account

## Workflow file cho GitHub Actions

Tạo file `.github/workflows/scrape-to-sheets.yml`:

```yaml
name: Scrape to Google Sheets

on:
  schedule:
    - cron: '*/10 * * * *'  # Mỗi 10 phút
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install chromium
        playwright install-deps
    
    - name: Run scraper
      env:
        APPS_SCRIPT_URL: ${{ secrets.APPS_SCRIPT_URL }}
      run: python scraper_to_sheets.py
```

## Troubleshooting

### Lỗi "Chưa có dữ liệu"
- Chưa chạy scraper lần nào
- Chạy `py scraper_to_sheets.py` để gửi dữ liệu lần đầu

### Scraper không gửi được lên Sheets
- Kiểm tra APPS_SCRIPT_URL đã đúng chưa
- Kiểm tra Apps Script đã deploy chưa
- Xem logs để biết lỗi cụ thể

### GitHub Actions fail
- Có thể vẫn bị Cloudflare chặn
- Xem logs trong Actions tab
- Thử tăng delay trong scraper.py
