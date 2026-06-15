import requests
import time

print("--- ĐÓNG VAI NGƯỜI DÙNG GỬI DỮ LIỆU ---")

# Chúng ta sẽ gửi dữ liệu vào cổng 5000 (Máy Master)
MASTER_URL = "http://127.0.0.1:5000"

data_to_send = {
    "key": "MonHoc",
    "value": "Ung dung phan tan - 10 diem"
}

print(f"1. Đang gửi dữ liệu: {data_to_send} tới Master...")
try:
    response = requests.post(f"{MASTER_URL}/set", json=data_to_send)
    print(f"2. Máy chủ phản hồi: {response.json()}")
except requests.exceptions.ConnectionError:
    print("LỖI: Không thể kết nối. Bạn đã bật máy chủ ở cổng 5000 chưa?")

print("--- HOÀN TẤT ---")