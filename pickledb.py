import json
import os

def load(location, auto_dumps):
    """
    Hàm này được gọi đầu tiên để mở cuốn sổ tay.
    - location: tên file (ví dụ: 'master.json')
    - auto_dumps: Có muốn tự động lưu ngay sau khi ghi không (True/False)
    """
    return PickleDB(location, auto_dumps)

class PickleDB(object):
    def __init__(self, location, auto_dumps):
        self.location = location
        self.auto_dumps = auto_dumps
        
        # Nếu file đã tồn tại trên máy, mở ra đọc. Nếu chưa, tạo một cuốn sổ trống (dictionary)
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}

    def _loaddb(self):
        """Đọc dữ liệu từ file JSON trên ổ cứng nạp vào RAM (bộ nhớ tạm)"""
        try:
            with open(self.location, 'r') as f:
                self.db = json.load(f)
        except ValueError:
            self.db = {}

    def dump(self):
        """Hành động lấy bút viết từ RAM lưu vĩnh viễn xuống ổ cứng (file JSON)"""
        with open(self.location, 'w') as f:
            json.dump(self.db, f)
        return True

    def set(self, key, value):
        """Lưu một cặp Chìa khóa - Giá trị vào sổ"""
        self.db[str(key)] = value
        
        # Nếu cài đặt auto_dumps là True, lưu xuống ổ cứng ngay lập tức
        if self.auto_dumps:
            self.dump()
        return True

    def get(self, key):
        """Tìm và đọc giá trị theo Chìa khóa"""
        try:
            return self.db[key]
        except KeyError:
            return None