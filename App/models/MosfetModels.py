from pydantic import BaseModel, Field, field_validator, model_validator, PrivateAttr
from typing import Optional
from enum import Enum

class ResistorUnit(str, Enum):
    OHM = "ohm"
    KOHM = "kohm"
    MOHM = "mohm"


class CommonSourceModel(BaseModel):
    """Common Source MOSFET Amplifier Request Model"""
    
    # Supply voltage
    vdd: float = Field(..., gt=0, le=1000, description="Drain supply voltage (V)")
    
    # Drain resistor
    rd: float = Field(..., gt=0, description="Drain resistor value")
    rd_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for Rd: ohm, kohm, mohm")
    
    # Gate bias resistor to Vdd
    r1: float = Field(..., gt=0, description="Gate bias resistor to Vdd value")
    r1_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for R1: ohm, kohm, mohm")
    
    # Gate bias resistor to GND
    r2: float = Field(..., gt=0, description="Gate bias resistor to GND value")
    r2_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for R2: ohm, kohm, mohm")
    
    # MOSFET parameters
    vth: float = Field(..., gt=0, le=10, description="Threshold voltage (V). Typical: 1.5V-4V")
    k: float = Field(..., gt=0, le=1.0, description="Transconductance parameter (A/V²). Typical: 0.001-0.1")
    
    # Optional source resistor
    rs: float = Field(0, ge=0, description="Source resistor (Ω). Default 0")
    rs_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Unit for Rs")
    
    # Optional load resistor
    rl: Optional[float] = Field(None, gt=0, description="Load resistor (Ω)")
    rl_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for RL")
    
    # Private fields for converted values
    _rd_ohm: float = PrivateAttr(None)
    _r1_ohm: float = PrivateAttr(None)
    _r2_ohm: float = PrivateAttr(None)
    _rs_ohm: float = PrivateAttr(None)
    _rl_ohm: float = PrivateAttr(None)
    
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
    
    @field_validator('vdd')
    @classmethod
    def validate_vdd(cls, v: float) -> float:
        if v < 1:
            raise ValueError(f"Vdd must be at least 1V (got {v}V)")
        if v > 1000:
            raise ValueError(f"Vdd too high: {v}V. Maximum 1000V")
        return v
    
    @field_validator('vth')
    @classmethod
    def validate_vth(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"Vth cannot be negative (got {v}V)")
        if v > 10:
            raise ValueError(f"Vth too high: {v}V. Maximum 10V")
        return v
    
    @field_validator('k')
    @classmethod
    def validate_k(cls, v: float) -> float:
        if v <= 0:
            raise ValueError(f"K must be > 0 (got {v})")
        if v > 1:
            raise ValueError(f"K too high: {v}. Maximum 1.0 A/V²")
        return v
    
    @field_validator('rd', 'r1', 'r2', 'rs', 'rl')
    @classmethod
    def validate_resistor_values(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError(f"Resistor value must be >= 0, got {v}")
        return v
    
    # ================================================================
    # MODEL VALIDATOR
    # ================================================================
    
    @model_validator(mode='after')
    def convert_resistors_to_ohm(self) -> 'CommonSourceModel':
        """Convert all resistors to Ohms"""
        self._rd_ohm = self.to_ohm(self.rd, self.rd_unit)
        self._r1_ohm = self.to_ohm(self.r1, self.r1_unit)
        self._r2_ohm = self.to_ohm(self.r2, self.r2_unit)
        self._rs_ohm = self.to_ohm(self.rs, self.rs_unit)
        
        if self.rl is not None:
            self._rl_ohm = self.to_ohm(self.rl, self.rl_unit)
        else:
            self._rl_ohm = float('inf')
        
        return self
    

class CommonDrainModel(BaseModel):
    """Common Drain MOSFET (Source Follower) Request Model"""
    
    # Supply voltage
    vdd: float = Field(..., gt=0, le=1000, description="Drain supply voltage (V)")
    
    # Gate bias resistor to Vdd
    r1: float = Field(..., gt=0, description="Gate bias resistor to Vdd value")
    r1_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for R1: ohm, kohm, mohm")
    
    # Gate bias resistor to GND
    r2: float = Field(..., gt=0, description="Gate bias resistor to GND value")
    r2_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for R2: ohm, kohm, mohm")
    
    # Source resistor (load)
    rs: float = Field(..., gt=0, description="Source resistor value (load)")
    rs_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Unit for Rs")
    
    # Source resistance (signal source impedance)
    rsource: float = Field(0, ge=0, description="Source resistance (Ω) — signal source impedance")
    rsource_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Unit for Rsource")
    
    # MOSFET parameters
    vth: float = Field(..., gt=0, le=10, description="Threshold voltage (V). Typical: 1.5V-4V")
    k: float = Field(..., gt=0, le=1.0, description="Transconductance parameter (A/V²). Typical: 0.001-0.1")
    
    # Private fields for converted values
    _r1_ohm: float = PrivateAttr(None)
    _r2_ohm: float = PrivateAttr(None)
    _rs_ohm: float = PrivateAttr(None)
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
    
    @field_validator('vdd')
    @classmethod
    def validate_vdd(cls, v: float) -> float:
        if v < 1:
            raise ValueError(f"Vdd must be at least 1V (got {v}V)")
        if v > 1000:
            raise ValueError(f"Vdd too high: {v}V. Maximum 1000V")
        return v
    
    @field_validator('vth')
    @classmethod
    def validate_vth(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"Vth cannot be negative (got {v}V)")
        if v > 10:
            raise ValueError(f"Vth too high: {v}V. Maximum 10V")
        return v
    
    @field_validator('k')
    @classmethod
    def validate_k(cls, v: float) -> float:
        if v <= 0:
            raise ValueError(f"K must be > 0 (got {v})")
        if v > 1:
            raise ValueError(f"K too high: {v}. Maximum 1.0 A/V²")
        return v
    
    @field_validator('r1', 'r2', 'rs', 'rsource')
    @classmethod
    def validate_resistor_values(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError(f"Resistor value must be >= 0, got {v}")
        return v
    
    # ================================================================
    # MODEL VALIDATOR
    # ================================================================
    
    @model_validator(mode='after')
    def convert_resistors_to_ohm(self) -> 'CommonDrainModel':
        """Convert all resistors to Ohms"""
        self._r1_ohm = self.to_ohm(self.r1, self.r1_unit)
        self._r2_ohm = self.to_ohm(self.r2, self.r2_unit)
        self._rs_ohm = self.to_ohm(self.rs, self.rs_unit)
        self._rsource_ohm = self.to_ohm(self.rsource, self.rsource_unit)
        
        return self
    

class CommonGateModel(BaseModel):
    """Common Gate MOSFET Amplifier Request Model - Simplified for Power Electronics"""
    
    # Supply voltage (up to 400V for power electronics)
    vdd: float = Field(..., gt=0, le=400, description="Drain supply voltage (V)")
    
    # Drain resistor
    rd: float = Field(..., gt=0, description="Drain resistor value")
    rd_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for Rd")
    
    # Source resistor
    rs: float = Field(..., gt=0, description="Source resistor value")
    rs_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Unit for Rs")
    
    # Gate bias voltage (external)
    vbias: float = Field(..., gt=0, le=20, description="Gate bias voltage (V)")
    
    # MOSFET parameters
    vth: float = Field(2.5, gt=0, le=10, description="Threshold voltage (V). Default 2.5V")
    k: float = Field(0.05, gt=0, le=1.0, description="Transconductance (A/V²). Default 0.05")
    
    # Optional load resistor
    rl: Optional[float] = Field(None, gt=0, description="Load resistor (Ω)")
    rl_unit: ResistorUnit = Field(ResistorUnit.KOHM, description="Unit for RL")
    
    # Private fields for converted values
    _rd_ohm: float = PrivateAttr(None)
    _rs_ohm: float = PrivateAttr(None)
    _rl_ohm: float = PrivateAttr(None)
    
    # ================================================================
    # CONVERSION (Single method)
    # ================================================================
    
    def _to_ohm(self, value: float, unit: ResistorUnit) -> float:
        if unit == ResistorUnit.OHM:
            return value
        elif unit == ResistorUnit.KOHM:
            return value * 1000
        else:  # MOHM
            return value * 1_000_000
    
    # ================================================================
    # MODEL VALIDATOR (Single validator for everything)
    # ================================================================
    
    @model_validator(mode='after')
    def validate_and_convert(self) -> 'CommonGateModel':
        """Single validator: converts resistors and checks basic rules"""
        
        # Convert resistors to Ohms
        self._rd_ohm = self._to_ohm(self.rd, self.rd_unit)
        self._rs_ohm = self._to_ohm(self.rs, self.rs_unit)
        
        if self.rl is not None:
            self._rl_ohm = self._to_ohm(self.rl, self.rl_unit)
        else:
            self._rl_ohm = None
        
        # Basic sanity checks (not strict errors, just warnings via print)
        if self.vbias <= self.vth:
            print(f"⚠️ Warning: Vbias ({self.vbias}V) <= Vth ({self.vth}V) — MOSFET will be OFF")
        
        if self.vdd > 100:
            print(f"⚠️ Warning: Vdd={self.vdd}V is high — ensure MOSFET is rated for this voltage")
        
        if self.k > 0.5:
            print(f"⚠️ Warning: K={self.k} is high — transistor may have high current")
        
        return self