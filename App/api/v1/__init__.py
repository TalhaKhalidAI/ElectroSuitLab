from fastapi import APIRouter
from .Users import router as users_router
from App.api.v1.BjtCalculator import bjt_route
from App.api.v1.Mosfet_Calculator import mosfet_router
v1_router=APIRouter()

v1_router.include_router(users_router)
v1_router.include_router(bjt_route)
v1_router.include_router(mosfet_router)