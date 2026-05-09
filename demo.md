# Demo Project

## 1. Chuan bi moi truong

Mo terminal tai thu muc goc du an:

```powershell
cd D:\nghich\webtruong
```

Neu chay bang Docker:

```powershell
docker-compose up -d --build
docker exec -it vnu_research_backend alembic upgrade head
docker exec -it vnu_research_backend python seed_data.py
```

Neu chay local:

```powershell
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd backend
..\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Mo terminal khac de chay frontend:

```powershell
cd D:\nghich\webtruong\frontend\vnu-frontend
npm install
npm run dev
```

Duong dan demo:

```text
Frontend: http://127.0.0.1:5173
API docs: http://127.0.0.1:8000/docs
Health check: http://127.0.0.1:8000/health
```

## 2. Demo tinh nang tra cuu cong khai

Mo frontend:

```text
http://127.0.0.1:5173
```

Can demo cac y sau:

- Trang web danh cho doanh nghiep, sinh vien, giang vien tra cuu tai lieu khoa hoc cua truong.
- Nguoi dung khong can dang nhap van co the tim kiem.
- Co the loc theo loai tai lieu, linh vuc, nam thuc hien, thanh phan thuc hien.
- Ket qua hien thi ten de tai, chu nhiem, linh vuc, nam, trang thai, tom tat, tu khoa.

Cac tu khoa nen thu:

```text
tri tue nhan tao
bien doi khi hau
cong nghe thong tin
blockchain
kinh te so
```

Can noi ro:

- He thong ho tro tim kiem tieng Viet co dau va khong dau.
- Vi du `tri tue nhan tao` van tim duoc de tai co chu `tri tue nhan tao` trong du lieu.
- Nut logo truong co the bam de quay ve trang chu.

## 3. Demo API bang Swagger

Mo:

```text
http://127.0.0.1:8000/docs
```

Demo cac API public:

```text
GET /health
GET /api/v1/projects/search
GET /api/v1/filters
```

Thu query:

```text
/api/v1/projects/search?q=tri%20tue%20nhan%20tao
/api/v1/projects/search?q=bien%20doi%20khi%20hau
```

Can noi ro:

- Backend dung FastAPI.
- API tra JSON chuan gom `status`, `data.total`, `data.items`.
- Frontend React goi API nay de hien thi ket qua.

## 4. Demo dang nhap admin

Mo trang admin tren frontend:

```text
http://127.0.0.1:5173/admin
```

Neu chua co tai khoan, dang ky tai khoan dau tien. Tai khoan dau tien se co role `admin`.

Demo API auth trong Swagger:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET /api/v1/auth/me
```

Can noi ro:

- Mat khau duoc hash bang bcrypt, khong luu plain text.
- Sau khi login, server tra JWT access token.
- Cac API them, sua, xoa du lieu yeu cau quyen admin.

## 5. Demo CRUD du lieu cho admin

Trong Swagger, bam `Authorize` va nhap token:

```text
Bearer <access_token>
```

Demo cac API admin:

```text
POST /api/v1/projects
PUT /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}
```

Kich ban demo:

- Tao mot cong trinh nghien cuu moi.
- Tim kiem lai tren frontend de thay du lieu moi.
- Sua nam hoac trang thai cua cong trinh.
- Tim kiem lai de thay du lieu da cap nhat.
- Xoa cong trinh demo.

Can noi ro:

- CRUD duoc bao ve bang JWT va role admin.
- Khi them, sua, xoa, cache search se duoc clear de tranh tra du lieu cu.

## 6. Demo hieu nang bang Locust

Tao thu muc report:

```powershell
mkdir reports
```

Neu dung Redis cache, reset thong ke truoc khi test:

```powershell
docker exec vnu_research_redis redis-cli FLUSHSTATS
```

Chay Locust headless:

```powershell
.\venv\Scripts\locust.exe -f locustfile.py --host http://localhost:8000 --users 50 --spawn-rate 5 --run-time 5m --headless --csv reports\locust_50u_5m --html reports\locust_50u_5m.html
```

Mo report:

```text
reports/locust_50u_5m.html
```

Can ghi lai cac chi so:

```text
So user ao: 50
Thoi gian test: 5 phut
RPS trung binh: lay cot Requests/s
Latency P50: lay cot 50%
Latency P95: lay cot 95%
Latency P99: lay cot 99%
Ti le loi: Failures / Requests * 100%
```

Lay cache hit/miss:

```powershell
docker exec vnu_research_redis redis-cli INFO stats
```

Tim cac dong:

```text
keyspace_hits:...
keyspace_misses:...
```

Tinh:

```text
Cache hit rate = hits / (hits + misses) * 100%
Cache miss rate = misses / (hits + misses) * 100%
```

## 7. Demo so sanh cache lanh va cache nong

Lan 1: cache lanh.

```powershell
docker exec vnu_research_redis redis-cli FLUSHDB
docker exec vnu_research_redis redis-cli FLUSHSTATS
.\venv\Scripts\locust.exe -f locustfile.py --host http://localhost:8000 --users 50 --spawn-rate 5 --run-time 3m --headless --csv reports\cold_cache --html reports\cold_cache.html
docker exec vnu_research_redis redis-cli INFO stats
```

Lan 2: cache nong.

```powershell
docker exec vnu_research_redis redis-cli FLUSHSTATS
.\venv\Scripts\locust.exe -f locustfile.py --host http://localhost:8000 --users 50 --spawn-rate 5 --run-time 3m --headless --csv reports\warm_cache --html reports\warm_cache.html
docker exec vnu_research_redis redis-cli INFO stats
```

Can noi ro:

- Cache lanh: lan dau chua co du lieu cache, miss cao hon.
- Cache nong: cac query lap lai da co trong Redis, hit cao hon.
- Neu cache hoat dong tot thi latency P50/P95 thuong se giam.

## 8. Mau bang ket qua de dua vao bao cao

| Kich ban | User ao | Thoi gian | RPS TB | P50 | P95 | P99 | Ti le loi | Cache hit | Cache miss | Hit rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Cache lanh | 50 | 3 phut | ... | ... ms | ... ms | ... ms | ...% | ... | ... | ...% |
| Cache nong | 50 | 3 phut | ... | ... ms | ... ms | ... ms | ...% | ... | ... | ...% |

## 9. Thu tu demo de thuyet trinh

1. Gioi thieu muc tieu: cong thong tin tra cuu cong trinh nghien cuu cua truong.
2. Mo frontend va tim kiem thu bang tieng Viet khong dau.
3. Loc ket qua theo loai tai lieu, linh vuc, nam.
4. Mo Swagger de cho thay API public.
5. Dang nhap admin va demo API auth.
6. Demo them, sua, xoa mot ban ghi.
7. Chay Locust hoac mo report Locust da chay truoc.
8. Trinh bay bang so lieu RPS, latency, error rate, cache hit/miss.
9. Ket luan: he thong co frontend, backend API, auth, CRUD admin, cache, monitoring va load test.

