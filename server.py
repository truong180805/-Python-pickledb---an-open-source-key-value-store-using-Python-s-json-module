import pickledb
import requests
from flask import Flask, request, jsonify
import argparse

app = Flask(__name__)

# Biến toàn cục để lưu trữ trạng thái của database và địa chỉ máy Phụ
db = None
REPLICA_URL = None

@app.route('/set', methods=['POST'])
def set_data():
    """
    Dành cho người dùng: Nhận dữ liệu, lưu vào máy hiện tại.
    Nếu máy này là Master (có REPLICA_URL), nó sẽ tự động chép sang Slave.
    """
    data = request.json
    key = data.get('key')
    value = data.get('value')

    # 1. Lưu vào sổ của máy hiện tại
    db.set(key, value)

    # 2. Nếu là Master, gửi bản sao sang máy Slave
    if REPLICA_URL:
        try:
            # Gửi một HTTP request sang đường dẫn /set_replica của máy Slave
            requests.post(f"{REPLICA_URL}/set_replica", json={"key": key, "value": value})
            return jsonify({"message": "Đã lưu tại Master và đồng bộ sang Slave thành công!", "key": key}), 200
        except Exception as e:
            return jsonify({"message": f"Đã lưu tại Master nhưng lỗi kết nối Slave: {str(e)}"}), 500
            
    return jsonify({"message": "Đã lưu thành công!", "key": key}), 200

@app.route('/set_replica', methods=['POST'])
def set_replica_data():
    """
    Dành riêng cho máy Phụ (Slave): Nhận lệnh đồng bộ từ Master và chép vào sổ.
    Người dùng bình thường không gọi vào đường dẫn này.
    """
    data = request.json
    db.set(data['key'], data['value'])
    return jsonify({"message": "Slave đã cập nhật bản sao!"}), 200

@app.route('/get/<key>', methods=['GET'])
def get_data(key):
    """Đọc dữ liệu từ cuốn sổ của máy hiện tại"""
    value = db.get(key)
    if value:
        return jsonify({"key": key, "value": value}), 200
    return jsonify({"message": "Không tìm thấy dữ liệu"}), 404

if __name__ == '__main__':
    # Thiết lập để có thể truyền tham số qua Terminal khi chạy
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help="Cổng chạy server (VD: 5000)")
    parser.add_argument('--db_file', type=str, default='data.json', help="Tên file sổ tay")
    parser.add_argument('--replica_url', type=str, default=None, help="Link máy Slave (Nếu đây là Master)")
    args = parser.parse_args()

    # Mở cuốn sổ tay (True = tự động lưu)
    db = pickledb.load(args.db_file, True)
    REPLICA_URL = args.replica_url

    print(f"[*] Khởi động Server tại cổng {args.port}")
    print(f"[*] Dữ liệu lưu tại file: {args.db_file}")
    if REPLICA_URL:
        print(f"[*] Chế độ MASTER: Đã thiết lập đồng bộ tới Slave tại {REPLICA_URL}")
    else:
        print(f"[*] Chế độ ĐỘC LẬP / SLAVE")
        
    # Chạy máy chủ
    app.run(port=args.port)