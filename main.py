# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Giữ lại router cũ nếu nó đã là FastAPI APIRouter
# (nếu đang là Flask blueprint, xem ghi chú phía dưới để đổi sang APIRouter)
from api import api_router

server_urls = os.getenv("SERVER_URL", "http://localhost:8000").split(",")

# Tạo danh sách servers cho FastAPI
servers = [
    {"url": url.strip(), "description": f"Server {i+1} ({url.strip()})"}
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

# Trang chủ render template (giống Flask)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health
@app.get("/healthz", tags=["system"])
async def healthz():
    return {"status": "ok"}

# Giữ prefix như cũ
app.include_router(api_router, prefix="/api/v1/test")
