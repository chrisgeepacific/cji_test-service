from flask import Flask, render_template
from fastopenapi.routers import FlaskRouter
from api import api_router

app = Flask(__name__)

# Initialize FastOpenAPI router
router = FlaskRouter(
    app=app,
    title="Flask OpenAPI",
    description="API for Flask application deployed on Railway",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Include API routes with a prefix
router.include_router(api_router, prefix="/api")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)