import requests

# Bây giờ người dùng KHÔNG gửi thẳng vào server nữa, mà gửi vào ROUTER (Cổng 6000)
ROUTER_URL = "http://127.0.0.1:6000"

# Dữ liệu 1: Key "MSSV" (4 ký tự -> Số chẵn -> Phải vào Shard 1)
data_chan = {"key": "MSSV", "value": "123456"}

# Dữ liệu 2: Key "Mon" (3 ký tự -> Số lẻ -> Phải vào Shard 2)
data_le = {"key": "Mon", "value": "Ung dung phan tan"}

print("--- BẮT ĐẦU GỬI DỮ LIỆU QUA TRẠM ĐIỀU PHỐI ---")

print("\n1. Gửi dữ liệu có Key CHẴN:")
res_chan = requests.post(f"{ROUTER_URL}/set", json=data_chan)
print(res_chan.json())

print("\n2. Gửi dữ liệu có Key LẺ:")
res_le = requests.post(f"{ROUTER_URL}/set", json=data_le)
print(res_le.json())