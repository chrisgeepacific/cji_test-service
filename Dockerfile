# 1. Base Stage: Chọn một base image Python chính thức.
# 'slim-buster' giúp giảm kích thước image đáng kể.
FROM python:3.11-slim-buster

# 2. Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Railway thường sử dụng cổng 8080. Đảm bảo Gunicorn sẽ lắng nghe cổng này.
ENV PORT 8080

# 3. Thiết lập thư mục làm việc bên trong container
WORKDIR /usr/src/app

# 4. Cài đặt các thư viện cần thiết
# Sao chép file requirements.txt trước để Docker có thể tận dụng cache
COPY requirements.txt .

# Cài đặt các gói phụ thuộc (bao gồm Gunicorn)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Sao chép toàn bộ code ứng dụng
# (Đảm bảo bạn có file .dockerignore để bỏ qua các file không cần thiết như .git, __pycache__, venv)
COPY . .

# 6. Lệnh khởi động (Startup Command)
# Sử dụng Gunicorn để chạy ứng dụng Flask của bạn
# 'app:create_app()' là ví dụ. Thay thế bằng cách gọi ứng dụng Flask của bạn.
# -b 0.0.0.0:$PORT: Gunicorn lắng nghe trên tất cả các interface mạng (0.0.0.0) và cổng 8080.
# -w 4: Chạy với 4 worker processes (thường là 2 * số lõi CPU + 1).
# 7. Khai báo cổng (Chỉ mang tính chất tài liệu, Railway không thực sự dùng)
# Thay thế 'app:app' bằng tên module và tên instance Flask của bạn (Ví dụ: main:app hoặc wsgi:app)
EXPOSE 8080

CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "[::]:8080"]


