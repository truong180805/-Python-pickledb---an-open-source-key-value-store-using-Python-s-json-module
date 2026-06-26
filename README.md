# PickleDB - Kho Lưu Trữ Khóa-Giá Trị Nhẹ Với JSON

Một giải pháp lưu trữ dữ liệu nhẹ, đơn giản và mạnh mẽ dựa trên JSON. Hỗ trợ sao lưu Master-Slave qua mạng.

## 🌟 Tính Năng

- **Lưu trữ Khóa-Giá trị**: Lưu trữ dữ liệu dưới dạng cặp key-value
- **JSON Format**: Sử dụng định dạng JSON tiêu chuẩn, dễ đọc và dễ sửa đổi
- **Auto Dump**: Tự động lưu dữ liệu xuống đĩa sau mỗi thao tác (tùy chọn)
- **Master-Slave Replication**: Đồng bộ dữ liệu giữa máy Master và Slave qua HTTP
- **Lightweight**: Không cần cài đặt database phức tạp, chỉ là file JSON
- **REST API**: Truy cập dữ liệu thông qua HTTP endpoints

## 📦 Cài Đặt

### Yêu Cầu
- Python 3.6+
- Flask (cho chức năng server)
- Requests (cho Master-Slave replication)

### Cài đặt Dependencies

```bash
pip install flask requests
```

## 🚀 Cách Sử Dụng

### 1. Sử Dụng PickleDB Cơ Bản (Local)

```python
import pickledb

# Tạo hoặc mở cuốn sổ
db = pickledb.load('master.json', auto_dumps=True)

# Lưu dữ liệu
db.set('tên', 'Nguyễn Văn A')
db.set('tuổi', 25)
db.set('email', 'a@example.com')

# Đọc dữ liệu
print(db.get('tên'))  # Output: Nguyễn Văn A
print(db.get('tuổi')) # Output: 25

# Lưu thủ công (nếu auto_dumps=False)
db.dump()
```

### 2. Chạy Server (Flask API)

**Chạy máy Master** (có khả năng sao lưu sang Slave):
```bash
python server.py --mode master
```

**Chạy máy Slave** (nhận dữ liệu từ Master):
```bash
python server.py --mode slave --master_url http://localhost:5000
```

### 3. Sử Dụng REST API

#### Set Data (Lưu dữ liệu)
```bash
curl -X POST http://localhost:5000/set \
  -H "Content-Type: application/json" \
  -d '{"key":"name", "value":"John Doe"}'
```

#### Get Data (Đọc dữ liệu)
```bash
curl http://localhost:5000/get/name
```

#### Delete Data (Xóa dữ liệu)
```bash
curl -X DELETE http://localhost:5000/delete/name
```

#### Get All Data (Lấy toàn bộ dữ liệu)
```bash
curl http://localhost:5000/getall
```

## 📊 Cấu Trúc Dữ Liệu

Dữ liệu được lưu trữ dưới dạng JSON đơn giản:

```json
{
  "name": "John Doe",
  "age": 25,
  "email": "john@example.com",
  "active": true
}
```

## 🏗️ Kiến Trúc Master-Slave

```
┌─────────────┐          HTTP           ┌─────────────┐
│   Master    │◄────────────────────────►│    Slave    │
│ (Port 5000) │    POST /set_replica    │ (Port 5001) │
└─────────────┘                         └─────────────┘
      ▲
      │ Receive write requests
      │
┌─────▼──────┐
│   Client   │
└────────────┘
```

Khi Master nhận yêu cầu ghi (`/set`), nó sẽ:
1. Lưu dữ liệu vào file của mình
2. Tự động gửi yêu cầu đến Slave để đồng bộ

## 📝 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/set` | Lưu cặp khóa-giá trị (Master) |
| GET | `/get/<key>` | Đọc giá trị theo khóa |
| DELETE | `/delete/<key>` | Xóa một khóa |
| GET | `/getall` | Lấy tất cả dữ liệu |
| POST | `/set_replica` | Nhận lệnh đồng bộ từ Master (Slave) |

## 🧪 Chạy Test

```bash
# Test cục bộ
python test_local.py

# Test mạng (cần chạy server trước)
python test_network.py
python test_network2.py
```

## 📂 Cấu Trúc Thư Mục

```
.
├── pickledb.py          # Module chính
├── server.py            # Server Flask với hỗ trợ Master-Slave
├── router.py            # Định tuyến API
├── master.json          # Dữ liệu của Master
├── slave.json           # Dữ liệu của Slave
├── shard1.json          # Dữ liệu shard 1 (nếu cần phân chia)
├── shard2.json          # Dữ liệu shard 2 (nếu cần phân chia)
├── test_local.py        # Test cục bộ
├── test_network.py      # Test mạng (Master)
├── test_network2.py     # Test mạng (Slave)
└── README.md            # Tài liệu này
```

## 💡 Ví Dụ Thực Tế

### Ví dụ 1: Ứng dụng Danh bạ Địa chỉ

```python
import pickledb

# Tạo danh bạ
contacts = pickledb.load('contacts.json', auto_dumps=True)

# Thêm liên hệ
contacts.set('phone_001', {'name': 'Bạn A', 'phone': '0123456789'})
contacts.set('phone_002', {'name': 'Bạn B', 'phone': '0987654321'})

# Lấy thông tin
info = contacts.get('phone_001')
print(f"Tên: {info['name']}, SĐT: {info['phone']}")
```

### Ví dụ 2: Ứng dụng Cấu hình

```python
import pickledb

# Lưu cấu hình ứng dụng
config = pickledb.load('config.json', auto_dumps=True)

config.set('app_name', 'My Application')
config.set('version', '1.0.0')
config.set('debug', False)

# Lấy cấu hình
print(f"App: {config.get('app_name')} v{config.get('version')}")
```

## ⚙️ Cấu Hình

### Auto Dumps

- **True**: Tự động lưu sau mỗi thao tác `set()` (chậm hơn nhưng an toàn)
- **False**: Lưu thủ công bằng `db.dump()` (nhanh hơn nhưng dễ mất dữ liệu)

```python
# Tự động lưu
db = pickledb.load('data.json', auto_dumps=True)

# Hoặc lưu thủ công
db = pickledb.load('data.json', auto_dumps=False)
db.set('key', 'value')
db.dump()  # Lưu chủ động
```

## ⚠️ Hạn Chế

- Không phù hợp với dữ liệu quá lớn (>100MB)
- Không hỗ trợ các truy vấn phức tạp như SQL
- Không có bảo mật mã hóa (dữ liệu lưu dưới dạng JSON thuần)
- Hiệu suất thấp với số lượng key quá lớn

## 🎯 Trường Hợp Sử Dụng

✅ **Phù hợp cho**:
- Ứng dụng nhỏ, dự án cá nhân
- Cấu hình ứng dụng
- Cache dữ liệu tạm thời
- Danh bạ, todolist
- Nguyên mẫu nhanh (prototype)

❌ **Không phù hợp cho**:
- Ứng dụng lớn quy mô cao
- Dữ liệu nhiều > 100MB
- Truy vấn phức tạp
- Nhiều người dùng đồng thời

## 📄 Giấy Phép

Open Source - Tự do sử dụng

## 🤝 Đóng Góp

Mọi đóng góp, phát triển tính năng mới được chào đón!

---
## Báo cáo sản phẩm: https://drive.google.com/file/d/1kxtcTPaEcF5R5haykLTxmwOMemZfZ4ZK/view?usp=sharing
## Demo sản phẩm: https://drive.google.com/file/d/19x2izuC8haqBcU_1MXEIEuix6bhftg5H/view?usp=sharing

**Tác giả**: PickleDB Contributors  
**Phiên bản**: 1.0.0  
**Cập nhật lần cuối**: 2026-06-22
