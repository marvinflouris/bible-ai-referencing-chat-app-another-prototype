"""
Scripture AI - Main Application
FastAPI entry point with all routes configured
"""

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.database import init_db
from app.config import settings
from app.routes import verses, auth, notes

# Create FastAPI app
app = FastAPI(
    title="Scripture AI API",
    description="Bible study application with Hebrew/Greek word analysis using Strong's numbers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://localhost:8080",      # Vue dev server
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= STARTUP =============

@app.on_event("startup")
def startup_event():
    """Initialize database on server startup"""
    init_db()
    print("\n" + "="*70)
    print(" "*15 + "✓ SCRIPTURE AI API STARTED")
    print("="*70)
    print(f"  Server: {settings.HOST}:{settings.PORT}")
    print(f"  Environment: {settings.ENV}")
    print(f"  Database: PostgreSQL")
    print(f"  Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print("="*70 + "\n")

# ============= ROOT ENDPOINTS =============

@app.get("/")
def root():
    """Root endpoint - API info"""
    return {
        "name": "Scripture AI",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "verses": "/api/verses",
            "auth": "/api/auth",
            "notes": "/api/notes"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "scripture-ai",
        "version": "1.0.0"
    }

# ============= INCLUDE ROUTES =============

# Verse endpoints
app.include_router(
    verses.router,
    prefix="/api",
)

# Authentication endpoints
app.include_router(
    auth.router,
    prefix="/api",
)

# Notes endpoints
app.include_router(
    notes.router,
    prefix="/api",
)

# ============= CUSTOM OPENAPI SCHEMA =============

def custom_openapi():
    """Custom OpenAPI schema with authentication examples"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Scripture AI API",
        version="1.0.0",
        description="""
        # Scripture AI - Bible Study Application

        A comprehensive Bible study API with:
        - **31,102 KJV verses** with Hebrew/Greek word analysis
        - **Strong's number linking** for original language lookup
        - **User authentication** with JWT tokens
        - **Personal notes** on verses
        - **Full-text search** capabilities

        ## Authentication

        Most endpoints require Bearer token authentication:

        ```
        Authorization: Bearer <your_access_token>
        ```

        Get a token by:
        1. Register: `POST /api/auth/register`
        2. Login: `POST /api/auth/login`

        ## Quick Start

        1. Register a user account
        2. Login to get access token
        3. Use token to access protected endpoints
        4. Search verses and create notes

        ## API Organization

        - **Verses** - Search and retrieve Bible verses
        - **Auth** - User registration and login
        - **Notes** - Create and manage personal notes
        """,
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ============= ERROR HANDLERS =============

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    import traceback
    traceback.print_exc()
    
    return {
        "error": "Internal Server Error",
        "detail": str(exc) if settings.ENV == "development" else "An error occurred"
    }

# ============= MAIN =============

if __name__ == "__main__":
    import uvicorn
    
    print("\nStarting Scripture AI server...")
    print(f"Configuration: {settings.ENV.upper()}")
    print()
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENV == "development"),
        log_level="info"
    )
