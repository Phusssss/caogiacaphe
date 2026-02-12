/**
 * Google Apps Script - Chỉ làm API và lưu dữ liệu
 * Nhận dữ liệu từ Python scraper
 */

const SHEET_ID = '1Ril0Srxm4mfzd-lWs2a6bONaVPM4kBIDRJmSMaFzmH8';

/**
 * Lưu dữ liệu vào Google Sheets
 */
function saveToSheet(data) {
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    let sheet = ss.getSheetByName('Prices');
    
    // Nếu sheet chưa tồn tại, tạo mới
    if (!sheet) {
      sheet = ss.insertSheet('Prices');
      sheet.appendRow(['Timestamp', 'Date', 'Đắk Lắk', 'Lâm Đồng', 'Gia Lai', 'Đắk Nông', 
                       'Change ĐL', 'Change LĐ', 'Change GL', 'Change ĐN']);
    }
    
    // Thêm dòng mới
    sheet.appendRow([
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
    
    // Cập nhật sheet "Latest"
    updateLatestSheet(data);
    
    Logger.log('Đã lưu vào Google Sheets');
    return true;
    
  } catch (e) {
    Logger.log('Lỗi khi lưu vào sheet: ' + e.toString());
    return false;
  }
}

/**
 * Cập nhật sheet Latest
 */
function updateLatestSheet(data) {
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    let sheet = ss.getSheetByName('Latest');
    
    if (!sheet) {
      sheet = ss.insertSheet('Latest');
      sheet.appendRow(['Field', 'Value']);
    } else {
      sheet.clear();
      sheet.appendRow(['Field', 'Value']);
    }
    
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
    Logger.log('Lỗi khi cập nhật Latest: ' + e.toString());
  }
}

/**
 * Endpoint nhận dữ liệu từ Python (POST)
 */
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    
    if (saveToSheet(data)) {
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        message: "Đã lưu dữ liệu"
      }))
      .setMimeType(ContentService.MimeType.JSON);
    } else {
      return ContentService.createTextOutput(JSON.stringify({
        status: "error",
        message: "Không thể lưu dữ liệu"
      }))
      .setMimeType(ContentService.MimeType.JSON);
    }
    
  } catch (e) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: e.toString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Endpoint trả về giá mới nhất (GET)
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
    
    // Parse dữ liệu
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
