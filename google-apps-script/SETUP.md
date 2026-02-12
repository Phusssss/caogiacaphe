# Setup Google Apps Script - MIỄN PHÍ 100%

## Ưu điểm
- ✅ Hoàn toàn miễn phí
- ✅ Chạy theo lịch (mỗi 10 phút)
- ✅ API endpoint miễn phí
- ✅ Lưu lịch sử vào Google Sheets
- ✅ Không cần server

## Bước 1: Tạo Google Sheet

1. Vào https://sheets.google.com
2. Tạo sheet mới, đặt tên: "Coffee Prices"
3. Copy Sheet ID từ URL:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
   ```

## Bước 2: Tạo Google Apps Script

1. Trong Google Sheet, vào **Extensions** > **Apps Script**
2. Xóa code mặc định
3. Copy toàn bộ code từ file `scraper.gs`
4. Paste vào Apps Script editor
5. Sửa dòng:
   ```javascript
   const SHEET_ID = 'YOUR_SHEET_ID_HERE';
   ```
   Thay bằng Sheet ID của bạn

6. Click **Save** (Ctrl+S)

## Bước 3: Test thử

1. Chọn function `testScrape` từ dropdown
2. Click **Run**
3. Lần đầu sẽ yêu cầu authorize - click **Review Permissions**
4. Chọn tài khoản Google
5. Click **Advanced** > **Go to [Project Name] (unsafe)**
6. Click **Allow**
7. Xem logs: **View** > **Logs**

Nếu thành công, bạn sẽ thấy giá cà phê trong logs và trong Google Sheet.

## Bước 4: Setup Trigger (Chạy tự động)

1. Click icon **Triggers** (⏰) bên trái
2. Click **Add Trigger**
3. Cấu hình:
   - **Choose which function to run**: `scrapeCoffeePrices`
   - **Choose which deployment should run**: `Head`
   - **Select event source**: `Time-driven`
   - **Select type of time based trigger**: `Minutes timer`
   - **Select minute interval**: `Every 10 minutes`
4. Click **Save**

## Bước 5: Deploy Web App (API)

1. Click **Deploy** > **New deployment**
2. Click icon ⚙️ > **Web app**
3. Cấu hình:
   - **Description**: Coffee Price API
   - **Execute as**: Me
   - **Who has access**: Anyone
4. Click **Deploy**
5. Copy **Web app URL** (ví dụ: `https://script.google.com/macros/s/ABC123/exec`)

## Bước 6: Test API

Mở browser và truy cập URL vừa copy:
```
https://script.google.com/macros/s/ABC123/exec
```

Bạn sẽ nhận được JSON:
```json
{
  "source": "giacaphe.com",
  "date": "2026-02-11 14:29:24",
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
  "unit": "VNĐ/kg"
}
```

## Bước 7: Sử dụng API

### Trong Google Apps Script khác:

```javascript
function getCoffeePrice() {
  const apiUrl = "https://script.google.com/macros/s/ABC123/exec";
  
  const response = UrlFetchApp.fetch(apiUrl);
  const data = JSON.parse(response.getContentText());
  
  let message = "☕ Giá cà phê hôm nay:\n";
  message += `Đắk Lắk: ${data.prices["Đắk Lắk"]} (${data.changes["Đắk Lắk"]})\n`;
  message += `Lâm Đồng: ${data.prices["Lâm Đồng"]} (${data.changes["Lâm Đồng"]})\n`;
  message += `Gia Lai: ${data.prices["Gia Lai"]} (${data.changes["Gia Lai"]})\n`;
  message += `Đắk Nông: ${data.prices["Đắk Nông"]} (${data.changes["Đắk Nông"]})\n`;
  
  return message;
}
```

### Trong JavaScript (website):

```javascript
fetch('https://script.google.com/macros/s/ABC123/exec')
  .then(response => response.json())
  .then(data => {
    console.log('Giá cà phê:', data);
  });
```

### Trong Python:

```python
import requests

response = requests.get('https://script.google.com/macros/s/ABC123/exec')
data = response.json()
print(data)
```

## Lưu ý

### ⚠️ Giới hạn của Google Apps Script

- **Trigger**: Tối đa 90 phút runtime/ngày
- **URL Fetch**: 20,000 requests/ngày
- **Execution time**: 6 phút/lần chạy

Với scraper chạy mỗi 10 phút:
- 144 lần/ngày × ~10 giây/lần = ~24 phút/ngày ✅ (dưới 90 phút)

### 🔄 Nếu bị Cloudflare chặn

Google Apps Script có thể bị Cloudflare chặn. Nếu gặp lỗi:

**Giải pháp**: Gọi API từ server khác (Python/Node.js) rồi lưu vào Google Sheets:

1. Chạy Python scraper trên máy local
2. Gửi kết quả đến Google Apps Script endpoint
3. Apps Script lưu vào Sheets và serve API

## Troubleshooting

### Lỗi "Authorization required"
- Chạy lại function `testScrape` và authorize

### Không tìm thấy giá
- Cloudflare có thể đang chặn
- Xem logs để debug

### Trigger không chạy
- Kiểm tra **Executions** để xem lỗi
- Có thể cần authorize lại

## Kết hợp với Telegram Bot

Update code Telegram bot của bạn:

```javascript
const apiUrl = "https://script.google.com/macros/s/ABC123/exec";
```

Thay vì gọi `https://api-caphe.bug.edu.vn/api/coffee-prices`

---

## 🎉 Hoàn thành!

Bây giờ bạn có:
- ✅ Scraper chạy tự động mỗi 10 phút
- ✅ API endpoint miễn phí
- ✅ Lịch sử giá lưu trong Google Sheets
- ✅ Hoàn toàn miễn phí, không giới hạn
