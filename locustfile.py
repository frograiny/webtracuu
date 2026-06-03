from locust import HttpUser, task, between
import random

class VNUResearchUser(HttpUser):
    # Thời gian chờ giữa các task của mỗi user (1 đến 5 giây)
    wait_time = between(1, 5)

    @task(5)
    def search_projects(self):
        """Giả lập user gõ tìm kiếm liên tục (chủ yếu test FTS + Trigram)"""
        queries = [
            "AI y hoc", 
            "tri tue nhan tao", 
            "cong nghe thong tin", 
            "nghien cuu ung dung",
            "khoa hoc may tinh",
            "dai hoc quoc gia",
            "blckchain", # Sai chính tả
        ]
        query = random.choice(queries)
        
        # Test endpoint có rate limit và cache
        with self.client.get(f"/api/v1/projects/search?q={query}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 429:
                response.success() # 429 Rate Limit là hành vi đúng đắn
            else:
                response.failure(f"Failed with status code: {response.status_code}")

    @task(1)
    def login_attempt(self):
        """Giả lập user cố gắng đăng nhập (Test Rate Limit /login)"""
        with self.client.post("/api/v1/auth/login", json={"email": "guest@test.com", "password": "wrong"}, catch_response=True) as response:
            if response.status_code in [401, 403, 429]:
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
