from app.api.routers.auth import router as auth_router
from app.api.routers.tasks import router as tasks_router
from app.api.routers.categories import router as categories_router

all_routers = [auth_router, tasks_router, categories_router]
