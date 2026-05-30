from App.api.dependencies.auth import get_current_active_user
from App.core.ElectronicsCalculator import electronic_calculator,ElectronicsCalculator
from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from functools import lru_cache
from App.models.BasicElectronicsModels import OhmLawModel,ResistorUnit,CurrentUnit,FrequencyUnit,CouplingCapacitorRequest,ResistorImpedanceModel,CapacitanceUnit,CapacitorImpedanceModel,InductanceUnit,InductorImpedanceModel,ComponentType,SeriesImpedanceModel,ParallelImpedanceModel
from enum import Enum

bcc_router=APIRouter(prefix="/basic_circuit",tags=["Baisc Electronic Calculator"])
@lru_cache(maxsize=1)
def get_calculator() -> ElectronicsCalculator:
    """Dependency for calculator instance."""
    return ElectronicsCalculator()

@bcc_router.post("/ohm_law")
async def ohm_law(
    oml: OhmLawModel,
    cal: ElectronicsCalculator = Depends(get_calculator)
):
    try:
        result = cal.ohms_law(
            voltage=oml._voltage_v,
            current=oml._current_a,
            resistance=oml._resistance_ohm
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@bcc_router.get("/resistor_units")
async def resistor_unnit():
    try:
        return  [unit.name for unit in ResistorUnit]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@bcc_router.get("/current_unit")
async def current_unit():
    try:
        return  [unit.name for unit in CurrentUnit]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@bcc_router.get("/frequancy_unit")
async def frequancy_unit():
    try:
        return  [unit.name for unit in FrequencyUnit]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@bcc_router.get("/capacitance_unit")
async def capacitanceUnit():
    try:
        return  [unit.name for unit in CapacitanceUnit]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@bcc_router.get("/inductance_unit")
async def InductorUnits():
    try:
        return  [unit.name for unit in InductanceUnit]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@bcc_router.get("/component_type")
async def ComponentTypes():
    try:
        return  [unit.name for unit in ComponentType]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@bcc_router.post("/coupling_capacitor")
async def coupling_capacitor(
    ccm:CouplingCapacitorRequest,
    cal: ElectronicsCalculator = Depends(get_calculator)
):
    """
         Calculate coupling capacitor value for RC high-pass filter.

         Use this to find the right capacitor value for:
         - Input coupling capacitor (Cin)
         - Output coupling capacitor (Cout)
         - Emitter bypass capacitor (Ce)

         Formula: C = 1 / (2π × f_cutoff × Z)
         where f_cutoff = frequency × cutoff_ratio
         """
    try:
        result = cal.coupling_capacitor(
            frequency_hz=ccm._frequency_hz,
            impedance_ohm=ccm._impedance_ohm,
            cutoff_ratio=ccm.cutoff_ratio
        )
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@bcc_router.post("/resistor_impedance")
async def resistor_impedance(
    rem:ResistorImpedanceModel,
    cal: ElectronicsCalculator = Depends(get_calculator)
):
    """
         Calculate coupling capacitor value for RC high-pass filter.

         Use this to find the right capacitor value for:
         - Input coupling capacitor (Cin)
         - Output coupling capacitor (Cout)
         - Emitter bypass capacitor (Ce)

         Formula: C = 1 / (2π × f_cutoff × Z)
         where f_cutoff = frequency × cutoff_ratio
         """
    try: 
        result=cal.resistor_impedance(rem._resistance_ohm)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
 
@bcc_router.post("/capacitor_impedance")
async def capacitorImpedance(
    cim:CapacitorImpedanceModel,
    cal: ElectronicsCalculator = Depends(get_calculator)
):
    try: 
       result=cal.capacitor_impedance(cim._capacitance_f,cim._frequency_hz)
       return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@bcc_router.post("/inductor_impedance")
async def inductorImpedance(
    iim:InductorImpedanceModel,
    cal: ElectronicsCalculator = Depends(get_calculator)
):
    try:
        res=cal.inductor_impedance(iim._inductance_h,iim._frequency_hz)
        return res 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@bcc_router.post("/series_impedance")
async def series_impedance(
    sim: SeriesImpedanceModel,
    cal: ElectronicsCalculator = Depends(get_calculator)
):
    """
    Calculate total impedance of series components.
    """
    try:
        # Build components list for calculator
        components_list = []
        for comp in sim.components:
            components_list.append({
                "type": comp.type.value,
                "value": comp._base_value
            })
        
        # Call calculator (now returns auto-formatted result)
        result = cal.series_impedance(
            components=components_list,
            frequency_hz=sim._frequency_hz
        )
        
        # The calculator already returns formatted output
        # Just add any additional formatting if needed
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@bcc_router.post("/parallel_impedance")
async def parallel_impedance(
    pim: ParallelImpedanceModel,
    cal: ElectronicsCalculator = Depends(get_calculator)
):
    """
    Calculate total impedance of parallel components.
    
    For parallel circuits:
    - Conductances add: G_total = G1 + G2 + ...
    - Susceptances add: B_total = Bc1 + Bc2 + ... + Bl1 + Bl2 + ...
    - Total impedance: Z = 1 / √(G² + B²)
    - Phase angle: θ = atan2(B, G)
    
    Returns:
        - Individual component susceptances
        - Total impedance with phase angle
    """
    try:
        # Build components list for calculator
        components_list = []
        for comp in pim.components:
            components_list.append({
                "type": comp.type.value,
                "value": comp._base_value
            })
        
        # Call calculator (now returns formatted output)
        result = cal.parallel_impedance(
            components=components_list,
            frequency_hz=pim._frequency_hz
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    