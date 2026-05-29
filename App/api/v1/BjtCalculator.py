from App.api.dependencies.auth import get_current_active_user
from App.core.ElectronicsCalculator import electronic_calculator,ElectronicsCalculator
from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from functools import lru_cache
from App.models.BjtModel import CEM,CBM,CCM
from enum import Enum

@lru_cache(maxsize=1)
def get_calculator() -> ElectronicsCalculator:
    """Dependency for calculator instance."""
    return ElectronicsCalculator()

bjt_route=APIRouter(prefix="/bjt_calculator",tags=["bjt-calculator"])

@bjt_route.post("/cmmon_emitter")
async def common_emitttor_calculator(cm:CEM,ec:ElectronicsCalculator=Depends(get_calculator)):
    try:
        cev=ec.common_emitter(cm.vcc,cm._rc_ohm,cm._re_ohm,cm._r1_ohm,cm._r2_ohm,cm.beta,cm._rl_ohm,cm.bypass,cm.ccb_pf,cm.freq_hz)
        return cev
        pass
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error common emittor calcualte due to {e}")
    
@bjt_route.post("/common_base")
async def common_base_calculator(
    cm: CBM,
    ec: ElectronicsCalculator = Depends(get_calculator)
):
    try:
        # Common Base expects: Vcc, Rc, Re, Vbias, beta, RL
        # NOT: R1, R2 (those are for voltage divider, but Common Base uses external Vbias)
        result = ec.common_base(
            Vcc=cm.vcc,
            Rc=cm._rc_ohm,
            Re=cm._re_ohm,
            Vbias=cm.vbias,
            beta=cm.beta,
            RL=cm._rl_ohm
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in common base calculation: {str(e)}"
        )
    
@bjt_route.post("/common_collector")
async def common_collector_calculator(
    cm: CCM,
    ec: ElectronicsCalculator = Depends(get_calculator)
):
    try:
        result = ec.common_collector(
            Vcc=cm.vcc,
            Re=cm._re_ohm,
            R1=cm._r1_ohm,
            R2=cm._r2_ohm,
            beta=cm.beta,
            Rsource=cm._rsource_ohm
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in common collector calculation: {str(e)}"
        )
