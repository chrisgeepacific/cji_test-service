# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Giữ lại router cũ nếu nó đã là FastAPI APIRouter
# (nếu đang là Flask blueprint, xem ghi chú phía dưới để đổi sang APIRouter)
from api import api_router

app = FastAPI(
    title="FastAPI OpenAPI",
    description="API for application test deployed",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/v3/api-docs/test",
)

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
