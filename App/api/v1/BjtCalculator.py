from App.api.dependencies.auth import get_current_active_user
from App.core.ElectronicsCalculator import electronic_calculator,ElectronicsCalculator
from fastapi import FastAPI,APIRouter
from functools import lru_cache

@lru_cache(maxsize=1)
def get_calculator() -> ElectronicsCalculator:
    """Dependency for calculator instance."""
    return ElectronicsCalculator()

bjt_route=APIRouter(prefix="/bjt_calculator",tags=["bjt-calculator"])

