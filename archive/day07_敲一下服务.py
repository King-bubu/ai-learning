import requests

BASE = "http://localhost:8000"

r = requests.post(f"{BASE}/askf", json={"question": "我的显卡显存有多大？", "session_id": "小豪"})
print("状态码", r.status_code)
print("返回", r.json())

r1 = requests.post(f"{BASE}/ask", json={"question": "我叫小明,记住我的名字", "session_id": "小明"})
print("状态码", r1.status_code)
print("A", r1.json())

r2 = requests.post(BASE+"/ask", json={"question": "请问我叫什么名字？", "session_id": "小豪"})
print("状态码", r2.status_code)
print("B", r2.json())

r3 = requests.post(f"{BASE}/ask", json={"question": "请问我叫什么名字？", "session_id": "小明"})
print("状态码", r1.status_code)
print("A", r1.json())