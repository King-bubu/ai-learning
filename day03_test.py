import requests

BASE = "http://localhost:8000"

r = requests.post(f"{BASE}/chat", json={"question": "用一句话解释什么是API"})
print("状态码:", r.status_code)
print("返回:", r.json())
print(r.url)
