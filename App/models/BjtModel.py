from pydantic import BaseModel, Field, field_validator, model_validator,PrivateAttr
from typing import Optional
from enum import Enum

class ResistorUnit(str, Enum):
    OHM = "ohm"
    KOHM = "kohm"
    MOHM = "mohm"


class CEM(BaseModel):
    vcc: float = Field(..., gt=0, le=1000)
    
    rc: float = Field(..., gt=0)
    rc_unit: ResistorUnit = ResistorUnit.KOHM
    
    re: float = Field(..., gt=0)
    re_unit: ResistorUnit = ResistorUnit.OHM
    
    r1: float = Field(..., gt=0)
    r1_unit: ResistorUnit = ResistorUnit.KOHM
    
    r2: float = Field(..., gt=0)
    r2_unit: ResistorUnit = ResistorUnit.KOHM
    
    beta: float = Field(200, ge=10, le=1000)
    
    rl: Optional[float] = Field(None, gt=0)
    rl_unit: ResistorUnit = ResistorUnit.KOHM

    bypass:float=True
    ccb_pf:Optional[float]=None
    freq_hz:Optional[float]=None
    # Store converted values
    _rc_ohm: float = None
    _re_ohm: float = None
    _r1_ohm: float = None
    _r2_ohm: float = None
    _rl_ohm: float = None
    
    # ================================================================
    # STATIC METHOD (for conversion)
    # ================================================================
    
    @staticmethod
    def to_ohm(value: float, unit: ResistorUnit) -> float:
        """Convert resistance value to Ohms"""
        if unit == ResistorUnit.OHM:
            return value
        elif unit == ResistorUnit.KOHM:
            return value * 1000
        elif unit == ResistorUnit.MOHM:
            return value * 1_000_000
        return value
    
    # ================================================================
    # FIELD VALIDATORS (need @classmethod)
    # ================================================================
    
    @field_validator('vcc')
    @classmethod
    def validate_vcc(cls, v: float) -> float:
        if v < 1:
            raise ValueError(f"Vcc must be at least 1V (got {v}V)")
        if v > 1000:
            raise ValueError(f"Vcc too high: {v}V. Maximum 1000V")
        return v
    
    @field_validator('beta')
    @classmethod
    def validate_beta(cls, v: float) -> float:
        if v < 10:
            raise ValueError(f"Beta too low: {v}. Minimum 10")
        if v > 1000:
            raise ValueError(f"Beta too high: {v}. Maximum 1000")
        return v
    
    @field_validator('rc', 're', 'r1', 'r2', 'rl')
    @classmethod
    def validate_resistor_values(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError(f"Resistor value must be > 0, got {v}")
        return v
    
    # ================================================================
    # MODEL VALIDATOR (NO @classmethod, use self)
    # ================================================================
    
    @model_validator(mode='after')
    def calculate_resistor_to_ohm(self) -> 'CEM':  # ✅ NO @classmethod
        """Convert all resistors to Ohms"""
        self._rc_ohm = self.to_ohm(self.rc, self.rc_unit)
        self._re_ohm = self.to_ohm(self.re, self.re_unit)
        self._r1_ohm = self.to_ohm(self.r1, self.r1_unit)
        self._r2_ohm = self.to_ohm(self.r2, self.r2_unit)
        
        if self.rl is not None:
            self._rl_ohm = self.to_ohm(self.rl, self.rl_unit) 

        else:
            self._rl_ohm = float('inf')
        
        return self



class CBM(BaseModel):
    vcc: float = Field(..., gt=0, le=1000)
    
    rc: float = Field(..., gt=0)
    rc_unit: ResistorUnit = ResistorUnit.KOHM
    
    re: float = Field(..., gt=0)
    re_unit: ResistorUnit = ResistorUnit.OHM
    
    r1: float = Field(..., gt=0)
    r1_unit: ResistorUnit = ResistorUnit.KOHM
    
    r2: float = Field(..., gt=0)
    r2_unit: ResistorUnit = ResistorUnit.KOHM
    
    beta: float = Field(200, ge=10, le=1000)
    
    rl: Optional[float] = Field(None, gt=0)
    rl_unit: ResistorUnit = ResistorUnit.KOHM

    vbias:float=Field(...,description="voltage bias or onput signal voltage bias pass in emittor of transsitor")

    # Store converted values
    _rc_ohm: float = None
    _re_ohm: float = None
    _r1_ohm: float = None
    _r2_ohm: float = None
    _rl_ohm: float = None
    
    # ================================================================
    # STATIC METHOD (for conversion)
    # ================================================================
    
    @staticmethod
    def to_ohm(value: float, unit: ResistorUnit) -> float:
        """Convert resistance value to Ohms"""
        if unit == ResistorUnit.OHM:
            return value
        elif unit == ResistorUnit.KOHM:
            return value * 1000
        elif unit == ResistorUnit.MOHM:
            return value * 1_000_000
        return value
    
    # ================================================================
    # FIELD VALIDATORS (need @classmethod)
    # ================================================================
    
    @field_validator('vcc')
    @classmethod
    def validate_vcc(cls, v: float) -> float:
        if v < 1:
            raise ValueError(f"Vcc must be at least 1V (got {v}V)")
        if v > 1000:
            raise ValueError(f"Vcc too high: {v}V. Maximum 1000V")
        return v
    
    @field_validator('beta')
    @classmethod
    def validate_beta(cls, v: float) -> float:
        if v < 10:
            raise ValueError(f"Beta too low: {v}. Minimum 10")
        if v > 1000:
            raise ValueError(f"Beta too high: {v}. Maximum 1000")
        return v
    
    @field_validator('rc', 're', 'r1', 'r2', 'rl')
    @classmethod
    def validate_resistor_values(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError(f"Resistor value must be > 0, got {v}")
        return v
    
    # ================================================================
    # MODEL VALIDATOR (NO @classmethod, use self)
    # ================================================================
    
    @model_validator(mode='after')
    def calculate_resistor_to_ohm(self) -> 'CBM':  # ✅ NO @classmethod
        """Convert all resistors to Ohms"""
        self._rc_ohm = self.to_ohm(self.rc, self.rc_unit)
        self._re_ohm = self.to_ohm(self.re, self.re_unit)
        self._r1_ohm = self.to_ohm(self.r1, self.r1_unit)
        self._r2_ohm = self.to_ohm(self.r2, self.r2_unit)
        
        if self.rl is not None:
            self._rl_ohm = self.to_ohm(self.rl, self.rl_unit) 

        else:
            self._rl_ohm = float('inf')
        
        return self
    
class CCM(BaseModel):
    """Common Collector (Emitter Follower) Request Model"""
    
    vcc: float = Field(..., gt=0, le=1000, description="Supply voltage (V)")
    
    # Emitter resistor
    re: float = Field(..., gt=0, description="Emitter resistor value")
    re_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Unit for Re: ohm, kohm, mohm")
    
    # Base bias resistor to Vcc
    r1: float = Field(..., gt=0, description="Base bias resistor to Vcc value")
    r1_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for R1: ohm, kohm, mohm")
    
    # Base bias resistor to GND
    r2: float = Field(..., gt=0, description="Base bias resistor to GND value")
    r2_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for R2: ohm, kohm, mohm")
    
    # Transistor beta
    beta: float = Field(200, description="DC current gain hFE", ge=10, le=1000)
    
    # Source resistance (optional)
    rsource: Optional[float] = Field(0, description="Source resistance (Ω)", ge=0)
    rsource_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Unit for Rsource")
    
    # Private fields for converted values
    _re_ohm: float = PrivateAttr(None)
    _r1_ohm: float = PrivateAttr(None)
    _r2_ohm: float = PrivateAttr(None)
    _rsource_ohm: float = PrivateAttr(None)
    
    # ================================================================
    # STATIC METHOD
    # ================================================================
    
    @staticmethod
    def to_ohm(value: float, unit: ResistorUnit) -> float:
        if unit == ResistorUnit.OHM:
            return value
        elif unit == ResistorUnit.KOHM:
            return value * 1000
        elif unit == ResistorUnit.MOHM:
            return value * 1_000_000
        return value
    
    # ================================================================
    # FIELD VALIDATORS
    # ================================================================
    
    @field_validator('vcc')
    @classmethod
    def validate_vcc(cls, v: float) -> float:
        if v < 1:
            raise ValueError(f"Vcc must be at least 1V (got {v}V)")
        if v > 1000:
            raise ValueError(f"Vcc too high: {v}V. Maximum 1000V")
        return v
    
    @field_validator('beta')
    @classmethod
    def validate_beta(cls, v: float) -> float:
        if v < 10:
            raise ValueError(f"Beta too low: {v}. Minimum 10")
        if v > 1000:
            raise ValueError(f"Beta too high: {v}. Maximum 1000")
        return v
    
    @field_validator('re', 'r1', 'r2', 'rsource')
    @classmethod
    def validate_resistor_values(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError(f"Resistor value must be >= 0, got {v}")
        return v
    
    # ================================================================
    # MODEL VALIDATOR
    # ================================================================
    
    @model_validator(mode='after')
    def convert_resistors_to_ohm(self) -> 'CCM':
        """Convert all resistors to Ohms"""
        self._re_ohm = self.to_ohm(self.re, self.re_unit)
        self._r1_ohm = self.to_ohm(self.r1, self.r1_unit)
        self._r2_ohm = self.to_ohm(self.r2, self.r2_unit)
        self._rsource_ohm = self.to_ohm(self.rsource, self.rsource_unit) if self.rsource else 0
        
        return self