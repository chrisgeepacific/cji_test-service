from flask import Flask, render_template
from fastopenapi.routers import FlaskRouter
from api import api_router

app = Flask(__name__)

# Initialize FastOpenAPI router
router = FlaskRouter(
    app=app,
    title="Flask OpenAPI",
    description="API for Flask application test deployed",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/v3/api-docs/test"
)

# Include API routes with a prefix
router.include_router(api_router, prefix="/api/v1/test")

@app.route('/')
def index():
    return render_template('index.html')


@router.get("/healthz", tags=["system"])
def healthz():
    return {"status": "ok"}

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="::", port=port, debug=False)  # host="::" để mở IPv6 khi chạy local
