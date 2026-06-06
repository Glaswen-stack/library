import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    req = urllib.request.Request(f"{BASE_URL}/health")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            print("✅ GET /health работает")
    except Exception as e:
        print(f"❌ Ошибка в GET /health: {e}")

if __name__ == "__main__":
    print("Запуск проверок API...")
    test_health()