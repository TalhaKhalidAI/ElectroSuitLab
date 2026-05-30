from pydantic import BaseModel, Field, model_validator, PrivateAttr,field_validator
from typing import Optional,List
from enum import Enum

class FrequencyUnit(str, Enum):
    HZ = "hz"
    KHZ = "khz"
    MHZ = "mhz"
    GHZ = "ghz"  # ← ADD THIS

class ResistorUnit(str, Enum):
    OHM = "ohm"
    KOHM = "kohm"
    MOHM = "mohm"

class ComponentType(str, Enum):
    R = "R"
    C = "C"
    L = "L"

class CurrentUnit(str, Enum):
    AMPS = "amps"
    MAMPS = "mamps"
    UAMPS = "uamps"
    NAMPS = "namps"
    PAMPS = "pamps"
    
class CapacitanceUnit(str, Enum):
    """Capacitance units"""
    F = "f"      # Farads
    MF = "mf"    # Millifarads (10^-3 F)
    UF = "uf"    # Microfarads (10^-6 F)
    NF = "nf"    # Nanofarads (10^-9 F)
    PF = "pf"    # Picofarads (10^-12 F)

class InductanceUnit(str, Enum):
    """Inductance units"""
    H = "h"      # Henry
    MH = "mh"    # Millihenry (10^-3 H)
    UH = "uh"    # Microhenry (10^-6 H)
    NH = "nh"    # Nanohenry (10^-9 H)
    PH = "ph"    # Picohenry (10^-12 H)

class OhmLawModel(BaseModel):
    voltage: Optional[float] = Field(None, description="Voltage in Volts (V)")
    
    current: Optional[float] = Field(None, description="Current value")
    current_unit: CurrentUnit = Field(CurrentUnit.AMPS, description="Current unit")
    
    resistance: Optional[float] = Field(None, description="Resistance value")
    resistance_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Resistance unit")
    
    # Private fields for converted values
    _voltage_v: Optional[float] = PrivateAttr(None)
    _current_a: Optional[float] = PrivateAttr(None)
    _resistance_ohm: Optional[float] = PrivateAttr(None)
    
    @staticmethod
    def to_ampere(value: float, unit: CurrentUnit) -> float:
        """Convert current value to Amperes (A)"""
        if unit == CurrentUnit.AMPS:
            return value
        elif unit == CurrentUnit.MAMPS:
            return value / 1000
        elif unit == CurrentUnit.UAMPS:
            return value / 1_000_000
        elif unit == CurrentUnit.NAMPS:
            return value / 1_000_000_000
        elif unit == CurrentUnit.PAMPS:
            return value / 1_000_000_000_000
        raise ValueError(f"Unknown current unit: {unit}")
    
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
    
    @model_validator(mode='after')
    def validate_model(self) -> 'OhmLawModel':
        """Validate and convert values"""
        
        # Convert voltage (already in volts)
        if self.voltage is not None:
            self._voltage_v = self.voltage
        
        # Convert current to Amperes
        if self.current is not None:
            self._current_a = self.to_ampere(self.current, self.current_unit)
        
        # Convert resistance to Ohms
        if self.resistance is not None:
            if self.resistance <= 0:
                raise ValueError(f"Resistance must be positive. Got {self.resistance}")
            self._resistance_ohm = self.to_ohm(self.resistance, self.resistance_unit)
        
        # Check exactly two fields provided
        provided = sum([
            self._voltage_v is not None,
            self._current_a is not None,
            self._resistance_ohm is not None
        ])
        
        if provided != 2:
            raise ValueError(
                f"Exactly two of voltage, current, resistance must be provided. "
                f"Got {provided} field(s)."
            )
        
        # Validate no negative values (after conversion)
        if self._voltage_v is not None and self._voltage_v < 0:
            raise ValueError(f"Voltage cannot be negative. Got {self._voltage_v}V")
        
        if self._current_a is not None and self._current_a < 0:
            raise ValueError(f"Current cannot be negative. Got {self._current_a}A")
        
        return self
    
class CouplingCapacitorRequest(BaseModel):
    """Request model for coupling capacitor calculator"""
    
    frequency: float = Field(..., description="Signal frequency value")
    frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, description="Frequency unit (hz, khz, mhz)")
    
    impedance: float = Field(..., description="Impedance value")
    impedance_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Impedance unit (ohm, kohm, mohm)")
    
    cutoff_ratio: float = Field(0.1, ge=0.01, le=0.5, description="Cutoff ratio (0.01-0.5, default 0.1)")
    
    # Private fields for converted values
    _frequency_hz: float = PrivateAttr(None)
    _impedance_ohm: float = PrivateAttr(None)
    
    @staticmethod
    def to_hz(value: float, unit: FrequencyUnit) -> float:
        """Convert frequency to Hz"""
        if unit == FrequencyUnit.HZ:
            return value
        elif unit == FrequencyUnit.KHZ:
            return value * 1000
        elif unit == FrequencyUnit.MHZ:
            return value * 1_000_000
        return value
    
    @staticmethod
    def to_ohm(value: float, unit: ResistorUnit) -> float:
        """Convert impedance to Ohms"""
        if unit == ResistorUnit.OHM:
            return value
        elif unit == ResistorUnit.KOHM:
            return value * 1000
        elif unit == ResistorUnit.MOHM:
            return value * 1_000_000
        return value
    
    @model_validator(mode='after')
    def convert_units(self) -> 'CouplingCapacitorRequest':
        """Convert all units to base units"""
        self._frequency_hz = self.to_hz(self.frequency, self.frequency_unit)
        self._impedance_ohm = self.to_ohm(self.impedance, self.impedance_unit)
        
        # Validate positive values after conversion
        if self._frequency_hz <= 0:
            raise ValueError(f"Frequency must be positive. Got {self.frequency} {self.frequency_unit.value}")
        if self._impedance_ohm <= 0:
            raise ValueError(f"Impedance must be positive. Got {self.impedance} {self.impedance_unit.value}")
        
        return self
    

class ResistorImpedanceModel(BaseModel):
    """Request model for resistor impedance calculator"""
    
    resistance: float = Field(..., description="Resistance value")
    resistance_unit: ResistorUnit = Field(ResistorUnit.OHM, description="Resistance unit (ohm, kohm, mohm)")
    
    # Private field for converted value
    _resistance_ohm: float = PrivateAttr(None)
    
    @staticmethod
    def to_ohm(value: float, unit: ResistorUnit) -> float:
        """Convert resistance to Ohms"""
        if unit == ResistorUnit.OHM:
            return value
        elif unit == ResistorUnit.KOHM:
            return value * 1000
        elif unit == ResistorUnit.MOHM:
            return value * 1_000_000
        return value
    
    @model_validator(mode='after')
    def convert_units(self) -> 'ResistorImpedanceModel':
        """Convert resistance to Ohms"""
        if self.resistance <= 0:
            raise ValueError(f"Resistance must be positive. Got {self.resistance}")
        
        self._resistance_ohm = self.to_ohm(self.resistance, self.resistance_unit)
        
        return self
    
class CapacitorImpedanceModel(BaseModel):
    """Request model for capacitor impedance (capacitive reactance) calculator"""
    
    capacitance: float = Field(..., description="Capacitance value")
    capacitance_unit: CapacitanceUnit = Field(CapacitanceUnit.UF, description="Capacitance unit (f, mf, uf, nf, pf)")
    
    frequency: float = Field(..., description="Frequency value")
    frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, description="Frequency unit (hz, khz, mhz, ghz)")
    
    # Private fields for converted values
    _capacitance_f: float = PrivateAttr(None)
    _frequency_hz: float = PrivateAttr(None)
    
    @staticmethod
    def to_farad(value: float, unit: CapacitanceUnit) -> float:
        """Convert capacitance to Farads"""
        if unit == CapacitanceUnit.F:
            return value
        elif unit == CapacitanceUnit.MF:
            return value * 1e-3
        elif unit == CapacitanceUnit.UF:
            return value * 1e-6
        elif unit == CapacitanceUnit.NF:
            return value * 1e-9
        elif unit == CapacitanceUnit.PF:
            return value * 1e-12
        return value
    
    @staticmethod
    def to_hz(value: float, unit: FrequencyUnit) -> float:
        """Convert frequency to Hertz"""
        if unit == FrequencyUnit.HZ:
            return value
        elif unit == FrequencyUnit.KHZ:
            return value * 1000
        elif unit == FrequencyUnit.MHZ:
            return value * 1_000_000
        elif unit == FrequencyUnit.GHZ:
            return value * 1_000_000_000
        return value
    
    @model_validator(mode='after')
    def convert_units(self) -> 'CapacitorImpedanceModel':
        """Convert all units to base units"""
        # Validate positive values
        if self.capacitance <= 0:
            raise ValueError(f"Capacitance must be positive. Got {self.capacitance}")
        if self.frequency <= 0:
            raise ValueError(f"Frequency must be positive. Got {self.frequency}")
        
        # Convert to base units
        self._capacitance_f = self.to_farad(self.capacitance, self.capacitance_unit)
        self._frequency_hz = self.to_hz(self.frequency, self.frequency_unit)
        
        return self
    
class InductorImpedanceModel(BaseModel):
    """Request model for inductor impedance (inductive reactance) calculator"""
    
    inductance: float = Field(..., description="Inductance value")
    inductance_unit: InductanceUnit = Field(InductanceUnit.UH, description="Inductance unit (h, mh, uh, nh, ph)")
    
    frequency: float = Field(..., description="Frequency value")
    frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, description="Frequency unit (hz, khz, mhz, ghz)")
    
    # Private fields for converted values
    _inductance_h: float = PrivateAttr(None)
    _frequency_hz: float = PrivateAttr(None)
    
    @staticmethod
    def to_henry(value: float, unit: InductanceUnit) -> float:
        """Convert inductance to Henry"""
        if unit == InductanceUnit.H:
            return value
        elif unit == InductanceUnit.MH:
            return value * 1e-3
        elif unit == InductanceUnit.UH:
            return value * 1e-6
        elif unit == InductanceUnit.NH:
            return value * 1e-9
        elif unit == InductanceUnit.PH:
            return value * 1e-12
        return value
    
    @staticmethod
    def to_hz(value: float, unit: FrequencyUnit) -> float:
        """Convert frequency to Hertz"""
        if unit == FrequencyUnit.HZ:
            return value
        elif unit == FrequencyUnit.KHZ:
            return value * 1000
        elif unit == FrequencyUnit.MHZ:
            return value * 1_000_000
        elif unit == FrequencyUnit.GHZ:
            return value * 1_000_000_000
        return value
    
    @model_validator(mode='after')
    def convert_units(self) -> 'InductorImpedanceModel':
        """Convert all units to base units"""
        # Validate positive values
        if self.inductance <= 0:
            raise ValueError(f"Inductance must be positive. Got {self.inductance}")
        if self.frequency <= 0:
            raise ValueError(f"Frequency must be positive. Got {self.frequency}")
        
        # Convert to base units
        self._inductance_h = self.to_henry(self.inductance, self.inductance_unit)
        self._frequency_hz = self.to_hz(self.frequency, self.frequency_unit)
        
        return self


class ComponentItem(BaseModel):
    """Single component in series circuit"""
    
    type: ComponentType = Field(..., description="Component type: 'R', 'C', or 'L'")
    value: float = Field(..., gt=0, description="Component value")
    
    # Optional units (only used for C and L)
    capacitance_unit: CapacitanceUnit = Field(CapacitanceUnit.UF, description="For type='C': f, mf, uf, nf, pf")
    inductance_unit: InductanceUnit = Field(InductanceUnit.UH, description="For type='L': h, mh, uh, nh, ph")
    
    # Private field for converted base value
    _base_value: float = PrivateAttr(None)
    
    @staticmethod
    def to_farad(value: float, unit: CapacitanceUnit) -> float:
        """Convert capacitance to Farads"""
        if unit == CapacitanceUnit.F:
            return value
        elif unit == CapacitanceUnit.MF:
            return value * 1e-3
        elif unit == CapacitanceUnit.UF:
            return value * 1e-6
        elif unit == CapacitanceUnit.NF:
            return value * 1e-9
        elif unit == CapacitanceUnit.PF:
            return value * 1e-12
        return value
    
    @staticmethod
    def to_henry(value: float, unit: InductanceUnit) -> float:
        """Convert inductance to Henry"""
        if unit == InductanceUnit.H:
            return value
        elif unit == InductanceUnit.MH:
            return value * 1e-3
        elif unit == InductanceUnit.UH:
            return value * 1e-6
        elif unit == InductanceUnit.NH:
            return value * 1e-9
        elif unit == InductanceUnit.PH:
            return value * 1e-12
        return value
    
    @model_validator(mode='after')
    def convert_value(self) -> 'ComponentItem':
        """Convert value to base units based on type"""
        if self.type == ComponentType.C:
            self._base_value = self.to_farad(self.value, self.capacitance_unit)
        elif self.type == ComponentType.L:
            self._base_value = self.to_henry(self.value, self.inductance_unit)
        else:  # Resistor
            self._base_value = self.value
        return self


class SeriesImpedanceModel(BaseModel):
    """Request model for series impedance calculator"""
    
    components: List[ComponentItem] = Field(..., min_length=1, description="List of components in series")
    
    frequency: float = Field(..., gt=0, description="Frequency value")
    frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, description="Frequency unit (hz, khz, mhz, ghz)")
    
    # Private field for converted frequency
    _frequency_hz: float = PrivateAttr(None)
    
    @staticmethod
    def to_hz(value: float, unit: FrequencyUnit) -> float:
        """Convert frequency to Hertz"""
        if unit == FrequencyUnit.HZ:
            return value
        elif unit == FrequencyUnit.KHZ:
            return value * 1000
        elif unit == FrequencyUnit.MHZ:
            return value * 1_000_000
        elif unit == FrequencyUnit.GHZ:
            return value * 1_000_000_000
        return value
    
    @model_validator(mode='after')
    def convert_frequency(self) -> 'SeriesImpedanceModel':
        """Convert frequency to Hz"""
        self._frequency_hz = self.to_hz(self.frequency, self.frequency_unit)
        return self
    
class ParallelComponentItem(BaseModel):
    """Single component in parallel circuit"""
    
    type: ComponentType = Field(..., description="Component type: 'R', 'C', or 'L'")
    value: float = Field(..., gt=0, description="Component value")
    
    # Optional units (only used for C and L)
    capacitance_unit: CapacitanceUnit = Field(CapacitanceUnit.UF, description="For type='C': f, mf, uf, nf, pf")
    inductance_unit: InductanceUnit = Field(InductanceUnit.UH, description="For type='L': h, mh, uh, nh, ph")
    
    # Private field for converted base value
    _base_value: float = PrivateAttr(None)
    
    @staticmethod
    def to_farad(value: float, unit: CapacitanceUnit) -> float:
        if unit == CapacitanceUnit.F:
            return value
        elif unit == CapacitanceUnit.MF:
            return value * 1e-3
        elif unit == CapacitanceUnit.UF:
            return value * 1e-6
        elif unit == CapacitanceUnit.NF:
            return value * 1e-9
        elif unit == CapacitanceUnit.PF:
            return value * 1e-12
        return value
    
    @staticmethod
    def to_henry(value: float, unit: InductanceUnit) -> float:
        if unit == InductanceUnit.H:
            return value
        elif unit == InductanceUnit.MH:
            return value * 1e-3
        elif unit == InductanceUnit.UH:
            return value * 1e-6
        elif unit == InductanceUnit.NH:
            return value * 1e-9
        elif unit == InductanceUnit.PH:
            return value * 1e-12
        return value
    
    @model_validator(mode='after')
    def convert_value(self) -> 'ParallelComponentItem':
        if self.type == ComponentType.C:
            self._base_value = self.to_farad(self.value, self.capacitance_unit)
        elif self.type == ComponentType.L:
            self._base_value = self.to_henry(self.value, self.inductance_unit)
        else:
            self._base_value = self.value
        return self


class ParallelImpedanceModel(BaseModel):
    """Request model for parallel impedance calculator"""
    
    components: List[ParallelComponentItem] = Field(..., min_length=1, description="List of components in parallel")
    
    frequency: float = Field(..., gt=0, description="Frequency value")
    frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, description="Frequency unit (hz, khz, mhz, ghz)")
    
    # Private field for converted frequency
    _frequency_hz: float = PrivateAttr(None)
    
    @staticmethod
    def to_hz(value: float, unit: FrequencyUnit) -> float:
        if unit == FrequencyUnit.HZ:
            return value
        elif unit == FrequencyUnit.KHZ:
            return value * 1000
        elif unit == FrequencyUnit.MHZ:
            return value * 1_000_000
        elif unit == FrequencyUnit.GHZ:
            return value * 1_000_000_000
        return value
    
    @model_validator(mode='after')
    def convert_frequency(self) -> 'ParallelImpedanceModel':
        self._frequency_hz = self.to_hz(self.frequency, self.frequency_unit)
        return self


