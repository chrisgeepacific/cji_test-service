FROM python:3.11.7-slim

# Cài đặt các phụ thuộc hệ thống
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép requirements.txt vào container
COPY requirements.txt .

# Cài đặt các phụ thuộc Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ code của ứng dụng vào container
COPY . .


ENV PYTHONPATH=/app

# Mở cổng mà ứng dụng sẽ lắng nghe
EXPOSE 8080

# Khởi chạy ứng dụng
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "[::]:8080"]