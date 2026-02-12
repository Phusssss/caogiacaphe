# Hướng dẫn Setup Tự động Scrape và Gửi lên Google Sheets

## Tổng quan

Hệ thống sẽ hoạt động như sau:
1. **GitHub Actions** tự động scrape giá cà phê mỗi ngày lúc 8:00 sáng
2. Gửi dữ liệu lên **Google Apps Script**
3. Google Apps Script lưu vào **Google Sheets**

## Bước 1: Setup Google Apps Script

### 1.1. Tạo Google Sheet

1. Vào https://sheets.google.com
2. Tạo sheet mới tên "Giá Cà Phê"
3. Tạo các cột: `Ngày | Đắk Lắk | Lâm Đồng | Gia Lai | Đắk Nông`

### 1.2. Tạo Apps Script

1. Trong Google Sheet, vào **Extensions > Apps Script**
2. Copy code từ file `google-apps-script/api-only.gs`
3. Paste vào Apps Script editor
4. Save (Ctrl+S)

### 1.3. Deploy Web App

1. Click **Deploy > New deployment**
2. Chọn type: **Web app**
3. Cấu hình:
   - Description: "Coffee Price API"
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Click **Deploy**
5. Copy **Web app URL** (dạng: `https://script.google.com/macros/s/...../exec`)

## Bước 2: Setup GitHub Actions

### 2.1. Thêm Secret

1. Vào GitHub repository: https://github.com/Phusssss/caogiacaphe
2. Vào **Settings > Secrets and variables > Actions**
3. Click **New repository secret**
4. Thêm secret:
   - Name: `APPS_SCRIPT_URL`
   - Value: URL từ bước 1.3 (Web app URL)
5. Click **Add secret**

### 2.2. Enable GitHub Actions

1. Vào tab **Actions** trên GitHub
2. Nếu bị disable, click **Enable Actions**
3. Workflow sẽ tự động chạy mỗi ngày lúc 8:00 sáng

### 2.3. Test chạy thủ công

1. Vào tab **Actions**
2. Chọn workflow **"Scrape Coffee Prices"**
3. Click **Run workflow**
4. Chọn branch `main`
5. Click **Run workflow**
6. Đợi vài phút và xem kết quả

## Bước 3: Kiểm tra kết quả

### 3.1. Xem logs GitHub Actions

1. Vào tab **Actions**
2. Click vào workflow run mới nhất
3. Click vào job **"scrape"**
4. Xem logs để kiểm tra:
   - ✓ Scrape thành công
   - ✓ Gửi lên Google Sheets thành công

### 3.2. Kiểm tra Google Sheets

1. Mở Google Sheet
2. Xem dữ liệu mới được thêm vào
3. Kiểm tra ngày giờ có đúng không

## Lịch chạy tự động

Workflow sẽ chạy:
- **Mỗi ngày lúc 8:00 sáng** (giờ Việt Nam)
- Hoặc **chạy thủ công** bất cứ lúc nào từ tab Actions

## Troubleshooting

### Lỗi: "APPS_SCRIPT_URL not found"

- Kiểm tra đã thêm secret `APPS_SCRIPT_URL` chưa
- Secret name phải viết đúng chính xác

### Lỗi: "403 Forbidden" khi gửi lên Apps Script

- Kiểm tra Apps Script deployment:
  - Execute as: **Me**
  - Who has access: **Anyone**
- Thử deploy lại Apps Script

### Lỗi: Scraper không lấy được dữ liệu

- Có thể website giacaphe.com thay đổi cấu trúc
- Xem logs chi tiết trong GitHub Actions
- Download debug HTML file từ Artifacts

### Workflow không chạy tự động

- Kiểm tra GitHub Actions có bị disable không
- Repository phải là public hoặc có GitHub Pro
- Kiểm tra cron schedule trong workflow file

## Nâng cao

### Thay đổi lịch chạy

Sửa file `.github/workflows/scrape-coffee-prices.yml`:

```yaml
schedule:
  # Chạy mỗi 6 giờ
  - cron: '0 */6 * * *'
  
  # Chạy 2 lần/ngày (8:00 và 14:00)
  - cron: '0 1,7 * * *'
```

### Gửi thông báo khi có lỗi

Thêm step vào workflow:

```yaml
- name: Send notification on failure
  if: failure()
  run: |
    curl -X POST https://your-webhook-url \
      -d "Scraper failed at $(date)"
```

## Chi phí

- **GitHub Actions**: Miễn phí (2000 phút/tháng cho public repo)
- **Google Apps Script**: Miễn phí
- **Google Sheets**: Miễn phí

Tổng chi phí: **$0/tháng** 🎉

