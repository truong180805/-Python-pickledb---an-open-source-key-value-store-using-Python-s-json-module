import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Định nghĩa địa chỉ của 2 Chi nhánh (Shard)
SHARD_1 = "http://127.0.0.1:5001"  # Dành cho Key chẵn
SHARD_2 = "http://127.0.0.1:5002"  # Dành cho Key lẻ

def get_shard_url(key):
    """Thuật toán phân mảnh: Chẵn vào Shard 1, Lẻ vào Shard 2"""
    if len(key) % 2 == 0:
        return SHARD_1
    else:
        return SHARD_2

@app.route('/set', methods=['POST'])
def route_set_data():
    """Nhận dữ liệu từ người dùng và điều hướng (route) tới đúng Shard"""
    data = request.json
    key = data.get('key')
    
    # 1. Xác định Chi nhánh (Shard) sẽ chịu trách nhiệm lưu trữ
    target_shard = get_shard_url(key)
    
    # 2. Chuyển tiếp (Forward) dữ liệu sang Chi nhánh đó
    try:
        # Lưu ý: Chúng ta gọi thẳng vào API '/set' của tệp server.py đã viết lúc trước
        response = requests.post(f"{target_shard}/set", json=data)
        return jsonify({
            "message": "Trạm điều phối đã phân luồng thành công!",
            "shard_luu_tru": target_shard,
            "ket_qua_tu_shard": response.json()
        }), 200
    except Exception as e:
        return jsonify({"message": f"Lỗi không thể kết nối tới Shard: {str(e)}"}), 500

if __name__ == '__main__':
    print("[*] Khởi động ROUTER (Trạm điều phối) tại cổng 6000")
    print(f"[*] Shard 1 (Key Chẵn) đang đợi ở cổng 5001")
    print(f"[*] Shard 2 (Key Lẻ) đang đợi ở cổng 5002")
    
    # Router sẽ chạy ở một cổng hoàn toàn khác (6000) để không đụng hàng
    app.run(port=6000)