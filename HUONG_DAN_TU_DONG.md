# 🚀 Hướng dẫn Chạy Tự động (3 bước đơn giản)

## ✅ Bước 1: Setup Google Apps Script (5 phút)

1. Mở Google Sheets: https://sheets.google.com
2. Tạo sheet mới tên "Giá Cà Phê"
3. Vào **Extensions > Apps Script**
4. Copy toàn bộ code từ file `google-apps-script/api-only.gs`
5. Paste vào Apps Script và Save
6. Click **Deploy > New deployment**
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
7. Click **Deploy** và copy URL (dạng: `https://script.google.com/macros/s/.../exec`)

## ✅ Bước 2: Setup GitHub Secret (1 phút)

1. Vào repo GitHub: https://github.com/Phusssss/caogiacaphe
2. **Settings > Secrets and variables > Actions**
3. Click **New repository secret**
4. Điền:
   - Name: `APPS_SCRIPT_URL`
   - Value: URL từ bước 1
5. Click **Add secret**

## ✅ Bước 3: Test thử (2 phút)

1. Vào tab **Actions** trên GitHub
2. Chọn workflow **"Scrape Coffee Prices"**
3. Click **Run workflow** > **Run workflow**
4. Đợi 2-3 phút
5. Kiểm tra Google Sheets xem có dữ liệu chưa

## 🎉 Xong rồi!

Từ giờ hệ thống sẽ tự động:
- Scrape giá cà phê **mỗi ngày lúc 8:00 sáng**
- Lưu vào Google Sheets
- Hoàn toàn miễn phí, không tốn tiền hosting

## 📊 Xem kết quả

- **Google Sheets**: Xem dữ liệu lịch sử
- **GitHub Actions**: Xem logs và kết quả chạy

## ⚙️ Thay đổi lịch chạy (tùy chọn)

Sửa file `.github/workflows/scrape-coffee-prices.yml`:

```yaml
schedule:
  # Chạy mỗi 6 giờ
  - cron: '0 */6 * * *'
  
  # Chạy 2 lần/ngày (8:00 và 20:00)
  - cron: '0 1,13 * * *'
```

## 🆘 Gặp lỗi?

### Lỗi: "Không tìm đủ dữ liệu giá"

Website giacaphe.com có thể đã thay đổi cấu trúc. Workflow sẽ tự động thử 2 phương pháp:
1. Playwright (chậm nhưng bypass được Cloudflare)
2. Simple requests (nhanh nhưng có thể bị chặn)

Để kiểm tra:
1. Vào **Actions** > Click vào workflow run bị lỗi
2. Download **debug-files** artifact
3. Mở file `debug_screenshot_1.png` để xem trang web
4. Mở file `debug_fail_attempt_1.html` để xem HTML

### Lỗi: "APPS_SCRIPT_URL not found"

- Kiểm tra đã thêm secret `APPS_SCRIPT_URL` chưa
- Secret name phải viết đúng chính xác

### Lỗi: "403 Forbidden" khi gửi lên Apps Script

- Kiểm tra Apps Script deployment:
  - Execute as: **Me**
  - Who has access: **Anyone**
- Thử deploy lại Apps Script

### Workflow không chạy tự động

- Kiểm tra GitHub Actions có bị disable không
- Repository phải là public hoặc có GitHub Pro
- Kiểm tra cron schedule trong workflow file

---

**Chi phí**: $0/tháng (hoàn toàn miễn phí) 💰

