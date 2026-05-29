from App.api.dependencies.auth import get_current_active_user
from App.core.ElectronicsCalculator import electronic_calculator,ElectronicsCalculator
from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from functools import lru_cache
# from App.models.BjtModel import CEM,CBM,CCM
from enum import Enum
from App.models.MosfetModels import CommonSourceModel,CommonDrainModel,CommonGateModel

mosfet_router=APIRouter(prefix="/mosfet_calculator",tags=["Mosfet_Calculator"])
@lru_cache(maxsize=1)
def get_calculator() -> ElectronicsCalculator:
    """Dependency for calculator instance."""
    return ElectronicsCalculator()

@mosfet_router.post("/common_source")
async def common_source_calculator(
    cc: CommonSourceModel,
    ec: ElectronicsCalculator = Depends(get_calculator)
):
    try:
        result = ec.common_source_mosfet(
            Vdd=cc.vdd,
            Rd=cc._rd_ohm,
            R1=cc._r1_ohm,
            R2=cc._r2_ohm,
            Vth=cc.vth,
            K=cc.k,
            RL=cc._rl_ohm,
            Rs=cc._rs_ohm      # ← FIXED: use converted value
        )
        return result          # ← FIXED: return the result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating common source MOSFET: {str(e)}"
        )
 
 
@mosfet_router.post("/common_drain")
async def common_drain_calculator(
    cd: CommonDrainModel,  # ← Use CommonDrainModel, not CommonSourceModel
    ec: ElectronicsCalculator = Depends(get_calculator)
):
    try:
        result = ec.common_drain_mosfet(
            Vdd=cd.vdd,
            R1=cd._r1_ohm,
            R2=cd._r2_ohm,
            Rs=cd._rs_ohm,
            Vth=cd.vth,
            K=cd.k,
            Rsource=cd._rsource_ohm      # ← This matches function parameter
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating common drain MOSFET: {str(e)}"
        )
    
@mosfet_router.post("/common_gate")
async def common_gate_calculator(
    cg: CommonGateModel,
    ec: ElectronicsCalculator = Depends(get_calculator)
):
    """
    Common Gate MOSFET Amplifier Calculator
    
    Input signal goes to SOURCE. Gate is biased externally (Vbias).
    Output taken from DRAIN. Very low input impedance (good for 50Ω systems).
    Non-inverting (0° phase shift).
    """
    try:
        result = ec.common_gate_mosfet(
            Vdd=cg.vdd,
            Rd=cg._rd_ohm,
            Rs=cg._rs_ohm,
            Vbias=cg.vbias,
            Vth=cg.vth,
            K=cg.k,
            RL=cg._rl_ohm
        )
        
        # Add power warning if needed
        if result.get("power_mW", {}).get("transistor", 0) > 500:
            result["warning"] = "⚠️ Power >500mW — needs heatsink!"
        else:
            result["warning"] = None
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating common gate MOSFET: {str(e)}"
        )