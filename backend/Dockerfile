# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết cho việc biên dịch
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Build wheels thay vì install trực tiếp để tái sử dụng ở stage sau
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Chỉ cài library cần thiết lúc chạy (Không cần gcc)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels từ builder và cài đặt
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy mã nguồn
COPY . .

EXPOSE 8000

# Khởi chạy server theo chuẩn modular (app.main:app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
