import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_with_diacritics():
    r = client.get("/api/v1/projects/search", params={"q": "tri tue"})
    print(f"[Search 'tri tue'] Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()["data"]
        print(f"  Total: {data['total']}")
        for item in data["items"]:
            print(f"    - {item['tenDeTai']}")
    else:
        print(f"  ERROR: {r.text[:300]}")

def test_search_no_diacritics():
    r = client.get("/api/v1/projects/search", params={"q": "vat lieu"})
    print(f"\n[Search 'vat lieu'] Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()["data"]
        print(f"  Total: {data['total']}")
        for item in data["items"]:
            print(f"    - {item['tenDeTai']}")
    else:
        print(f"  ERROR: {r.text[:300]}")

def test_search_author():
    r = client.get("/api/v1/projects/search", params={"q": "nguyen"})
    print(f"\n[Search 'nguyen'] Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()["data"]
        print(f"  Total: {data['total']}")
        for item in data["items"]:
            print(f"    - {item['chuNhiem']}: {item['tenDeTai'][:50]}")
    else:
        print(f"  ERROR: {r.text[:300]}")

def test_search_no_query():
    r = client.get("/api/v1/projects/search")
    print(f"\n[Search empty] Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()["data"]
        print(f"  Total: {data['total']}")
    else:
        print(f"  ERROR: {r.text[:300]}")

def test_project_detail():
    r = client.get("/api/v1/projects/NCKH-2023-001")
    print(f"\n[Detail NCKH-2023-001] Status: {r.status_code}")
    if r.status_code == 200:
        item = r.json()["data"]
        print(f"  Title: {item['tenDeTai']}")
        print(f"  Author: {item['chuNhiem']}")
    else:
        print(f"  ERROR: {r.text[:300]}")

def test_project_not_found():
    r = client.get("/api/v1/projects/NONEXISTENT")
    print(f"\n[Detail NONEXISTENT] Status: {r.status_code}")
    print(f"  Response: {r.json()}")

def test_filters():
    r = client.get("/api/v1/filters/")
    print(f"\n[Filters] Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()["data"]
        print(f"  Fields: {data['fields']}")
        print(f"  Years: {data['years']}")
        print(f"  Audiences: {data['audiences']}")
        print(f"  DocumentTypes: {data.get('documentTypes', 'MISSING')}")
    else:
        print(f"  ERROR: {r.text[:300]}")

def test_search_with_filter():
    r = client.get("/api/v1/projects/search", params={"q": "blockchain", "field": "Công nghệ thông tin"})
    print(f"\n[Search 'blockchain' + field filter] Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()["data"]
        print(f"  Total: {data['total']}")
    else:
        print(f"  ERROR: {r.text[:300]}")

if __name__ == "__main__":
    test_search_with_diacritics()
    test_search_no_diacritics()
    test_search_author()
    test_search_no_query()
    test_project_detail()
    test_project_not_found()
    test_filters()
    test_search_with_filter()
    print("\n=== ALL TESTS COMPLETED ===")
