from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings
from app.core.rate_limit import limiter
from app.api.routers import all_routers

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    @app.exception_handler(RateLimitExceeded)
    async def _rate_limit_handler(request, exc):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

    # Routers
    for r in all_routers:
        app.include_router(r)


    @app.get("/health") # pragma: no cover
    async def health():
        return {"ok": True, "env": settings.env}

    return app

app = create_app()
