# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.utils import get_openapi

# Giữ lại router cũ nếu nó đã là FastAPI APIRouter
# (nếu đang là Flask blueprint, xem ghi chú phía dưới để đổi sang APIRouter)
from api import api_router

server_urls = os.getenv("SERVER_URL", "http://localhost:8000").split(",")

# Tạo danh sách servers cho FastAPI
servers = [
    {"url": url.strip(), "description": f"Server {i + 1} ({url.strip()})"}
    for i, url in enumerate(server_urls)
    if url.strip()  # Bỏ qua URL rỗng
]

docs_url = os.getenv("DOCS_URL", "/v3/docs")
redoc_url = os.getenv("REDOC_URL", "/v3/redoc")
openapi_url = os.getenv("OPENAPI_URL", "/v3/api-docs")

app = FastAPI(docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url, servers=servers)

# Mount static & templates (nếu bạn có thư mục này)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Giữ prefix như cũ
app.include_router(api_router, prefix="")

# Add define openapi function to customize OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        description=app.description,
    )

    # ✅ BẢO TOÀN DANH SÁCH SERVERS
    # Lấy từ app.servers (được set khi khởi tạo FastAPI(..., servers=servers))
    schema["servers"] = [
        {"url": s.url, "description": s.description or ""}
        for s in (app.servers or [])
    ]


    # ========== SecurityScheme: bearerAuth (HTTP Bearer JWT) ==========
    schema.setdefault("components", {}).setdefault("securitySchemes", {})["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT auth description",
    }

    # ========== Global Security Requirement (như @SecurityRequirement) ==========
    # Cho Swagger hiển thị nút Authorize và tự gửi Authorization header cho mọi endpoint
    schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi
