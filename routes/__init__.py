from fastapi import APIRouter

# Create main API router
api_router = APIRouter()

# Import and include route modules here
from .auth import router as auth_router
# from .menu import router as menu_router
# from .orders import router as orders_router

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(menu_router, prefix="/menu", tags=["Menu"])
# api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])

@api_router.get("/")
async def api_root():
    return {"message": "Restro Backend API", "version": "1.0.0"}
