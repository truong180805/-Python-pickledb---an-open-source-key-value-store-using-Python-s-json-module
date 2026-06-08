import pickledb
import requests
from flask import Flask, request, jsonify
import argparse

app = Flask(__name__)
db = None
REPLICA_URL = None

@app.route('/set', methods=['POST'])
def set_data():
    """Nhận dữ liệu từ người dùng và lưu vào máy chủ hiện tại. Đồng bộ sang Slave nếu là Master."""
    data = request.json
    key = data.get('key')
    value = data.get('value')

    # Lưu vào pickledb của máy chủ này
    db.set(key, value)
    db.dump()

    # Đồng bộ sang Slave
    if REPLICA_URL:
        try:
            requests.post(f"{REPLICA_URL}/set_replica", json={"key": key, "value": value})
            return jsonify({"message": "Đã lưu tại Master và đồng bộ sang Slave thành công!", "key": key}), 200
        except Exception as e:
            return jsonify({"message": f"Đã lưu tại Master nhưng lỗi đồng bộ: {str(e)}"}), 500
            
    return jsonify({"message": "Đã lưu thành công!", "key": key}), 200

@app.route('/set_replica', methods=['POST'])
def set_replica_data():
    """Dành riêng cho Slave nhận dữ liệu từ Master."""
    data = request.json
    db.set(data['key'], data['value'])
    db.dump()
    return jsonify({"message": "Slave đã cập nhật dữ liệu!"}), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--db_file', type=str, default='master.db')
    parser.add_argument('--replica_url', type=str, default=None)
    args = parser.parse_args()

    db = pickledb.load(args.db_file, False)
    REPLICA_URL = args.replica_url

    print(f"Khởi động Server tại cổng {args.port}, database: {args.db_file}")
    app.run(port=args.port)