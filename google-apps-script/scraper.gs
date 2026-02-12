/**
 * Coffee Price Scraper cho Google Apps Script
 * Scrape giá từ giacaphe.com và lưu vào Google Sheets
 */

// ID của Google Sheet để lưu dữ liệu
// Tạo sheet mới tại: https://sheets.google.com
const SHEET_ID = 'YOUR_SHEET_ID_HERE'; // Thay bằng ID của sheet

/**
 * Scrape giá cà phê từ giacaphe.com
 */
function scrapeCoffeePrices() {
  const url = "https://giacaphe.com/gia-ca-phe-noi-dia/";
  
  try {
    Logger.log('Đang scrape giá cà phê...');
    
    // Fetch HTML
    const response = UrlFetchApp.fetch(url, {
      muteHttpExceptions: true,
      followRedirects: true
    });
    
    if (response.getResponseCode() !== 200) {
      Logger.log('Lỗi: ' + response.getResponseCode());
      return null;
    }
    
    const html = response.getContentText();
    
    // Tìm CSS content trong <style> tags
    const styleRegex = /<style[^>]*>([\s\S]*?)<\/style>/gi;
    let allCss = '';
    let match;
    
    while ((match = styleRegex.exec(html)) !== null) {
      allCss += match[1] + '\n';
    }
    
    // Tìm giá trong CSS ::after content
    const priceRegex = /::after\s*{\s*content:\s*'([^']+)'/g;
    const values = [];
    
    while ((match = priceRegex.exec(allCss)) !== null) {
      values.push(match[1]);
    }
    
    Logger.log('Tìm thấy ' + values.length + ' giá trị');
    
    if (values.length < 8) {
      Logger.log('Không đủ dữ liệu giá');
      return null;
    }
    
    // Parse dữ liệu
    const data = {
      source: "giacaphe.com",
      prices: {
        "Đắk Lắk": values[0],
        "Lâm Đồng": values[2],
        "Gia Lai": values[4],
        "Đắk Nông": values[6]
      },
      changes: {
        "Đắk Lắk": values[1],
        "Lâm Đồng": values[3],
        "Gia Lai": values[5],
        "Đắk Nông": values[7]
      },
      timestamp: new Date().getTime(),
      date: Utilities.formatDate(new Date(), "Asia/Ho_Chi_Minh", "yyyy-MM-dd HH:mm:ss"),
      unit: "VNĐ/kg"
    };
    
    Logger.log('Giá cà phê:');
    Logger.log(JSON.stringify(data, null, 2));
    
    // Lưu vào Google Sheets
    saveToSheet(data);
    
    return data;
    
  } catch (e) {
    Logger.log('Lỗi: ' + e.toString());
    return null;
  }
}

/**
 * Lưu dữ liệu vào Google Sheets
 */
function saveToSheet(data) {
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Prices');
    
    // Nếu sheet chưa tồn tại, tạo mới
    if (!sheet) {
      const newSheet = SpreadsheetApp.openById(SHEET_ID).insertSheet('Prices');
      // Thêm header
      newSheet.appendRow(['Timestamp', 'Date', 'Đắk Lắk', 'Lâm Đồng', 'Gia Lai', 'Đắk Nông', 
                          'Change ĐL', 'Change LĐ', 'Change GL', 'Change ĐN']);
    }
    
    const targetSheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Prices');
    
    // Thêm dòng mới
    targetSheet.appendRow([
      data.timestamp,
      data.date,
      data.prices["Đắk Lắk"],
      data.prices["Lâm Đồng"],
      data.prices["Gia Lai"],
      data.prices["Đắk Nông"],
      data.changes["Đắk Lắk"],
      data.changes["Lâm Đồng"],
      data.changes["Gia Lai"],
      data.changes["Đắk Nông"]
    ]);
    
    // Cập nhật sheet "Latest" với giá mới nhất
    updateLatestSheet(data);
    
    Logger.log('Đã lưu vào Google Sheets');
    
  } catch (e) {
    Logger.log('Lỗi khi lưu vào sheet: ' + e.toString());
  }
}

/**
 * Cập nhật sheet Latest với giá mới nhất
 */
function updateLatestSheet(data) {
  try {
    let sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Latest');
    
    // Nếu sheet chưa tồn tại, tạo mới
    if (!sheet) {
      sheet = SpreadsheetApp.openById(SHEET_ID).insertSheet('Latest');
      sheet.appendRow(['Field', 'Value']);
    } else {
      sheet.clear();
      sheet.appendRow(['Field', 'Value']);
    }
    
    // Thêm dữ liệu
    sheet.appendRow(['Date', data.date]);
    sheet.appendRow(['Đắk Lắk', data.prices["Đắk Lắk"]]);
    sheet.appendRow(['Đắk Lắk Change', data.changes["Đắk Lắk"]]);
    sheet.appendRow(['Lâm Đồng', data.prices["Lâm Đồng"]]);
    sheet.appendRow(['Lâm Đồng Change', data.changes["Lâm Đồng"]]);
    sheet.appendRow(['Gia Lai', data.prices["Gia Lai"]]);
    sheet.appendRow(['Gia Lai Change', data.changes["Gia Lai"]]);
    sheet.appendRow(['Đắk Nông', data.prices["Đắk Nông"]]);
    sheet.appendRow(['Đắk Nông Change', data.changes["Đắk Nông"]]);
    
  } catch (e) {
    Logger.log('Lỗi khi cập nhật Latest sheet: ' + e.toString());
  }
}

/**
 * Web App endpoint - Trả về giá mới nhất dưới dạng JSON
 */
function doGet(e) {
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Latest');
    
    if (!sheet) {
      return ContentService.createTextOutput(JSON.stringify({
        error: "Chưa có dữ liệu"
      }))
      .setMimeType(ContentService.MimeType.JSON);
    }
    
    const data = sheet.getDataRange().getValues();
    
    // Parse dữ liệu từ sheet
    const result = {
      source: "giacaphe.com",
      date: data[1][1],
      prices: {
        "Đắk Lắk": data[2][1],
        "Lâm Đồng": data[4][1],
        "Gia Lai": data[6][1],
        "Đắk Nông": data[8][1]
      },
      changes: {
        "Đắk Lắk": data[3][1],
        "Lâm Đồng": data[5][1],
        "Gia Lai": data[7][1],
        "Đắk Nông": data[9][1]
      },
      unit: "VNĐ/kg"
    };
    
    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
    
  } catch (e) {
    return ContentService.createTextOutput(JSON.stringify({
      error: e.toString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Test function
 */
function testScrape() {
  scrapeCoffeePrices();
}
