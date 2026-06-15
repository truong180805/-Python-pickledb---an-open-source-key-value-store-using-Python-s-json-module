# Gọi "cuốn sổ tay" mà chúng ta vừa tự viết ở file pickledb.py
import pickledb
import os

print("--- BẮT ĐẦU BÀI KIỂM TRA ---")

# 1. Mở một cuốn sổ mới tên là 'test_sotay.json'
# Tham số True nghĩa là: Cứ viết chữ nào vào là tự động lưu xuống ổ cứng luôn.
db = pickledb.load('test_sotay.json', True)

# 2. Ghi thử dữ liệu vào sổ
print("1. Đang ghi dữ liệu vào sổ...")
db.set('SinhVien_01', 'Nguyen Van A')
db.set('SinhVien_02', 'Tran Thi B')

# 3. Đọc thử dữ liệu ra màn hình
print("2. Đang đọc dữ liệu từ sổ...")
sv1 = db.get('SinhVien_01')
sv2 = db.get('SinhVien_02')
print(f"   -> Tìm thấy: Mã SinhVien_01 là {sv1}")
print(f"   -> Tìm thấy: Mã SinhVien_02 là {sv2}")

# 4. Kiểm tra xem file đã được tạo trên máy tính chưa
print("3. Kiểm tra ổ cứng...")
if os.path.exists('test_sotay.json'):
    print("   -> TUYỆT VỜI! File 'test_sotay.json' đã được tạo thành công.")
else:
    print("   -> LỖI: Không tìm thấy file.")

print("--- KẾT THÚC BÀI KIỂM TRA ---")