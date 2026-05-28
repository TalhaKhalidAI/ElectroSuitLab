import math

class ElectronicsCalculator:
    """Complete BJT calculator for Common Emitter, Common Base, and Common Collector configurations"""
    
    def __init__(self):
        pass
    
    @staticmethod
    def to_ohm(value: float, unit: str) -> float:
        """Convert resistance value to Ohms"""
        unit = unit.lower().strip()
        if unit in ['k', 'kohm', 'kω', 'kΩ']:
            return value * 1000
        elif unit in ['m', 'mohm', 'mω', 'mΩ']:
            return value * 1_000_000
        elif unit in ['', 'ohm', 'ω', 'Ω']:
            return value
        else:
            raise ValueError(f"Unknown unit: {unit}")
    
    @staticmethod
    def to_farad(value: float, unit: str) -> float:
        """Convert capacitance value to Farads"""
        unit = unit.lower().strip()
        if unit in ['p', 'pf']:
            return value * 1e-12
        elif unit in ['n', 'nf']:
            return value * 1e-9
        elif unit in ['u', 'uf', 'μ', 'μf']:
            return value * 1e-6
        elif unit in ['m', 'mf']:
            return value * 1e-3
        elif unit in ['', 'f']:
            return value
        else:
            raise ValueError(f"Unknown unit: {unit}")
    
    @staticmethod
    def _check_saturation(Vc, Ve, Vcc):
        """
        Check transistor bias condition.
        
        Args:
            Vc: Collector voltage (V)
            Ve: Emitter voltage (V)
            Vcc: Supply voltage (V)
        
        Returns:
            str: Bias status description
        """
        if Vc < Ve + 0.1:                     # Vc very close to Ve → saturated
            return "saturated (valve fully open)"
        elif Vc > Vcc - 0.5:                  # Vc near Vcc → cutoff
            return "cutoff (valve closed)"
        else:
            return "active (valve half open) - good amplification"
    
    # ================================================================
    # COMMON EMITTER (Base in, Collector out, Emitter ground)
    # ================================================================
    def common_emitter(self, Vcc: float, Rc: float, Re: float, R1: float, R2: float, beta: float, RL: float = float('inf')):
        """
        Common Emitter Amplifier Calculator
        
        Args:
            Vcc: Supply voltage (V)
            Rc: Collector resistor (Ω)
            Re: Emitter resistor (Ω)
            R1: Base bias resistor to Vcc (Ω)
            R2: Base bias resistor to GND (Ω)
            beta: Transistor current gain (hFE)
            RL: Load resistor (Ω), default = infinity (no load)
        
        Returns:
            dict: All calculated values
        """
        # DC bias
        Vb = Vcc * (R2 / (R1 + R2))
        Ve = Vb - 0.6
        Ie = Ve / Re
        Ic = Ie * (beta / (beta + 1))
        Ib = Ie / (beta + 1)
        
        V_Rc = Ic * Rc
        Vc = Vcc - V_Rc
        if Vc < Ve:
            # Transistor is saturated, Vc cannot go below Ve
            Vc = Ve + 0.05  # Slightly above Ve
            V_Rc = Vcc - Vc
            Ic = V_Rc / Rc
            # Recalculate Ie, Ib from Ic
            Ie = Ic * ((beta + 1) / beta)
            Ib = Ie / (beta + 1)
        
        Vce = Vc - Ve
    
        # Gain
        gain_approx = Rc / Re
        gm = Ic / 0.026
        Rc_eff = Rc if RL == float('inf') else (Rc * RL) / (Rc + RL)
        gain_exact = -gm * Rc_eff
        
        # Power
        P_Q = Vce * Ic
        P_Rc = V_Rc * Ic
        P_Re = Ve * Ie
        
        # Input/Output Impedance
        Rin = 1 / ((1/R1) + (1/R2) + (1/(beta * Re)))
        Rout = Rc
        
        return {
            "configuration": "Common Emitter",
            "voltages": {
                "Vb": round(Vb, 2),
                "Ve": round(Ve, 2),
                "Vc": round(Vc, 2),
                "Vce": round(Vce, 2)
            },
            "currents": {
                "Ib_uA": round(Ib * 1e6, 2),
                "Ic_mA": round(Ic * 1000, 2),
                "Ie_mA": round(Ie * 1000, 2)
            },
            "gain": {
                "approx": round(gain_approx, 1),
                "exact": round(gain_exact, 1)
            },
            "impedance": {
                "Zin_ohm": round(Rin, 0),
                "Zout_ohm": round(Rout, 0)
            },
            "power_mW": {
                "transistor": round(P_Q * 1000, 1),
                "Rc": round(P_Rc * 1000, 1),
                "Re": round(P_Re * 1000, 1)
            },
            "bias_status": self._check_saturation(Vc,Ve,Vcc),
            "phase_shift": "180° (inverted)"
        }
    
    # ================================================================
    # COMMON BASE (Emitter in, Collector out, Base ground)
    # ================================================================
    def common_base(self, Vcc: float, Rc: float, Re: float, Vbias: float, beta: float, RL: float = float('inf')):
        """
        Common Base Amplifier Calculator
        
        Args:
            Vcc: Supply voltage (V)
            Rc: Collector resistor (Ω)
            Re: Emitter resistor (Ω)
            Vbias: Base bias voltage (V) - externally set
            beta: Transistor current gain (hFE)
            RL: Load resistor (Ω), default = infinity (no load)
        
        Returns:
            dict: All calculated values
        """
        # DC bias (base is fixed, emitter follows)
        Vb = Vbias
        Ve = Vb - 0.6
        Ie = Ve / Re
        Ic = Ie * (beta / (beta + 1))
        Ib = Ie / (beta + 1)
        
        V_Rc = Ic * Rc
        Vc = Vcc - V_Rc

        if Ve < 0:
            Ve = 0.05  # Can't go below 0V
            # Recalculate Vb? No, Vb is fixed externally
            # But Ve cannot be negative!
        
        Ie = Ve / Re
        Ic = Ie * (beta / (beta + 1))
        Ib = Ie / (beta + 1)
        
        V_Rc = Ic * Rc
        Vc = Vcc - V_Rc
        
        # *** SATURATION CLAMP FOR Vc ***
        if Vc < Ve:
            Vc = Ve + 0.05
            V_Rc = Vcc - Vc
            Ic = V_Rc / Rc
            Ie = Ic * ((beta + 1) / beta)
            Ib = Ie / (beta + 1)
        
        Vcb = Vc - Vb
        
        # Gain (same as CE but non-inverting)
        gain_approx = Rc / Re
        gm = Ic / 0.026
        Rc_eff = Rc if RL == float('inf') else (Rc * RL) / (Rc + RL)
        gain_exact = gm * Rc_eff  # Positive gain (non-inverting)
        
        # Power
        P_Q = Vcb * Ic
        P_Rc = V_Rc * Ic
        P_Re = Ve * Ie
        
        # Input/Output Impedance (very low input Z)
        Rin = 1 / gm  # ~ 26mV / Ic
        Rout = Rc
        
        return {
            "configuration": "Common Base",
            "voltages": {
                "Vb": round(Vb, 2),
                "Ve": round(Ve, 2),
                "Vc": round(Vc, 2),
                "Vcb": round(Vcb, 2)
            },
            "currents": {
                "Ib_uA": round(Ib * 1e6, 2),
                "Ic_mA": round(Ic * 1000, 2),
                "Ie_mA": round(Ie * 1000, 2)
            },
            "gain": {
                "approx": round(gain_approx, 1),
                "exact": round(gain_exact, 1)
            },
            "impedance": {
                "Zin_ohm": round(Rin, 0),
                "Zout_ohm": round(Rout, 0)
            },
            "power_mW": {
                "transistor": round(P_Q * 1000, 1),
                "Rc": round(P_Rc * 1000, 1),
                "Re": round(P_Re * 1000, 1)
            },
            "bias_status": self._check_saturation(Vc,Ve,Vcc),
            "phase_shift": "0° (non-inverting)"
        }
    
    # ================================================================
    # COMMON COLLECTOR (Base in, Emitter out, Collector ground)
    # ================================================================
    def common_collector(self, Vcc: float, Re: float, R1: float, R2: float, beta: float, Rsource: float = 0):
        """
        Common Collector (Emitter Follower) Amplifier Calculator
        
        Args:
            Vcc: Supply voltage (V)
            Re: Emitter resistor (Ω)
            R1: Base bias resistor to Vcc (Ω)
            R2: Base bias resistor to GND (Ω)
            beta: Transistor current gain (hFE)
            Rsource: Source resistance (Ω), default = 0
        
        Returns:
            dict: All calculated values
        """
        # DC bias
        Vb = Vcc * (R2 / (R1 + R2))
        Ve = Vb - 0.6
        Ie = Ve / Re
        Ic = Ie * (beta / (beta + 1))
        Ib = Ie / (beta + 1)

        Vc = Vcc
        
        # *** SATURATION CLAMP FOR Ve ***
        if Ve < 0:
            Ve = 0.05  # Can't go below 0V
        if Ve > Vcc:
            Ve = Vcc - 0.05  # Can't exceed Vcc
        
        # Recalculate currents after clamp
        Ie = Ve / Re
        Ic = Ie * (beta / (beta + 1))
        Ib = Ie / (beta + 1)
        
        Vce = Vcc - Ve  # Collector is at Vcc, emitter below
        
        # Gain (≈1)
        gain_approx = 0.98  # typical
        gm = Ic / 0.026 if Ic > 0 else 0
        re = 0.026 / Ie if Ie > 0 else 1000  # intrinsic emitter resistance
        rpi = beta * re if beta > 0 else 0

        # Exact gain:
        if Rsource + rpi + (beta + 1) * Re > 0:
            gain_exact = (beta * Re) / (Rsource + rpi + (beta + 1) * Re)
        else:
            gain_exact = 0

        # Input/Output Impedance
        Rin = beta * Re if Re > 0 else 0  # very high
        Rout = (Rsource / beta) + re if beta > 0 else re
        
        # Power
        P_Q = Vce * Ic
        P_Re = Ve * Ie
        
        # ================================================================
        # BIAS STATUS FOR COMMON COLLECTOR (Fixed!)
        # ================================================================
        if Ve < 0.2:
            bias_status = "cutoff (valve closed)"
        elif Ve > Vcc - 0.2:
            bias_status = "saturated (valve fully open)"
        else:
            bias_status = "active (valve half open) - good amplification"
        
        return {
            "configuration": "Common Collector (Emitter Follower)",
            "voltages": {
                "Vb": round(Vb, 2),
                "Ve": round(Ve, 2),
                "Vc": round(Vc, 2),
                "Vce": round(Vce, 2)
            },
            "currents": {
                "Ib_uA": round(Ib * 1e6, 2),
                "Ic_mA": round(Ic * 1000, 2),
                "Ie_mA": round(Ie * 1000, 2)
            },
            "gain": {
                "approx": round(gain_approx, 2),
                "exact": round(gain_exact, 3)
            },
            "impedance": {
                "Zin_ohm": round(Rin, 0),
                "Zout_ohm": round(Rout, 1)
            },
            "power_mW": {
                "transistor": round(P_Q * 1000, 1),
                "Re": round(P_Re * 1000, 1)
            },
            "bias_status": bias_status,  # ✅ FIXED
            "phase_shift": "0° (non-inverting)"
        }
    
    # ================================================================
    # OHM'S LAW & KIRCHHOFF HELPERS
    # ================================================================
    def ohms_law(self, voltage=None, current=None, resistance=None):
        """Calculate missing value using Ohm's Law: V = I × R"""
        if voltage is not None and current is not None:
            return {"resistance": round(voltage / current, 2)}
        elif voltage is not None and resistance is not None:
            return {"current": round(voltage / resistance, 6)}
        elif current is not None and resistance is not None:
            return {"voltage": round(current * resistance, 2)}
        else:
            raise ValueError("Need at least two of: voltage, current, resistance")
    
    def voltage_divider(self, Vcc, R1, R2):
        """Calculate output voltage of a voltage divider"""
        Vout = Vcc * (R2 / (R1 + R2))
        return {"Vout": round(Vout, 2)}
    
    def rc_cutoff(self, R, C):
        """Calculate RC low-pass/high-pass cutoff frequency"""
        f = 1 / (2 * math.pi * R * C)
        return {"cutoff_freq_hz": round(f, 2)}
    # ================================================================
    # MOSFET COMMON SOURCE (Gate in, Drain out, Source ground)
    # ================================================================

    def common_source_mosfet(self, Vdd: float, Rd: float, R1: float, R2: float, 
                            Vth: float, K: float, RL: float = float('inf'), 
                            Rs: float = 0):
        """
        Common Source MOSFET Amplifier Calculator (Corrected)
        """
        # Gate voltage (voltage divider — no gate current!)
        Vg = Vdd * (R2 / (R1 + R2))
        
        if Rs == 0:
            Vgs = Vg
            Id = K * (Vgs - Vth)**2 if Vgs > Vth else 0
            Vs = 0
        else:
            a = K * Rs**2
            b = -(2 * K * Rs * (Vg - Vth) + 1)
            c = K * (Vg - Vth)**2
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                Id = 0
            else:
                Id = (-b - math.sqrt(discriminant)) / (2*a)
            Vs = Id * Rs
            Vgs = Vg - Vs
        
        Vd_calc = Vdd - (Id * Rd)
        
        # *** SATURATION CLAMP (FIX) ***
        if Vd_calc < 0.2:
            Vd = 0.2
            Id = (Vdd - Vd) / Rd
            if Rs > 0:
                Vs = Id * Rs
                Vgs = Vg - Vs
            else:
                Vs = 0
                Vgs = Vg
            Vds = Vd - Vs
        else:
            Vd = Vd_calc
            Vds = Vd - Vs
        
        Vov = Vgs - Vth if Vgs > Vth else 0
        
        if Vds >= Vov and Vov > 0:
            region = "saturation (active) — good for amplification"
        else:
            region = "triode (linear) — not ideal for amplification"
        
        gm = 2 * K * Vov if Vov > 0 else 0
        Rd_eff = Rd if RL == float('inf') else (Rd * RL) / (Rd + RL)
        gain = -gm * Rd_eff
        
        Zin = (R1 * R2) / (R1 + R2)
        Zout = Rd
        
        P_Q = Vds * Id
        P_Rd = (Vdd - Vd) * Id
        P_Rs = Vs * Id if Rs > 0 else 0
        
        return {
            "configuration": "Common Source (MOSFET)",
            "voltages": {
                "Vg": round(Vg, 2),
                "Vs": round(Vs, 2),
                "Vd": round(Vd, 2),
                "Vgs": round(Vgs, 2),
                "Vds": round(Vds, 2),
                "Vov": round(Vov, 2)
            },
            "currents": {
                "Id_mA": round(Id * 1000, 2)
            },
            "gain": {
                "gm_mS": round(gm * 1000, 2),
                "voltage_gain": round(gain, 1)
            },
            "impedance": {
                "Zin_kohm": round(Zin / 1000, 0),
                "Zout_ohm": round(Zout, 0)
            },
            "power_mW": {
                "transistor": round(P_Q * 1000, 1),
                "Rd": round(P_Rd * 1000, 1),
                "Rs": round(P_Rs * 1000, 1)
            },
            "region": region,
            "phase_shift": "180° (inverted)"
        }


    # ================================================================
    # MOSFET COMMON DRAIN (Source Follower) — Gate in, Source out
    # ================================================================
    def common_drain_mosfet(self, Vdd: float, R1: float, R2: float, Rs: float,
                            Vth: float, K: float, Rsource: float = 0):
        """
        Common Drain MOSFET Amplifier (Source Follower)
        
        Args:
            Vdd: Supply voltage (V)
            R1: Gate bias resistor to Vdd (Ω)
            R2: Gate bias resistor to GND (Ω)
            Rs: Source resistor (Ω)
            Vth: Threshold voltage (V)
            K: Transconductance parameter (A/V²)
            Rsource: Source resistance (Ω), default = 0
        
        Returns:
            dict: All calculated values
        """
        # Gate voltage (voltage divider)
        Vg = Vdd * (R2 / (R1 + R2))
        
        # Solve for Id (MOSFET in saturation)
        # Vgs = Vg - Vs = Vg - Id×Rs
        # Id = K × (Vg - Id×Rs - Vth)²
        a = K * Rs**2
        b = -(2 * K * Rs * (Vg - Vth) + 1)
        c = K * (Vg - Vth)**2
        
        Id = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
        Vs = Id * Rs
        Vgs = Vg - Vs
        Vds = Vdd - Vs
        
        # Gain (≈1)
        gm = 2 * K * (Vgs - Vth)
        gain = (gm * Rs) / (1 + gm * (Rs + Rsource))
        
        # Input/Output Impedance
        Zin = (R1 * R2) / (R1 + R2)  # very high
        Zout = 1 / gm  # low output impedance
        
        # Power
        P_Q = Vds * Id
        P_Rs = Vs * Id
        
        return {
            "configuration": "Common Drain (Source Follower)",
            "voltages": {
                "Vg": round(Vg, 2),
                "Vs": round(Vs, 2),
                "Vgs": round(Vgs, 2),
                "Vds": round(Vds, 2)
            },
            "currents": {
                "Id_mA": round(Id * 1000, 2)
            },
            "gain": {
                "gm_mS": round(gm * 1000, 2),
                "voltage_gain": round(gain, 3)
            },
            "impedance": {
                "Zin_kohm": round(Zin / 1000, 0),
                "Zout_ohm": round(Zout, 1)
            },
            "power_mW": {
                "transistor": round(P_Q * 1000, 1),
                "Rs": round(P_Rs * 1000, 1)
            },
            "phase_shift": "0° (non-inverting)"
        }


    # ================================================================
    # MOSFET COMMON GATE (Source in, Drain out, Gate ground)
    # ================================================================
    def common_gate_mosfet(self, Vdd: float, Rd: float, Rs: float, Vbias: float,
                            Vth: float, K: float, RL: float = float('inf')):
        """
        Common Gate MOSFET Amplifier Calculator
        
        Args:
            Vdd: Supply voltage (V)
            Rd: Drain resistor (Ω)
            Rs: Source resistor (Ω)
            Vbias: Gate bias voltage (V) — externally set
            Vth: Threshold voltage (V)
            K: Transconductance parameter (A/V²)
            RL: Load resistor (Ω), default = infinity
        
        Returns:
            dict: All calculated values
        """
        # Gate fixed, source follows
        Vg = Vbias
        Vs = Vg - Vth - 0.5  # initial guess, but we solve properly
        
        # Solve for Id in saturation
        # Vgs = Vg - Vs
        # Id = K × (Vgs - Vth)² = K × (Vg - Vs - Vth)²
        # Also Vs = Id × Rs
        # So Id = K × (Vg - Id×Rs - Vth)²
        
        a = K * Rs**2
        b = -(2 * K * Rs * (Vg - Vth) + 1)
        c = K * (Vg - Vth)**2
        
        Id = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
        Vs = Id * Rs
        Vgs = Vg - Vs
        Vd = Vdd - (Id * Rd)
        Vds = Vd - Vs
        
        # Gain
        gm = 2 * K * (Vgs - Vth)
        Rd_eff = Rd if RL == float('inf') else (Rd * RL) / (Rd + RL)
        gain = gm * Rd_eff  # positive gain (non-inverting)
        
        # Input/Output Impedance (very low input Z)
        Zin = 1 / gm
        Zout = Rd
        
        # Power
        P_Q = Vds * Id
        P_Rd = (Vdd - Vd) * Id
        P_Rs = Vs * Id
        
        return {
            "configuration": "Common Gate (MOSFET)",
            "voltages": {
                "Vg": round(Vg, 2),
                "Vs": round(Vs, 2),
                "Vd": round(Vd, 2),
                "Vgs": round(Vgs, 2),
                "Vds": round(Vds, 2)
            },
            "currents": {
                "Id_mA": round(Id * 1000, 2)
            },
            "gain": {
                "gm_mS": round(gm * 1000, 2),
                "voltage_gain": round(gain, 1)
            },
            "impedance": {
                "Zin_ohm": round(Zin, 0),
                "Zout_ohm": round(Zout, 0)
            },
            "power_mW": {
                "transistor": round(P_Q * 1000, 1),
                "Rd": round(P_Rd * 1000, 1),
                "Rs": round(P_Rs * 1000, 1)
            },
            "phase_shift": "0° (non-inverting)"
        }
        
    # ================================================================
    # UNIT CONVERSION (Resistance & Capacitance)
    # ================================================================

    @staticmethod
    def convert_resistance(value: float, from_unit: str, to_unit: str = 'ohm') -> float:
        """
        Convert resistance between units
        
        Args:
            value: Resistance value
            from_unit: 'ohm', 'k', 'm' (kΩ, MΩ)
            to_unit: 'ohm', 'k', 'm' (default 'ohm')
        
        Returns:
            Converted value in target unit
        """
        # First convert to Ohms
        from_unit = from_unit.lower().strip()
        if from_unit in ['k', 'kohm', 'kω', 'kΩ']:
            ohms = value * 1000
        elif from_unit in ['m', 'mohm', 'mω', 'mΩ']:
            ohms = value * 1_000_000
        elif from_unit in ['', 'ohm', 'ω', 'Ω']:
            ohms = value
        else:
            raise ValueError(f"Unknown resistance unit: {from_unit}")
        
        # Then convert to target unit
        to_unit = to_unit.lower().strip()
        if to_unit in ['k', 'kohm', 'kω', 'kΩ']:
            return ohms / 1000
        elif to_unit in ['m', 'mohm', 'mω', 'mΩ']:
            return ohms / 1_000_000
        elif to_unit in ['', 'ohm', 'ω', 'Ω']:
            return ohms
        else:
            raise ValueError(f"Unknown resistance unit: {to_unit}")


    @staticmethod
    def convert_capacitance(value: float, from_unit: str, to_unit: str = 'f') -> float:
        """
        Convert capacitance between units
        
        Args:
            value: Capacitance value
            from_unit: 'p', 'n', 'u', 'm', 'f' (pF, nF, µF, mF, F)
            to_unit: 'p', 'n', 'u', 'm', 'f' (default 'f')
        
        Returns:
            Converted value in target unit
        """
        # First convert to Farads
        from_unit = from_unit.lower().strip()
        if from_unit in ['p', 'pf']:
            farads = value * 1e-12
        elif from_unit in ['n', 'nf']:
            farads = value * 1e-9
        elif from_unit in ['u', 'uf', 'μ', 'μf']:
            farads = value * 1e-6
        elif from_unit in ['m', 'mf']:
            farads = value * 1e-3
        elif from_unit in ['', 'f']:
            farads = value
        else:
            raise ValueError(f"Unknown capacitance unit: {from_unit}")
        
        # Then convert to target unit
        to_unit = to_unit.lower().strip()
        if to_unit in ['p', 'pf']:
            return farads / 1e-12
        elif to_unit in ['n', 'nf']:
            return farads / 1e-9
        elif to_unit in ['u', 'uf', 'μ', 'μf']:
            return farads / 1e-6
        elif to_unit in ['m', 'mf']:
            return farads / 1e-3
        elif to_unit in ['', 'f']:
            return farads
        else:
            raise ValueError(f"Unknown capacitance unit: {to_unit}")


    # ================================================================
    # LC RESONANCE (Colpitts, Hartley, Tank Circuits)
    # ================================================================
    @staticmethod
    def _format_frequency(f_hz: float) -> dict:
        """
        Auto-format frequency to best unit (Hz, kHz, MHz, GHz)
        
        Args:
            f_hz: Frequency in Hertz
        
        Returns:
            dict with value and unit
        """
        if f_hz >= 1e9:
            return {"value": round(f_hz / 1e9, 4), "unit": "GHz"}
        elif f_hz >= 1e6:
            return {"value": round(f_hz / 1e6, 4), "unit": "MHz"}
        elif f_hz >= 1e3:
            return {"value": round(f_hz / 1e3, 2), "unit": "kHz"}
        else:
            return {"value": round(f_hz, 2), "unit": "Hz"}
        

    def lc_resonance(self, L: float = None, C: float = None, f: float = None):
        """
        Calculate LC resonance frequency, inductance, or capacitance.
        
        Formula: f = 1 / (2π × √(L × C))
        
        Args:
            L: Inductance (Henries) — provide if calculating f or C
            C: Capacitance (Farads) — provide if calculating f or L
            f: Frequency (Hz) — provide if calculating L or C
        
        Returns:
            dict: Calculated value(s) with auto-formatted frequency
        """
        import math
        
        # Case 1: Calculate frequency (given L and C)
        if L is not None and C is not None:
            f_hz = 1 / (2 * math.pi * math.sqrt(L * C))
            formatted = self._format_frequency(f_hz)
            
            return {
                "frequency": {
                    "value": formatted["value"],
                    "unit": formatted["unit"],
                    "hz": round(f_hz, 2),
                    "khz": round(f_hz / 1000, 2),
                    "mhz": round(f_hz / 1e6, 4)
                },
                "L_h": L,
                "L_uh": L * 1e6,
                "C_f": C,
                "C_pf": C * 1e12
            }
        
        # Case 2: Calculate inductance (given f and C)
        elif f is not None and C is not None:
            L = 1 / ((2 * math.pi * f) ** 2 * C)
            formatted = self._format_frequency(f)
            
            return {
                "inductance": {
                    "h": round(L, 10),
                    "mh": round(L * 1000, 4),
                    "uh": round(L * 1e6, 2)
                },
                "frequency": {
                    "value": formatted["value"],
                    "unit": formatted["unit"],
                    "hz": f
                },
                "C_f": C,
                "C_pf": C * 1e12
            }
        
        # Case 3: Calculate capacitance (given f and L)
        elif f is not None and L is not None:
            C = 1 / ((2 * math.pi * f) ** 2 * L)
            formatted = self._format_frequency(f)
            
            return {
                "capacitance": {
                    "f": round(C, 12),
                    "uf": round(C * 1e6, 4),
                    "nf": round(C * 1e9, 2),
                    "pf": round(C * 1e12, 1)
                },
                "frequency": {
                    "value": formatted["value"],
                    "unit": formatted["unit"],
                    "hz": f
                },
                "L_h": L,
                "L_uh": L * 1e6
            }
        
        else:
            raise ValueError("Need at least two of: L, C, f")


    def colpitts_frequency(self, L: float, C1: float, C2: float):
        """
        Calculate Colpitts oscillator frequency.
        
        Formula: f = 1 / (2π × √(L × C_total))
        where C_total = (C1 × C2) / (C1 + C2)
        
        Args:
            L: Inductance (Henries)
            C1: Capacitor 1 (Farads)
            C2: Capacitor 2 (Farads)
        
        Returns:
            dict: Frequency with auto-format, total capacitance
        """
        C_total = (C1 * C2) / (C1 + C2)
        f_hz = 1 / (2 * math.pi * math.sqrt(L * C_total))
        
        # Auto-format frequency
        formatted = self._format_frequency(f_hz)
        
        return {
            "frequency": {
                "value": formatted["value"],
                "unit": formatted["unit"],
                "hz": round(f_hz, 2),
                "khz": round(f_hz / 1000, 2),
                "mhz": round(f_hz / 1e6, 4)
            },
            "C_total": {
                "f": round(C_total, 12),
                "pf": round(C_total * 1e12, 2)
            },
            "L_uh": round(L * 1e6, 2),
            "C1_pf": round(C1 * 1e12, 2),
            "C2_pf": round(C2 * 1e12, 2)
        }


    def hartley_frequency(self, L1: float, L2: float, C: float, M: float = 0):
        """
        Calculate Hartley oscillator frequency.
        
        Formula: f = 1 / (2π × √((L1 + L2 + 2M) × C))
        
        Args:
            L1: Inductance 1 (Henries)
            L2: Inductance 2 (Henries)
            C: Capacitance (Farads)
            M: Mutual inductance (default 0 for no coupling)
        
        Returns:
            dict: Frequency with auto-format, total inductance
        """
        L_total = L1 + L2 + (2 * M)
        f_hz = 1 / (2 * math.pi * math.sqrt(L_total * C))
        
        # Auto-format frequency
        formatted = self._format_frequency(f_hz)
        
        return {
            "frequency": {
                "value": formatted["value"],
                "unit": formatted["unit"],
                "hz": round(f_hz, 2),
                "khz": round(f_hz / 1000, 2),
                "mhz": round(f_hz / 1e6, 4)
            },
            "L_total": {
                "h": round(L_total, 8),
                "mh": round(L_total * 1000, 4),
                "uh": round(L_total * 1e6, 2)
            },
            "C_pf": round(C * 1e12, 2),
            "L1_uh": round(L1 * 1e6, 2),
            "L2_uh": round(L2 * 1e6, 2),
            "M_uh": round(M * 1e6, 2) if M != 0 else None
        }
    
    def ne555_astable(self, R1: float, R2: float, C: float):
        """
        555 Timer Astable Mode Calculator
        
        Formulas:
            t_high = 0.693 × (R1 + R2) × C
            t_low  = 0.693 × R2 × C
            f = 1.44 / ((R1 + 2 × R2) × C)
        
        Args:
            R1: Resistor from Vcc to Discharge (Ohms)
            R2: Resistor from Discharge to Threshold (Ohms)
            C: Capacitor from Threshold to GND (Farads)
        
        Returns:
            dict: Timing and frequency with auto-formatted units
        """
        
        t_high = 0.693 * (R1 + R2) * C
        t_low = 0.693 * R2 * C
        period = t_high + t_low
        frequency_hz = 1.44 / ((R1 + 2 * R2) * C)
        duty_cycle = ((R1 + R2) / (R1 + 2 * R2)) * 100
        
        # Auto-format frequency
        formatted_freq = self._format_frequency(frequency_hz)
        
        # Auto-format time values
        def format_time(t):
            if t >= 1:
                return round(t, 4), "s"
            elif t >= 1e-3:
                return round(t * 1000, 2), "ms"
            elif t >= 1e-6:
                return round(t * 1e6, 2), "µs"
            else:
                return round(t * 1e9, 2), "ns"
        
        t_high_val, t_high_unit = format_time(t_high)
        t_low_val, t_low_unit = format_time(t_low)
        period_val, period_unit = format_time(period)
        
        return {
            "frequency": {
                "value": formatted_freq["value"],
                "unit": formatted_freq["unit"],
                "hz": round(frequency_hz, 2),
                "khz": round(frequency_hz / 1000, 2),
                "mhz": round(frequency_hz / 1e6, 4)
            },
            "timing": {
                "t_high": {"value": t_high_val, "unit": t_high_unit},
                "t_low": {"value": t_low_val, "unit": t_low_unit},
                "period": {"value": period_val, "unit": period_unit}
            },
            "duty_cycle_percent": round(duty_cycle, 1)
        }
    
    def ne555_astable_inverse(self, target_freq_hz: float, C: float = None, 
                            duty_cycle_target: float = None, R2_ratio: float = 0.5):
        """
        555 Timer Inverse Calculator: Find components from frequency.
        
        Formula: R1 + 2×R2 = 1.44 / (f × C)
        
        Args:
            target_freq_hz: Desired frequency (Hz)
            C: Capacitance (Farads) — if provided, calculates R1,R2
            duty_cycle_target: Desired duty cycle % (optional, 50-80 typical)
            R2_ratio: R2 / (R1+R2) ratio (default 0.5 = equal)
        
        Returns:
            dict: Recommended R1, R2, C values
        """
        
        # If C is provided, calculate R1 and R2
        if C is not None:
            total_R = 1.44 / (target_freq_hz * C)  # R1 + 2×R2
            
            if duty_cycle_target is not None:
                # Solve for R1, R2 from duty cycle
                # Duty = (R1+R2)/(R1+2R2)
                # Let r = R2/R1, then solve
                # Duty = (1+r)/(1+2r)
                r = (1 - duty_cycle_target/100) / ((2 * duty_cycle_target/100) - 1)
                if r < 0:
                    # Use default ratio
                    R2 = total_R / 3
                    R1 = total_R - 2 * R2
                else:
                    R2 = total_R / (1/r + 2)
                    R1 = R2 / r
            else:
                # Standard: R1 = R2
                R2 = total_R / 3
                R1 = total_R - 2 * R2
            
            # Round to standard resistor values (E12 series)
            def to_std_resistor(val):
                std_values = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, 100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820]
                val_k = val / 1000
                closest = min(std_values, key=lambda x: abs(x - val_k))
                return closest * 1000
            
            R1_std = to_std_resistor(R1)
            R2_std = to_std_resistor(R2)
            
            # Calculate actual frequency with standard values
            actual_freq = 1.44 / ((R1_std + 2 * R2_std) * C)
            actual_duty = ((R1_std + R2_std) / (R1_std + 2 * R2_std)) * 100
            
            formatted_freq = self._format_frequency(actual_freq)
            
            return {
                "recommended": {
                    "R1_ohm": round(R1_std),
                    "R1_kohm": round(R1_std / 1000, 1),
                    "R2_ohm": round(R2_std),
                    "R2_kohm": round(R2_std / 1000, 1),
                    "C_f": C,
                    "C_uF": round(C * 1e6, 3),
                    "C_nF": round(C * 1e9, 1)
                },
                "resulting_frequency": {
                    "value": formatted_freq["value"],
                    "unit": formatted_freq["unit"],
                    "hz": round(actual_freq, 2)
                },
                "resulting_duty_cycle": round(actual_duty, 1),
                "formula": "R1 + 2×R2 = 1.44 / (f × C)"
            }
        
        else:
            # Suggest C value based on frequency range
            if target_freq_hz < 1:
                C_uF = 1000  # 1000µF
                C_range = "very large (1000µF)"
            elif target_freq_hz < 10:
                C_uF = 100   # 100µF
                C_range = "large (100µF)"
            elif target_freq_hz < 100:
                C_uF = 10    # 10µF
                C_range = "medium (10µF)"
            elif target_freq_hz < 1000:
                C_uF = 1     # 1µF
                C_range = "standard (1µF)"
            elif target_freq_hz < 10000:
                C_uF = 0.1   # 100nF
                C_range = "common (100nF)"
            elif target_freq_hz < 100000:
                C_uF = 0.01  # 10nF
                C_range = "small (10nF)"
            else:
                C_uF = 0.001  # 1nF
                C_range = "very small (1nF)"
            
            C_f = C_uF / 1_000_000
            
            return {
                "suggestion": {
                    "message": f"For {target_freq_hz} Hz, use {C_range} capacitor",
                    "recommended_C_uF": C_uF,
                    "recommended_C_f": C_f
                },
                "next_step": f"Call with C={C_f} to get R1,R2 values"
            }


    # ================================================================
    # KIRCHHOFF'S VOLTAGE LAW (KVL) CALCULATOR
    # ================================================================

    def kvl_series_circuit(self, Vsupply: float, resistors: list):
        """
        Calculate voltages, currents, and power in a series circuit using KVL.
        
        Kirchhoff's Voltage Law: Sum of all voltage drops = Supply voltage
        
        Args:
            Vsupply: Supply voltage (V)
            resistors: List of resistor values in Ohms [R1, R2, R3, ...]
        
        Returns:
            dict: Current, voltage drops, power, KVL verification
        """
        import math
        
        # Total resistance
        R_total = sum(resistors)
        
        # Current (Ohm's Law: I = V / R_total)
        I_total = Vsupply / R_total
        
        # Voltage drops and power for each resistor
        voltage_drops = []
        power_dissipation = []
        for i, R in enumerate(resistors, 1):
            V_drop = I_total * R
            P_drop = I_total ** 2 * R
            voltage_drops.append({"resistor": f"R{i}", "resistance_ohm": R, "voltage_v": round(V_drop, 2)})
            power_dissipation.append({"resistor": f"R{i}", "power_mw": round(P_drop * 1000, 2), "power_w": round(P_drop, 4)})
        
        # Sum of voltage drops (KVL check)
        sum_Vdrops = sum([v["voltage_v"] for v in voltage_drops])
        
        # Format voltage values with auto-unit
        def format_voltage(v):
            if v >= 1:
                return f"{v:.2f} V"
            elif v >= 1e-3:
                return f"{v*1000:.2f} mV"
            else:
                return f"{v*1e6:.2f} µV"
        
        return {
            "supply_voltage": Vsupply,
            "total_resistance_ohm": round(R_total, 2),
            "total_resistance_kohm": round(R_total / 1000, 2),
            "total_current": {
                "amperes": round(I_total, 6),
                "milliamperes": round(I_total * 1000, 2),
                "microamperes": round(I_total * 1e6, 2)
            },
            "voltage_drops": voltage_drops,
            "power_dissipation": power_dissipation,
            "total_power_w": round(Vsupply * I_total, 4),
            "total_power_mw": round(Vsupply * I_total * 1000, 2),
            "kvl_check": {
                "sum_voltage_drops_v": round(sum_Vdrops, 2),
                "supply_voltage_v": Vsupply,
                "difference": round(abs(sum_Vdrops - Vsupply), 4),
                "verified": abs(sum_Vdrops - Vsupply) < 0.01
            }
        }


    def kvl_with_load(self, Vsupply: float, R_load: float, resistors: list, load_position: int = -1):
        """
        Calculate KVL for a series circuit with a specified load resistor.
        
        Args:
            Vsupply: Supply voltage (V)
            R_load: Load resistor value (Ohms)
            resistors: List of other resistors in Ohms [R1, R2, ...]
            load_position: Where to insert load (-1 = end, 0 = beginning, 1 = after R1, etc.)
        
        Returns:
            dict: Complete circuit analysis
        """
        # Insert load at specified position
        circuit_resistors = resistors.copy()
        if load_position == -1 or load_position >= len(circuit_resistors):
            circuit_resistors.append(R_load)
            load_index = len(circuit_resistors) - 1
        elif load_position == 0:
            circuit_resistors.insert(0, R_load)
            load_index = 0
        else:
            circuit_resistors.insert(load_position, R_load)
            load_index = load_position
        
        # Calculate using KVL
        result = self.kvl_series_circuit(Vsupply, circuit_resistors)
        
        # Add load-specific info
        load_voltage = result["voltage_drops"][load_index]["voltage_v"]
        result["load_info"] = {
            "load_resistance_ohm": R_load,
            "load_resistance_kohm": round(R_load / 1000, 2),
            "load_position": load_index + 1,
            "load_voltage_v": round(load_voltage, 2),
            "load_voltage_percent": round((load_voltage / Vsupply) * 100, 1),
            "load_power_mw": round((load_voltage ** 2 / R_load) * 1000, 2)
        }
        
        return result


    def kvl_parallel_branch(self, Vsupply: float, branch_resistors: list):
        """
        Calculate parallel branch currents using Kirchhoff's Current Law (KCL).
        
        Args:
            Vsupply: Supply voltage (V)
            branch_resistors: List of resistor values in Ohms for each parallel branch
        
        Returns:
            dict: Branch currents, total current, power
        """
        # Calculate total parallel resistance
        R_parallel = 0
        for R in branch_resistors:
            R_parallel += 1 / R
        R_total = 1 / R_parallel
        
        # Total current
        I_total = Vsupply / R_total
        
        # Branch currents
        branch_currents = []
        for i, R in enumerate(branch_resistors, 1):
            I_branch = Vsupply / R
            P_branch = Vsupply * I_branch
            branch_currents.append({
                "branch": i,
                "resistance_ohm": R,
                "current_ma": round(I_branch * 1000, 2),
                "current_a": round(I_branch, 6),
                "power_mw": round(P_branch * 1000, 2)
            })
        
        # KCL check: Sum of branch currents = Total current
        sum_branch_currents = sum([c["current_a"] for c in branch_currents])
        
        return {
            "supply_voltage": Vsupply,
            "total_resistance_ohm": round(R_total, 2),
            "total_current_ma": round(I_total * 1000, 2),
            "branch_currents": branch_currents,
            "kcl_check": {
                "sum_branch_currents_a": round(sum_branch_currents, 4),
                "total_current_a": round(I_total, 4),
                "verified": abs(sum_branch_currents - I_total) < 0.001
            }
        }


    def voltage_divider_load(self, Vcc: float, R1: float, R2: float, R_load: float = None):
        """
        Calculate voltage divider with optional load.
        
        Without load: Vout = Vcc × (R2 / (R1 + R2))
        With load: R2_eff = (R2 × R_load) / (R2 + R_load)
        
        Args:
            Vcc: Input voltage (V)
            R1: Top resistor (Ω)
            R2: Bottom resistor (Ω)
            R_load: Load resistor (Ω), default = None (no load)
        
        Returns:
            dict: Output voltage, currents, power
        """
        if R_load is None or R_load == 0:
            Vout = Vcc * (R2 / (R1 + R2))
            I_R1 = Vcc / (R1 + R2)
            I_R2 = I_R1
            I_load = 0
            effective_R2 = R2
        else:
            effective_R2 = (R2 * R_load) / (R2 + R_load)
            Vout = Vcc * (effective_R2 / (R1 + effective_R2))
            I_R1 = Vcc / (R1 + effective_R2)
            I_R2 = Vout / R2
            I_load = Vout / R_load
        
        P_R1 = I_R1 ** 2 * R1
        P_R2 = I_R2 ** 2 * R2
        P_load = I_load ** 2 * R_load if R_load else 0
        
        return {
            "input_voltage": Vcc,
            "output_voltage": round(Vout, 2),
            "division_ratio": round(Vout / Vcc, 3),
            "currents": {
                "I_R1_mA": round(I_R1 * 1000, 2),
                "I_R2_mA": round(I_R2 * 1000, 2),
                "I_load_mA": round(I_load * 1000, 2) if R_load else 0
            },
            "power_mW": {
                "R1": round(P_R1 * 1000, 2),
                "R2": round(P_R2 * 1000, 2),
                "load": round(P_load * 1000, 2) if R_load else 0
            },
            "effective_resistance": {
                "R2_effective_ohm": round(effective_R2, 0),
                "R2_effective_kohm": round(effective_R2 / 1000, 2)
            } if R_load else None
        }
    
    # ================================================================
    # UNIFIED RESISTOR NETWORK (Series OR Parallel)
    # ================================================================

    def resistor_network(self, Vcc: float, resistors: list, config: str = "series", node_names: list = None):
        """
        Calculate voltages, currents, and power for series or parallel networks.
        
        Args:
            Vcc: Supply voltage (V)
            resistors: List of resistor values in Ohms [R1, R2, R3, ...]
            config: "series" or "parallel"
            node_names: Optional names for outputs
        
        Returns:
            dict: Voltages, currents, power for each resistor
        """
        
        if config.lower() == "series":
            # ============================================================
            # SERIES CONFIGURATION (KVL)
            # ============================================================
            R_total = sum(resistors)
            I_total = Vcc / R_total
            
            results = []
            cumulative_R = 0
            
            for i, R in enumerate(resistors, 1):
                cumulative_R += R
                V_node = Vcc - (I_total * cumulative_R)
                V_drop = I_total * R
                P_mW = V_drop * I_total * 1000
                
                name = node_names[i-1] if node_names and i-1 < len(node_names) else f"R{i}"
                
                results.append({
                    "resistor": name,
                    "resistance_ohm": R,
                    "resistance_kohm": round(R / 1000, 2),
                    "voltage_drop_v": round(V_drop, 2),
                    "current_a": round(I_total, 4),
                    "current_ma": round(I_total * 1000, 2),
                    "power_mw": round(P_mW, 2),
                    "node_voltage_v": round(V_node, 2) if i < len(resistors) else 0
                })
            
            return {
                "configuration": "SERIES",
                "supply_voltage_v": Vcc,
                "total_resistance_ohm": round(R_total, 2),
                "total_current_ma": round(I_total * 1000, 2),
                "total_power_mw": round(Vcc * I_total * 1000, 2),
                "resistors": results,
                "kvl_check": f"{Vcc}V = " + " + ".join([f"{r['voltage_drop_v']}V" for r in results]) + f" = {sum([r['voltage_drop_v'] for r in results])}V"
            }
        
        elif config.lower() == "parallel":
            # ============================================================
            # PARALLEL CONFIGURATION (KCL)
            # ============================================================
            # Calculate total parallel resistance
            R_parallel_sum = 0
            for R in resistors:
                R_parallel_sum += 1 / R
            R_total = 1 / R_parallel_sum
            
            I_total = Vcc / R_total
            
            results = []
            
            for i, R in enumerate(resistors, 1):
                I_branch = Vcc / R
                P_mW = Vcc * I_branch * 1000
                
                name = node_names[i-1] if node_names and i-1 < len(node_names) else f"R{i}"
                
                results.append({
                    "resistor": name,
                    "resistance_ohm": R,
                    "resistance_kohm": round(R / 1000, 2),
                    "voltage_v": round(Vcc, 2),
                    "current_a": round(I_branch, 4),
                    "current_ma": round(I_branch * 1000, 2),
                    "current_percent": round((I_branch / I_total) * 100, 1) if I_total > 0 else 0,
                    "power_mw": round(P_mW, 2)
                })
            
            return {
                "configuration": "PARALLEL",
                "supply_voltage_v": Vcc,
                "total_resistance_ohm": round(R_total, 2),
                "total_current_ma": round(I_total * 1000, 2),
                "total_power_mw": round(Vcc * I_total * 1000, 2),
                "resistors": results,
                "kcl_check": f"{round(I_total*1000,2)}mA = " + " + ".join([f"{r['current_ma']}mA" for r in results]) + f" = {sum([r['current_ma'] for r in results])}mA"
            }
        
        else:
            raise ValueError("config must be 'series' or 'parallel'")
        
    # ================================================================
    # VPEAK & CAPACITOR RATING CALCULATOR (with auto unit formatting)
    # ================================================================

    def vpeak_and_capacitor_rating(self, vrms: float = None, vdc: float = None, 
                                    safety_margin: float = 1.3, 
                                    return_all_units: bool = True):
        """
        Calculate Vpeak from AC (Vrms) or DC voltage, then recommend capacitor voltage rating.
        
        Args:
            vrms: AC voltage (RMS) — use for transformer or mains
            vdc: DC voltage — use for after rectifier or battery
            safety_margin: Multiplier for cap rating (default 1.3 = 30%)
            return_all_units: If True, returns Vpeak in V, mV, kV
        
        Returns:
            dict: Vpeak, recommended capacitor rating, auto-formatted units
        """
        import math
        
        # ============================================================
        # Step 1: Calculate Vpeak
        # ============================================================
        if vrms is not None:
            # AC input
            vpeak = vrms * math.sqrt(2)
            source_type = "AC (RMS)"
            source_value = vrms
            formula = f"Vpeak = {vrms}V × √2 = {vpeak:.1f}V"
        elif vdc is not None:
            # DC input
            vpeak = vdc
            source_type = "DC"
            source_value = vdc
            formula = f"Vpeak = {vdc}V (DC)"
        else:
            raise ValueError("Either vrms or vdc must be provided")
        
        # ============================================================
        # Step 2: Calculate minimum capacitor voltage rating
        # ============================================================
        vcap_min = vpeak * safety_margin
        
        # Standard capacitor voltage ratings (common values)
        std_ratings = [6.3, 10, 16, 25, 35, 50, 63, 80, 100, 
                    160, 200, 250, 350, 400, 450, 500, 630]
        
        # Find the next higher standard rating
        recommended_rating = None
        for rating in std_ratings:
            if rating >= vcap_min:
                recommended_rating = rating
                break
        
        if recommended_rating is None:
            recommended_rating = 1000  # Fallback for very high voltage
        
        # ============================================================
        # Step 3: Format Vpeak with auto unit (V, mV, kV)
        # ============================================================
        def format_voltage(v):
            if v >= 1000:
                return round(v / 1000, 2), "kV"
            elif v >= 1:
                return round(v, 1), "V"
            elif v >= 0.001:
                return round(v * 1000, 1), "mV"
            else:
                return round(v * 1_000_000, 1), "µV"
        
        vpeak_val, vpeak_unit = format_voltage(vpeak)
        vcap_val, vcap_unit = format_voltage(vcap_min)
        
        # ============================================================
        # Step 4: Format safety margin as percentage
        # ============================================================
        margin_percent = (safety_margin - 1) * 100
        
        # ============================================================
        # Step 5: Build result
        # ============================================================
        result = {
            "input": {
                "type": source_type,
                "value_v": source_value,
                "vrms_v": vrms if vrms is not None else None,
                "vdc_v": vdc if vdc is not None else None
            },
            "vpeak": {
                "value": vpeak_val,
                "unit": vpeak_unit,
                "raw_v": round(vpeak, 2),
                "formula": formula
            },
            "capacitor_rating": {
                "minimum_v": {
                    "value": vcap_val,
                    "unit": vcap_unit,
                    "raw_v": round(vcap_min, 1)
                },
                "safety_margin": f"{margin_percent:.0f}%",
                "recommended_rating_v": recommended_rating,
                "standard_ratings_available_v": std_ratings
            },
            "warning": f"Use capacitor rated ≥ {recommended_rating}V (never below {round(vpeak,1)}V)"
        }
        
        # ============================================================
        # Step 6: Add all units if requested
        # ============================================================
        if return_all_units:
            result["vpeak_all_units"] = {
                "v": round(vpeak, 2),
                "mv": round(vpeak * 1000, 1),
                "kv": round(vpeak / 1000, 3),
                "uv": round(vpeak * 1_000_000, 0)
            }
        
        return result


    # ================================================================
    # HELPER: Format capacitance with auto unit (F, mF, µF, nF, pF)
    # ================================================================

    def format_capacitance(self, farads: float):
        """
        Auto-format capacitance to appropriate unit.
        
        Rules:
            ≥ 1F      → Farads (F)
            ≥ 0.001F  → millifarads (mF)
            ≥ 1e-6F   → microfarads (µF)
            ≥ 1e-9F   → nanofarads (nF)
            < 1e-9F   → picofarads (pF)
        """
        if farads >= 1:
            return round(farads, 2), "F"
        elif farads >= 1e-3:
            return round(farads * 1000, 2), "mF"
        elif farads >= 1e-6:
            return round(farads * 1_000_000, 2), "µF"
        elif farads >= 1e-9:
            return round(farads * 1_000_000_000, 2), "nF"
        else:
            return round(farads * 1_000_000_000_000, 2), "pF"


    def format_resistance(self, ohms: float):
        """
        Auto-format resistance to appropriate unit.
        
        Rules:
            ≥ 1e6Ω  → MΩ
            ≥ 1000Ω → kΩ
            < 1000Ω → Ω
        """
        if ohms >= 1_000_000:
            return round(ohms / 1_000_000, 2), "MΩ"
        elif ohms >= 1000:
            return round(ohms / 1000, 2), "kΩ"
        else:
            return round(ohms, 1), "Ω"


    # ================================================================
    # COMPLETE POWER SUPPLY DESIGN FUNCTION
    # ================================================================

    def power_supply_capacitor(self, vrms: float = None, vdc: float = None,
                                load_ma: float = None, ripple_mv: float = None,
                                safety_margin: float = 1.3):
        """
        Complete power supply capacitor calculator.
        
        Calculates:
            - Vpeak from AC or DC
            - Minimum capacitor voltage rating
            - Required capacitance for desired ripple (if load provided)
        
        Args:
            vrms: AC input voltage (V)
            vdc: DC input voltage (V)
            load_ma: Load current in mA (for ripple calculation)
            ripple_mv: Desired ripple voltage in mV (for capacitance calculation)
            safety_margin: Voltage safety margin (default 1.3)
        
        Returns:
            dict: Complete power supply capacitor specifications
        """
        import math
        
        # Step 1: Get Vpeak and capacitor voltage rating
        vpeak_result = self.vpeak_and_capacitor_rating(
            vrms=vrms, vdc=vdc, safety_margin=safety_margin, return_all_units=False
        )
        
        result = {
            "voltage": vpeak_result,
            "capacitor_recommendations": {
                "voltage_rating_v": vpeak_result["capacitor_rating"]["recommended_rating_v"]
            }
        }
        
        # Step 2: Calculate required capacitance for ripple (if load provided)
        if load_ma is not None and ripple_mv is not None:
            I_load = load_ma / 1000
            ripple_v = ripple_mv / 1000
            frequency = 100  # Full-wave rectifier at 50Hz mains = 100Hz ripple
            
            C_farads = I_load / (frequency * ripple_v)
            C_val, C_unit = self.format_capacitance(C_farads)
            
            result["capacitor_recommendations"]["ripple_calculation"] = {
                "load_ma": load_ma,
                "target_ripple_mv": ripple_mv,
                "calculated_capacitance": {
                    "value": C_val,
                    "unit": C_unit,
                    "farads": round(C_farads, 8)
                },
                "formula": f"C = I_load / (f × Vripple) = {I_load}A / ({frequency}Hz × {ripple_v}V) = {C_val} {C_unit}"
            }
            
            # Recommend standard capacitor value
            std_caps_uf = [1, 2.2, 4.7, 10, 22, 47, 100, 220, 330, 470, 680, 
                        1000, 2200, 3300, 4700, 6800, 10000]
            C_uf = C_farads * 1_000_000
            recommended_uf = min(std_caps_uf, key=lambda x: abs(x - C_uf))
            result["capacitor_recommendations"]["recommended_capacitance_uf"] = recommended_uf
        
        return result
    
    # ================================================================
    # DIODE RECTIFIERS (Half-Wave, Full-Wave Bridge)
    # ================================================================

    def half_wave_rectifier(self, vrms: float, frequency: float = 50, 
                            load_ma: float = None, ripple_mv: float = None,
                            safety_margin: float = 1.3):
        """
        Half-wave rectifier calculator.
        
        Formula:
            Vpeak = Vrms × √2
            Vdc = Vpeak / π
            Ripple frequency = input frequency
            Vripple = I_load / (f_ripple × C)
        
        Args:
            vrms: AC input voltage (V RMS)
            frequency: AC line frequency (Hz, default 50)
            load_ma: Load current in mA (for ripple calculation)
            ripple_mv: Desired ripple voltage in mV (for capacitance calculation)
            safety_margin: Capacitor voltage safety margin (default 1.3)
        
        Returns:
            dict: Vpeak, Vdc, capacitor voltage rating, required capacitance
        """
        import math
        
        # Calculate peak voltage
        vpeak = vrms * math.sqrt(2)
        vdc_no_load = vpeak / math.pi
        ripple_freq = frequency  # Half-wave ripple frequency = line frequency
        
        # Get capacitor voltage rating
        cap_rating = self.vpeak_and_capacitor_rating(vrms=vrms, safety_margin=safety_margin)
        
        result = {
            "rectifier_type": "HALF-WAVE",
            "input": {
                "vrms_v": vrms,
                "frequency_hz": frequency,
                "vpeak_v": round(vpeak, 1)
            },
            "output": {
                "vdc_no_load_v": round(vdc_no_load, 1),
                "ripple_frequency_hz": ripple_freq
            },
            "capacitor_rating": {
                "minimum_voltage_v": cap_rating["capacitor_rating"]["minimum_v"]["raw_v"],
                "recommended_voltage_v": cap_rating["capacitor_rating"]["recommended_rating_v"],
                "safety_margin": cap_rating["capacitor_rating"]["safety_margin"]
            },
            "formulas": {
                "vpeak": f"Vpeak = {vrms} × √2 = {round(vpeak,1)}V",
                "vdc": f"Vdc = Vpeak/π = {round(vpeak,1)}/3.14 = {round(vdc_no_load,1)}V"
            }
        }
        
        # Calculate required capacitance for ripple
        if load_ma is not None and ripple_mv is not None:
            I_load = load_ma / 1000
            ripple_v = ripple_mv / 1000
            C_farads = I_load / (ripple_freq * ripple_v)
            
            # Format capacitance using existing method
            C_val, C_unit = self.format_capacitance(C_farads)
            
            result["ripple_calculation"] = {
                "load_ma": load_ma,
                "target_ripple_mv": ripple_mv,
                "required_capacitance": {
                    "value": C_val,
                    "unit": C_unit,
                    "farads": round(C_farads, 8)
                },
                "formula": f"C = I_load / (f × Vripple) = {I_load}A / ({ripple_freq}Hz × {ripple_v}V) = {C_val} {C_unit}"
            }
            
            # Recommend standard capacitor value
            C_uf = C_farads * 1_000_000
            std_caps_uf = [1, 2.2, 4.7, 10, 22, 47, 100, 220, 330, 470, 680, 
                        1000, 2200, 3300, 4700, 6800, 10000]
            recommended_uf = min(std_caps_uf, key=lambda x: abs(x - C_uf))
            result["ripple_calculation"]["recommended_capacitance_uf"] = recommended_uf
        
        return result


    def full_wave_rectifier(self, vrms: float, frequency: float = 50,
                            load_ma: float = None, ripple_mv: float = None,
                            safety_margin: float = 1.3):
        """
        Full-wave bridge rectifier calculator.
        
        Formula:
            Vpeak = Vrms × √2
            Vdc = 2 × Vpeak / π
            Ripple frequency = 2 × input frequency
            Vripple = I_load / (f_ripple × C)
            Diode drop = 2 × 0.7V = 1.4V
        
        Args:
            vrms: AC input voltage (V RMS)
            frequency: AC line frequency (Hz, default 50)
            load_ma: Load current in mA (for ripple calculation)
            ripple_mv: Desired ripple voltage in mV (for capacitance calculation)
            safety_margin: Capacitor voltage safety margin (default 1.3)
        
        Returns:
            dict: Vpeak, Vdc, capacitor voltage rating, required capacitance
        """
        import math
        
        # Calculate peak voltage
        vpeak = vrms * math.sqrt(2)
        diode_drop = 1.4  # 2 × 0.7V
        vdc_no_load = (2 * vpeak) / math.pi
        vdc_with_diodes = vdc_no_load - diode_drop
        ripple_freq = 2 * frequency  # Full-wave ripple frequency = 2× line frequency
        
        # Get capacitor voltage rating
        cap_rating = self.vpeak_and_capacitor_rating(vrms=vrms, safety_margin=safety_margin)
        
        result = {
            "rectifier_type": "FULL-WAVE BRIDGE",
            "input": {
                "vrms_v": vrms,
                "frequency_hz": frequency,
                "vpeak_v": round(vpeak, 1)
            },
            "output": {
                "vdc_no_load_v": round(vdc_no_load, 1),
                "vdc_with_diode_drop_v": round(vdc_with_diodes, 1),
                "diode_drop_v": diode_drop,
                "ripple_frequency_hz": ripple_freq
            },
            "capacitor_rating": {
                "minimum_voltage_v": cap_rating["capacitor_rating"]["minimum_v"]["raw_v"],
                "recommended_voltage_v": cap_rating["capacitor_rating"]["recommended_rating_v"],
                "safety_margin": cap_rating["capacitor_rating"]["safety_margin"]
            },
            "formulas": {
                "vpeak": f"Vpeak = {vrms} × √2 = {round(vpeak,1)}V",
                "vdc": f"Vdc = 2×Vpeak/π = 2×{round(vpeak,1)}/3.14 = {round(vdc_no_load,1)}V",
                "vdc_actual": f"Vdc_actual = Vdc - 1.4V = {round(vdc_with_diodes,1)}V"
            }
        }
        
        # Calculate required capacitance for ripple
        if load_ma is not None and ripple_mv is not None:
            I_load = load_ma / 1000
            ripple_v = ripple_mv / 1000
            C_farads = I_load / (ripple_freq * ripple_v)
            
            # Format capacitance using existing method
            C_val, C_unit = self.format_capacitance(C_farads)
            
            result["ripple_calculation"] = {
                "load_ma": load_ma,
                "target_ripple_mv": ripple_mv,
                "required_capacitance": {
                    "value": C_val,
                    "unit": C_unit,
                    "farads": round(C_farads, 8),
                    "uf": round(C_farads * 1_000_000, 2)
                },
                "formula": f"C = I_load / (f_ripple × Vripple) = {I_load}A / ({ripple_freq}Hz × {ripple_v}V) = {C_val} {C_unit}"
            }
            
            # Recommend standard capacitor value
            C_uf = C_farads * 1_000_000
            std_caps_uf = [1, 2.2, 4.7, 10, 22, 47, 100, 220, 330, 470, 680, 
                        1000, 2200, 3300, 4700, 6800, 10000]
            recommended_uf = min(std_caps_uf, key=lambda x: abs(x - C_uf))
            result["ripple_calculation"]["recommended_capacitance_uf"] = recommended_uf
            result["ripple_calculation"]["recommended_capacitance"] = self.format_capacitance(recommended_uf / 1_000_000)
        
        return result


    def diode_selection(self, vrms: float, load_ma: float = None, safety_margin: float = 1.5):
        """
        Select appropriate diode for rectifier.
        
        Args:
            vrms: AC input voltage (V RMS)
            load_ma: Load current in mA
            safety_margin: Voltage safety margin (default 1.5 = 50%)
        
        Returns:
            dict: Recommended diode type and ratings
        """
        vpeak = vrms * math.sqrt(2)
        min_piv = vpeak * safety_margin  # Peak Inverse Voltage requirement
        
        # Common diode ratings
        diodes = [
            {"name": "1N4001", "piv_v": 50, "current_a": 1, "use": "Low voltage DC"},
            {"name": "1N4002", "piv_v": 100, "current_a": 1, "use": "12-24V AC"},
            {"name": "1N4003", "piv_v": 200, "current_a": 1, "use": "24-48V AC"},
            {"name": "1N4004", "piv_v": 400, "current_a": 1, "use": "120V AC"},
            {"name": "1N4005", "piv_v": 600, "current_a": 1, "use": "220V AC (marginal)"},
            {"name": "1N4007", "piv_v": 1000, "current_a": 1, "use": "220V AC, 240V AC (recommended)"},
            {"name": "1N5408", "piv_v": 1000, "current_a": 3, "use": "High current (3A)"},
            {"name": "10A10", "piv_v": 1000, "current_a": 10, "use": "Very high current (10A)"}
        ]
        
        # Find suitable diode
        suitable = []
        for d in diodes:
            if d["piv_v"] >= min_piv:
                if load_ma:
                    if d["current_a"] * 1000 >= load_ma * 1.5:  # 50% current margin
                        suitable.append(d)
                else:
                    suitable.append(d)
        
        # Recommended diode
        if suitable:
            recommended = suitable[0]
            # For 220V AC, always recommend 1N4007 or higher
            if vrms >= 200:
                recommended = diodes[5]  # 1N4007
                if load_ma and load_ma > 1000:
                    recommended = diodes[7]  # 10A10
        else:
            recommended = {"name": "1N4007", "piv_v": 1000, "current_a": 1, "use": "Safe choice for most applications"}
        
        return {
            "input": {
                "vrms_v": vrms,
                "vpeak_v": round(vpeak, 1),
                "min_piv_v": round(min_piv, 0),
                "load_ma": load_ma
            },
            "recommended_diode": recommended,
            "alternative_diodes": suitable[1:3] if len(suitable) > 1 else [],
            "warning": f"Use diode with PIV ≥ {round(min_piv,0)}V and current ≥ {round((load_ma or 100)*1.5/1000,1)}A" if load_ma else f"Use diode with PIV ≥ {round(min_piv,0)}V"
        }


    def power_supply_design(self, vrms: float, load_ma: float, target_vdc: float = None,
                            ripple_mv: float = 100, frequency: float = 50,
                            rectifier_type: str = "full"):
        """
        Complete power supply design calculator.
        
        Calculates:
            - Transformer secondary voltage needed
            - Rectifier type selection
            - Filter capacitor value
            - Diode selection
            - Output voltage
        
        Args:
            vrms: AC input voltage (V RMS)
            load_ma: Load current in mA
            target_vdc: Desired DC output voltage (optional)
            ripple_mv: Desired ripple voltage in mV (default 100mV)
            frequency: AC line frequency (default 50Hz)
            rectifier_type: "half" or "full" (default "full")
        
        Returns:
            dict: Complete power supply design
        """
        import math
        
        if rectifier_type.lower() == "half":
            result = self.half_wave_rectifier(vrms=vrms, frequency=frequency, 
                                            load_ma=load_ma, ripple_mv=ripple_mv)
            vdc = result["output"]["vdc_no_load_v"]
        else:
            result = self.full_wave_rectifier(vrms=vrms, frequency=frequency,
                                            load_ma=load_ma, ripple_mv=ripple_mv)
            vdc = result["output"]["vdc_with_diode_drop_v"]
        
        # Add diode selection
        diode_result = self.diode_selection(vrms=vrms, load_ma=load_ma)
        
        # Add transformer VA rating
        va_rating = (vrms * (load_ma / 1000)) * 1.2  # 20% margin
        
        result["diode_recommendation"] = diode_result
        result["transformer"] = {
            "secondary_voltage_v": vrms,
            "current_ma": load_ma,
            "va_rating": round(va_rating, 1),
            "recommendation": f"Use {round(va_rating,1)}VA or higher transformer"
        }
        
        if target_vdc:
            if vdc < target_vdc:
                result["warning"] = f"Output Vdc ({vdc}V) is lower than target ({target_vdc}V). Increase transformer secondary voltage."
            elif vdc > target_vdc * 1.2:
                result["warning"] = f"Output Vdc ({vdc}V) is higher than target ({target_vdc}V). Consider using voltage regulator."
            else:
                result["success"] = f"Output Vdc ({vdc}V) meets target ({target_vdc}V)"
        
        return result
    


    # ================================================================
    # CAPACITOR FILTER CALCULATOR
    # ================================================================

    def capacitor_filter_calculator(self, load_ma: float, ripple_mv: float = 500,
                                    frequency_hz: float = 50, rectifier_type: str = "full",
                                    voltage_v: float = None, safety_margin: float = 1.3):
        """
        Calculate filter capacitor for power supply.
        
        Formulas:
            Full-wave: C = I_load / (2 × f × Vripple)
            Half-wave: C = I_load / (f × Vripple)
        
        Args:
            load_ma: Load current in mA
            ripple_mv: Desired ripple voltage in mV (default 500mV = 0.5V)
            frequency_hz: AC line frequency (default 50Hz for Pakistan)
            rectifier_type: "full" or "half"
            voltage_v: Output voltage (for capacitor voltage rating)
            safety_margin: Capacitor voltage safety margin (default 1.3)
        
        Returns:
            dict: Required capacitance, recommended standard value, voltage rating
        """
        import math
        
        # Convert to base units
        I_load = load_ma / 1000
        ripple_v = ripple_mv / 1000
        
        # Calculate required capacitance
        if rectifier_type.lower() == "full":
            ripple_freq = 2 * frequency_hz
            C_farads = I_load / (ripple_freq * ripple_v)
            formula = f"C = I_load / (2 × f × Vripple) = {I_load}A / (2 × {frequency_hz}Hz × {ripple_v}V)"
        elif rectifier_type.lower() == "half":
            ripple_freq = frequency_hz
            C_farads = I_load / (ripple_freq * ripple_v)
            formula = f"C = I_load / (f × Vripple) = {I_load}A / ({frequency_hz}Hz × {ripple_v}V)"
        else:
            raise ValueError("rectifier_type must be 'full' or 'half'")
        
        # Convert to µF
        C_uf = C_farads * 1_000_000
        
        # Standard capacitor values (E6/E12 series)
        std_caps_uf = [1, 2.2, 4.7, 10, 22, 33, 47, 68, 100, 150, 220, 330, 470, 
                    680, 1000, 1500, 2200, 3300, 4700, 6800, 10000, 15000, 22000]
        
        # Find recommended standard value (round UP for safety)
        recommended_uf = None
        for cap in std_caps_uf:
            if cap >= C_uf:
                recommended_uf = cap
                break
        
        if recommended_uf is None:
            recommended_uf = round(C_uf, -3)  # Round to nearest thousand
        
        # Calculate actual ripple with recommended capacitor
        C_actual_f = recommended_uf / 1_000_000
        actual_ripple_v = I_load / (ripple_freq * C_actual_f)
        actual_ripple_mv = actual_ripple_v * 1000
        
        # Calculate voltage rating
        voltage_rating = None
        if voltage_v:
            min_rating = voltage_v * safety_margin
            std_voltages = [6.3, 10, 16, 25, 35, 50, 63, 80, 100, 160, 200, 250, 350, 400, 450, 500]
            recommended_voltage = None
            for v in std_voltages:
                if v >= min_rating:
                    recommended_voltage = v
                    break
            if recommended_voltage is None:
                recommended_voltage = 500
            
            voltage_rating = {
                "minimum_v": round(min_rating, 1),
                "recommended_v": recommended_voltage
            }
        
        # Quality assessment
        if actual_ripple_mv <= ripple_mv * 1.1:
            quality = "Excellent (meets or exceeds requirement)"
        elif actual_ripple_mv <= ripple_mv * 1.5:
            quality = "Good (slightly higher ripple than target)"
        else:
            quality = "Fair (consider larger capacitor)"
        
        # Format capacitance for output
        cap_val, cap_unit = self.format_capacitance(C_farads)
        
        return {
            "input": {
                "load_ma": load_ma,
                "target_ripple_mv": ripple_mv,
                "frequency_hz": frequency_hz,
                "rectifier_type": rectifier_type.upper(),
                "output_voltage_v": voltage_v
            },
            "calculated": {
                "required_capacitance": {
                    "value": cap_val,
                    "unit": cap_unit,
                    "uf": round(C_uf, 0),
                    "farads": round(C_farads, 6)
                },
                "formula": formula,
                "ripple_frequency_hz": ripple_freq
            },
            "recommendations": {
                "capacitor_uf": recommended_uf,
                "actual_ripple_mv": round(actual_ripple_mv, 1),
                "quality": quality
            },
            "voltage_rating": voltage_rating,
            "notes": {
                "full_wave_advantage": "Full-wave has 100Hz ripple (easier to filter) vs half-wave 50Hz",
                "rule_of_thumb": f"For {load_ma}mA load, use {recommended_uf}µF for {actual_ripple_mv:.0f}mV ripple"
            }
        }


    def ripple_calculator(self, load_ma: float, capacitor_uf: float,
                        frequency_hz: float = 50, rectifier_type: str = "full"):
        """
        Calculate ripple voltage for given load and capacitor.
        
        Args:
            load_ma: Load current in mA
            capacitor_uf: Filter capacitor in µF
            frequency_hz: AC line frequency (default 50Hz)
            rectifier_type: "full" or "half"
        
        Returns:
            dict: Ripple voltage and quality assessment
        """
        I_load = load_ma / 1000
        C_f = capacitor_uf / 1_000_000
        
        if rectifier_type.lower() == "full":
            ripple_freq = 2 * frequency_hz
            ripple_v = I_load / (ripple_freq * C_f)
            formula = f"Vripple = I_load / (2 × f × C) = {I_load}A / (2 × {frequency_hz}Hz × {C_f}F)"
        else:
            ripple_freq = frequency_hz
            ripple_v = I_load / (ripple_freq * C_f)
            formula = f"Vripple = I_load / (f × C) = {I_load}A / ({frequency_hz}Hz × {C_f}F)"
        
        ripple_mv = ripple_v * 1000
        
        # Quality assessment
        if ripple_mv < 10:
            quality = "Excellent (audio/precision grade)"
            use_case = "Audio amplifiers, precision analog, medical devices"
        elif ripple_mv < 50:
            quality = "Good (microcontroller/ADC grade)"
            use_case = "Arduino, ESP32, sensors, ADC readings"
        elif ripple_mv < 100:
            quality = "Fair (general purpose)"
            use_case = "LEDs, relays, digital logic"
        elif ripple_mv < 500:
            quality = "Acceptable (power supply)"
            use_case = "Motors, LEDs, battery chargers"
        else:
            quality = "Poor (needs larger capacitor)"
            use_case = "Only for very tolerant loads"
        
        return {
            "input": {
                "load_ma": load_ma,
                "capacitor_uf": capacitor_uf,
                "frequency_hz": frequency_hz,
                "rectifier_type": rectifier_type.upper()
            },
            "ripple": {
                "voltage_v": round(ripple_v, 3),
                "voltage_mv": round(ripple_mv, 1)
            },
            "quality": quality,
            "use_case": use_case,
            "formula": formula,
            "recommendation": f"To reduce ripple, use larger capacitor. For {ripple_mv:.0f}mV → need {round(capacitor_uf * (ripple_mv/100),0)}µF for 100mV ripple"
        }


    def standard_capacitor_values(self, min_uf: float = None, max_uf: float = None):
        """
        Return list of standard capacitor values.
        
        Args:
            min_uf: Minimum capacitance in µF
            max_uf: Maximum capacitance in µF
        
        Returns:
            dict: Standard values and recommendations
        """
        std_values = [1, 2.2, 4.7, 10, 22, 33, 47, 68, 100, 150, 220, 330, 470, 
                    680, 1000, 1500, 2200, 3300, 4700, 6800, 10000, 15000, 22000, 
                    33000, 47000, 68000, 100000]
        
        if min_uf is not None:
            std_values = [v for v in std_values if v >= min_uf]
        if max_uf is not None:
            std_values = [v for v in std_values if v <= max_uf]
        
        return {
            "standard_capacitors_uf": std_values,
            "note": "E6/E12 series - most common values",
            "voltage_ratings": [6.3, 10, 16, 25, 35, 50, 63, 80, 100, 160, 200, 250, 350, 400, 450]
    }

    def zener_regulator(self, vin: float, vz: float, i_load_ma: float = 0,
                        iz_min_ma: float = 5, zener_power_w: float = 1):
        """
        Calculate Zener diode regulator.
        
        Args:
            vin: Input voltage (V) — must be > Vz
            vz: Zener voltage (V) — e.g., 3.3, 5.1, 12
            i_load_ma: Load current in mA
            iz_min_ma: Minimum Zener current for regulation (mA)
            zener_power_w: Zener power rating (e.g., 0.5, 1, 5)
        
        Returns:
            dict: Resistor values, power, safety check
        """
        i_load = i_load_ma / 1000
        iz_min = iz_min_ma / 1000
        
        if vin <= vz:
            return {"error": f"Vin ({vin}V) must be greater than Vz ({vz}V)"}
        
        # Calculate series resistor
        i_total = iz_min + i_load
        R = (vin - vz) / i_total
        
        # Standard resistor values
        std_resistors = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, 
                        100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 
                        680, 820, 1000, 1200, 1500, 1800, 2200, 2700, 3300]
        R_std = min(std_resistors, key=lambda x: abs(x - R))
        
        # Calculate actual values with standard resistor
        i_total_actual = (vin - vz) / R_std
        iz_actual = i_total_actual - i_load
        iz_actual_ma = iz_actual * 1000
        
        # Power dissipation
        p_r = (vin - vz) ** 2 / R_std
        p_z = vz * iz_actual
        p_z_mw = p_z * 1000
        
        # Safety checks
        zener_safe = p_z <= zener_power_w * 0.8  # 80% derating
        resistor_safe = p_r <= 0.5  # 1/2W resistor typical
        
        # Determine Zener type
        if vz <= 5.6:
            zener_type = "Low voltage (good temperature stability)"
        elif vz <= 12:
            zener_type = "Medium voltage"
        else:
            zener_type = "High voltage (poor temperature stability)"
        
        return {
            "input": {
                "voltage_v": vin,
                "zener_voltage_v": vz,
                "load_ma": i_load_ma
            },
            "series_resistor": {
                "calculated_ohm": round(R, 0),
                "calculated_kohm": round(R / 1000, 2),
                "recommended_ohm": R_std,
                "recommended_kohm": round(R_std / 1000, 2),
                "power_w": round(p_r, 2),
                "power_mw": round(p_r * 1000, 0),
                "use_wattage": "1W" if p_r > 0.5 else "0.5W or 1/2W"
            },
            "zener_diode": {
                "voltage_v": vz,
                "current_ma": round(iz_actual_ma, 1),
                "power_mw": round(p_z_mw, 0),
                "power_rating_w": zener_power_w,
                "safe": zener_safe,
                "type": zener_type
            },
            "output": {
                "voltage_v": vz,
                "max_current_ma": round(((vin - vz) / R_std - iz_min) * 1000, 0),
                "min_current_ma": 0
            },
            "formulas": {
                "resistor": f"R = ({vin} - {vz}) / ({iz_min_ma}mA + {i_load_ma}mA) = {R_std}Ω",
                "zener_power": f"Pz = {vz}V × {round(iz_actual_ma,1)}mA = {round(p_z_mw,0)}mW"
            },
            "warning": f"Use {R_std}Ω {p_r*1000:.0f}mW resistor and {vz}V {zener_power_w}W Zener" if not zener_safe else None
        }
    


    # ================================================================
    # OPERATIONAL AMPLIFIERS (OP-AMPS)
    # ================================================================

    def opamp_inverting(self, Rf: float, Rin: float):
        """
        Inverting Amplifier Calculator.
        
        Formula: Av = -Rf / Rin
        
        Args:
            Rf: Feedback resistor (Ω)
            Rin: Input resistor (Ω)
        
        Returns:
            dict: Gain, output voltage for 1V input, resistor values
        """
        gain = -Rf / Rin
        gain_magnitude = abs(gain)
        
        return {
            "configuration": "Inverting Amplifier",
            "resistors": {
                "Rf_ohm": Rf,
                "Rf_kohm": round(Rf / 1000, 2),
                "Rin_ohm": Rin,
                "Rin_kohm": round(Rin / 1000, 2)
            },
            "gain": {
                "ratio": round(gain, 2),
                "magnitude": round(gain_magnitude, 2),
                "db": round(20 * math.log10(gain_magnitude), 1) if gain_magnitude > 0 else -999
            },
            "output_for_1v_input_v": round(gain, 2),
            "phase_shift": "180°",
            "formula": f"Av = -({Rf}/{Rin}) = {gain:.2f}"
        }


    def opamp_non_inverting(self, Rf: float, Rg: float):
        """
        Non-inverting Amplifier Calculator.
        
        Formula: Av = 1 + Rf/Rg
        
        Args:
            Rf: Feedback resistor (Ω)
            Rg: Gain resistor (Ω)
        
        Returns:
            dict: Gain, output voltage for 1V input
        """
        gain = 1 + (Rf / Rg)
        
        return {
            "configuration": "Non-Inverting Amplifier",
            "resistors": {
                "Rf_ohm": Rf,
                "Rf_kohm": round(Rf / 1000, 2),
                "Rg_ohm": Rg,
                "Rg_kohm": round(Rg / 1000, 2)
            },
            "gain": {
                "ratio": round(gain, 2),
                "db": round(20 * math.log10(gain), 1)
            },
            "output_for_1v_input_v": round(gain, 2),
            "phase_shift": "0°",
            "formula": f"Av = 1 + ({Rf}/{Rg}) = {gain:.2f}"
        }


    def opamp_buffer(self):
        """
        Voltage Follower (Buffer) Calculator.
        
        Formula: Av = 1
        """
        return {
            "configuration": "Voltage Follower (Buffer)",
            "gain": {
                "ratio": 1,
                "db": 0
            },
            "input_impedance": "Very high (MΩ)",
            "output_impedance": "Very low (Ω)",
            "phase_shift": "0°",
            "use_case": "Impedance matching, isolation, driving heavy loads",
            "formula": "Vout = Vin"
        }


    def opamp_summing(self, V_inputs: list, R_inputs: list, Rf: float):
        """
        Summing Amplifier Calculator (Inverting).
        
        Formula: Vout = -Rf × (V1/R1 + V2/R2 + V3/R3 + ...)
        
        Args:
            V_inputs: List of input voltages [V1, V2, V3, ...]
            R_inputs: List of input resistors [R1, R2, R3, ...] (Ω)
            Rf: Feedback resistor (Ω)
        
        Returns:
            dict: Output voltage, individual contributions
        """
        if len(V_inputs) != len(R_inputs):
            raise ValueError("V_inputs and R_inputs must have same length")
        
        total = 0
        contributions = []
        
        for i, (V, R) in enumerate(zip(V_inputs, R_inputs), 1):
            contribution = V / R
            total += contribution
            contributions.append({
                "input": i,
                "voltage_v": V,
                "resistor_ohm": R,
                "resistor_kohm": round(R / 1000, 2),
                "contribution": round(contribution, 6)
            })
        
        Vout = -Rf * total
        
        return {
            "configuration": "Summing Amplifier (Inverting)",
            "inputs": contributions,
            "Rf_ohm": Rf,
            "Rf_kohm": round(Rf / 1000, 2),
            "output_voltage_v": round(Vout, 3),
            "formula": f"Vout = -{Rf} × ({' + '.join([f'V{i}/R{i}' for i in range(1, len(V_inputs)+1)])}) = {Vout:.3f}V"
        }


    def opamp_differential(self, V1: float, V2: float, R1: float, R2: float, R3: float, R4: float):
        """
        Differential Amplifier Calculator.
        
        Formula: Vout = (R2/R1) × (V2 - V1)  (if R1=R3 and R2=R4)
        
        Args:
            V1: Input to inverting terminal (V)
            V2: Input to non-inverting terminal (V)
            R1: Resistor from V1 to inverting input (Ω)
            R2: Feedback resistor (Ω)
            R3: Resistor from V2 to non-inverting input (Ω)
            R4: Resistor from non-inverting input to GND (Ω)
        
        Returns:
            dict: Output voltage, common mode rejection
        """
        # For matched resistors: R1=R3, R2=R4
        if R1 == R3 and R2 == R4:
            gain = R2 / R1
            Vout = gain * (V2 - V1)
            matched = True
        else:
            # General formula
            Vout = (R2/R1) * (V2 * (R1/(R1+R2)) * ((R3+R4)/R3) - V1)
            gain = R2 / R1
            matched = False
        
        return {
            "configuration": "Differential Amplifier",
            "inputs": {
                "V1": V1,
                "V2": V2,
                "difference_v": round(V2 - V1, 3)
            },
            "resistors": {
                "R1_ohm": R1,
                "R2_ohm": R2,
                "R3_ohm": R3,
                "R4_ohm": R4
            },
            "gain": round(gain, 2),
            "output_voltage_v": round(Vout, 3),
            "matched_resistors": matched,
            "formula": f"Vout = {gain:.2f} × ({V2} - {V1}) = {Vout:.3f}V"
        }


    def opamp_integrator(self, R: float, C: float, Vin: float, time_s: float):
        """
        Integrator Amplifier Calculator.
        
        Formula: Vout = -1/(RC) × ∫Vin dt
        
        Args:
            R: Input resistor (Ω)
            C: Feedback capacitor (F)
            Vin: Input voltage (V) (constant)
            time_s: Time in seconds
        
        Returns:
            dict: Output voltage after time
        """
        RC = R * C
        Vout = - (Vin / RC) * time_s
        
        # Saturation limits (typical op-amp supply ±12V)
        if Vout > 12:
            Vout = 12
            saturated = True
        elif Vout < -12:
            Vout = -12
            saturated = True
        else:
            saturated = False
        
        return {
            "configuration": "Integrator",
            "components": {
                "R_ohm": R,
                "R_kohm": round(R / 1000, 2),
                "C_f": C,
                "C_uf": round(C * 1e6, 2),
                "RC_time_constant_s": round(RC, 6)
            },
            "input_voltage_v": Vin,
            "time_s": time_s,
            "output_voltage_v": round(Vout, 3),
            "saturated": saturated,
            "formula": f"Vout = -({Vin}/{RC}) × {time_s} = {Vout:.3f}V"
        }


    def opamp_differentiator(self, R: float, C: float, Vin_peak: float, frequency_hz: float):
        """
        Differentiator Amplifier Calculator.
        
        Formula: Vout = -RC × dVin/dt
        
        Args:
            R: Feedback resistor (Ω)
            C: Input capacitor (F)
            Vin_peak: Input voltage peak (V)
            frequency_hz: Input frequency (Hz)
        
        Returns:
            dict: Output voltage
        """
        RC = R * C
        omega = 2 * math.pi * frequency_hz
        Vout_peak = RC * omega * Vin_peak
        
        return {
            "configuration": "Differentiator",
            "components": {
                "R_ohm": R,
                "R_kohm": round(R / 1000, 2),
                "C_f": C,
                "C_nf": round(C * 1e9, 2),
                "RC_time_constant_s": round(RC, 6)
            },
            "input": {
                "voltage_peak_v": Vin_peak,
                "frequency_hz": frequency_hz
            },
            "output_voltage_peak_v": round(Vout_peak, 3),
            "formula": f"Vout = -{RC} × 2π×{frequency_hz} × {Vin_peak} = {Vout_peak:.3f}V"
        }


    def opamp_comparator(self, Vref: float, Vsense: float, Vcc: float = 12, Vee: float = 0):
        """
        Comparator (Schmitt Trigger without hysteresis).
        
        Args:
            Vref: Reference voltage (V)
            Vsense: Input voltage to compare (V)
            Vcc: Positive supply voltage (V)
            Vee: Negative supply voltage (V)
        
        Returns:
            dict: Output voltage and decision
        """
        if Vsense > Vref:
            Vout = Vcc
            decision = "HIGH"
            condition = "Input > Reference"
        elif Vsense < Vref:
            Vout = Vee
            decision = "LOW"
            condition = "Input < Reference"
        else:
            Vout = 0
            decision = "INDETERMINATE"
            condition = "Input = Reference"
        
        return {
            "configuration": "Comparator",
            "reference_voltage_v": Vref,
            "sense_voltage_v": Vsense,
            "output_voltage_v": round(Vout, 2),
            "output_state": decision,
            "condition": condition,
            "rule": "Output HIGH when Vsense > Vref, LOW when Vsense < Vref"
        }


    def opamp_schmitt_trigger(self, Vcc: float, R1: float, R2: float, Vin: float = None):
        """
        Schmitt Trigger (Comparator with Hysteresis).
        
        Formula: Vth_high = Vcc × (R2/(R1+R2)), Vth_low = 0 (for inverting)
        
        Args:
            Vcc: Supply voltage (V)
            R1: Resistor from output to non-inverting input (Ω)
            R2: Resistor from non-inverting input to GND (Ω)
            Vin: Input voltage to check (optional)
        
        Returns:
            dict: Thresholds and output state
        """
        threshold_ratio = R2 / (R1 + R2)
        Vth_high = Vcc * threshold_ratio
        Vth_low = 0
        
        hysteresis = Vth_high - Vth_low
        
        result = {
            "configuration": "Schmitt Trigger (Non-inverting)",
            "resistors": {
                "R1_ohm": R1,
                "R1_kohm": round(R1 / 1000, 2),
                "R2_ohm": R2,
                "R2_kohm": round(R2 / 1000, 2)
            },
            "thresholds": {
                "upper_v": round(Vth_high, 2),
                "lower_v": round(Vth_low, 2),
                "hysteresis_v": round(hysteresis, 2)
            },
            "formula": f"Vth = Vcc × (R2/(R1+R2)) = {Vcc} × ({R2}/{R1+R2}) = {Vth_high:.2f}V"
        }
        
        if Vin is not None:
            if Vin > Vth_high:
                output = "HIGH"
                state = "above upper threshold"
            elif Vin < Vth_low:
                output = "LOW"
                state = "below lower threshold"
            else:
                output = "UNCHANGED"
                state = "within hysteresis band"
            
            result["input_check"] = {
                "input_voltage_v": Vin,
                "output_state": output,
                "status": state
            }
        
        return result
    

    # ================================================================
    # AC CIRCUITS & IMPEDANCE
    # ================================================================

    def ac_capacitive_reactance(self, f_hz: float, C_f: float):
        """
        Calculate capacitive reactance.
        
        Formula: Xc = 1 / (2πfC)
        
        Args:
            f_hz: Frequency in Hz
            C_f: Capacitance in Farads
        
        Returns:
            dict: Xc in ohms
        """
        Xc = 1 / (2 * math.pi * f_hz * C_f)
        
        return {
            "frequency_hz": f_hz,
            "capacitance": {
                "f": C_f,
                "uf": round(C_f * 1e6, 2),
                "nf": round(C_f * 1e9, 2),
                "pf": round(C_f * 1e12, 1)
            },
            "reactance_ohm": round(Xc, 2),
            "reactance_kohm": round(Xc / 1000, 2),
            "formula": f"Xc = 1/(2π × {f_hz} × {C_f}) = {Xc:.2f}Ω"
        }


    def ac_inductive_reactance(self, f_hz: float, L_h: float):
        """
        Calculate inductive reactance.
        
        Formula: XL = 2πfL
        
        Args:
            f_hz: Frequency in Hz
            L_h: Inductance in Henries
        
        Returns:
            dict: XL in ohms
        """
        XL = 2 * math.pi * f_hz * L_h
        
        return {
            "frequency_hz": f_hz,
            "inductance": {
                "h": L_h,
                "mh": round(L_h * 1000, 2),
                "uh": round(L_h * 1e6, 2)
            },
            "reactance_ohm": round(XL, 2),
            "reactance_kohm": round(XL / 1000, 2),
            "formula": f"XL = 2π × {f_hz} × {L_h} = {XL:.2f}Ω"
        }


    def ac_series_rlc(self, R: float, L_h: float, C_f: float, f_hz: float):
        """
        Calculate series RLC impedance.
        
        Formula: Z = √(R² + (XL - XC)²)
        
        Args:
            R: Resistance (Ω)
            L_h: Inductance (H)
            C_f: Capacitance (F)
            f_hz: Frequency (Hz)
        
        Returns:
            dict: Impedance, reactances, phase angle
        """
        XL = 2 * math.pi * f_hz * L_h
        XC = 1 / (2 * math.pi * f_hz * C_f)
        X_net = XL - XC
        Z = math.sqrt(R**2 + X_net**2)
        phase_angle = math.atan2(X_net, R) * 180 / math.pi
        
        # Power factor
        power_factor = R / Z if Z > 0 else 0
        
        return {
            "input": {
                "resistance_ohm": R,
                "inductance_h": L_h,
                "inductance_mh": round(L_h * 1000, 2),
                "capacitance_f": C_f,
                "capacitance_uf": round(C_f * 1e6, 2),
                "frequency_hz": f_hz
            },
            "reactances": {
                "xl_ohm": round(XL, 2),
                "xc_ohm": round(XC, 2),
                "x_net_ohm": round(X_net, 2)
            },
            "impedance_ohm": round(Z, 2),
            "phase_angle_deg": round(phase_angle, 1),
            "power_factor": round(power_factor, 3),
            "formula": f"Z = √({R}² + ({XL:.1f} - {XC:.1f})²) = {Z:.2f}Ω"
        }


    def ac_parallel_rlc(self, R: float, L_h: float, C_f: float, f_hz: float):
        """
        Calculate parallel RLC impedance.
        
        Args:
            R: Resistance (Ω)
            L_h: Inductance (H)
            C_f: Capacitance (F)
            f_hz: Frequency (Hz)
        
        Returns:
            dict: Impedance, resonant frequency
        """
        # Resonant frequency
        f_res = 1 / (2 * math.pi * math.sqrt(L_h * C_f))
        
        # At resonance, XL = XC, impedance = R (for parallel)
        # Off resonance calculation is complex
        f_ratio = f_hz / f_res
        
        return {
            "components": {
                "resistance_ohm": R,
                "inductance_mh": round(L_h * 1000, 2),
                "capacitance_uf": round(C_f * 1e6, 2)
            },
            "resonant_frequency_hz": round(f_res, 2),
            "resonant_frequency": self._format_frequency(f_res),
            "impedance_at_resonance_ohm": R,
            "note": "At resonance, parallel RLC acts as pure resistance",
            "formula": f"f_res = 1/(2π√LC) = 1/(2π√({L_h}×{C_f})) = {f_res:.2f}Hz"
        }


    def ac_resonant_frequency(self, L_h: float, C_f: float):
        """
        Calculate RLC resonant frequency.
        
        Formula: f = 1 / (2π√(LC))
        
        Args:
            L_h: Inductance (H)
            C_f: Capacitance (F)
        
        Returns:
            dict: Resonant frequency
        """
        f_res = 1 / (2 * math.pi * math.sqrt(L_h * C_f))
        formatted = self._format_frequency(f_res)
        
        return {
            "inductance": {
                "h": L_h,
                "mh": round(L_h * 1000, 2),
                "uh": round(L_h * 1e6, 2)
            },
            "capacitance": {
                "f": C_f,
                "uf": round(C_f * 1e6, 2),
                "nf": round(C_f * 1e9, 2),
                "pf": round(C_f * 1e12, 1)
            },
            "resonant_frequency": {
                "value": formatted["value"],
                "unit": formatted["unit"],
                "hz": round(f_res, 2)
            },
            "formula": f"f = 1/(2π√({L_h}×{C_f})) = {f_res:.2f}Hz"
        }


    def ac_q_factor(self, R: float, L_h: float, C_f: float, f_hz: float = None):
        """
        Calculate quality factor (Q) for RLC circuit.
        
        Series: Q = (1/R) × √(L/C)
        Parallel: Q = R × √(C/L)
        
        Args:
            R: Resistance (Ω)
            L_h: Inductance (H)
            C_f: Capacitance (F)
            f_hz: Frequency (optional, for bandwidth)
        
        Returns:
            dict: Q factor and bandwidth
        """
        # Series RLC Q factor
        Q_series = (1 / R) * math.sqrt(L_h / C_f)
        
        # Parallel RLC Q factor
        Q_parallel = R * math.sqrt(C_f / L_h)
        
        result = {
            "q_factor_series": round(Q_series, 2),
            "q_factor_parallel": round(Q_parallel, 2),
            "bandwidth_series_hz": None,
            "bandwidth_parallel_hz": None
        }
        
        if f_hz:
            f_res = 1 / (2 * math.pi * math.sqrt(L_h * C_f))
            bw_series = f_res / Q_series if Q_series > 0 else 0
            bw_parallel = f_res / Q_parallel if Q_parallel > 0 else 0
            result["bandwidth_series_hz"] = round(bw_series, 2)
            result["bandwidth_parallel_hz"] = round(bw_parallel, 2)
            result["resonant_frequency_hz"] = round(f_res, 2)
            result["formula"] = f"Q = (1/R)√(L/C) = {Q_series:.2f}, BW = f0/Q = {f_res:.2f}/{Q_series:.2f} = {bw_series:.2f}Hz"
        
        return result
    
    # ================================================================
    # FILTERS
    # ================================================================

    def filter_rc_lowpass(self, R: float, C: float):
        """
        RC Low-pass filter cutoff frequency.
        
        Formula: fc = 1 / (2πRC)
        
        Args:
            R: Resistance (Ω)
            C: Capacitance (F)
        
        Returns:
            dict: Cutoff frequency
        """
        fc = 1 / (2 * math.pi * R * C)
        formatted = self._format_frequency(fc)
        
        return {
            "resistance_ohm": R,
            "resistance_kohm": round(R / 1000, 2),
            "capacitance_f": C,
            "capacitance_uf": round(C * 1e6, 2),
            "cutoff_frequency": {
                "value": formatted["value"],
                "unit": formatted["unit"],
                "hz": round(fc, 2)
            },
            "formula": f"fc = 1/(2πRC) = 1/(2π×{R}×{C}) = {fc:.2f}Hz"
        }


    def filter_rc_highpass(self, R: float, C: float):
        """
        RC High-pass filter cutoff frequency.
        
        Formula: fc = 1 / (2πRC)
        
        Args:
            R: Resistance (Ω)
            C: Capacitance (F)
        
        Returns:
            dict: Cutoff frequency
        """
        fc = 1 / (2 * math.pi * R * C)
        formatted = self._format_frequency(fc)
        
        return {
            "resistance_ohm": R,
            "resistance_kohm": round(R / 1000, 2),
            "capacitance_f": C,
            "capacitance_uf": round(C * 1e6, 2),
            "cutoff_frequency": {
                "value": formatted["value"],
                "unit": formatted["unit"],
                "hz": round(fc, 2)
            },
            "formula": f"fc = 1/(2πRC) = 1/(2π×{R}×{C}) = {fc:.2f}Hz"
        }


    def filter_lc(self, L_h: float, C_f: float, filter_type: str = "pi"):
        """
        LC filter calculator (Pi or T configuration).
        
        Args:
            L_h: Inductance (H)
            C_f: Capacitance (F)
            filter_type: "pi" (C-L-C) or "t" (L-C-L)
        
        Returns:
            dict: Cutoff frequency
        """
        fc = 1 / (2 * math.pi * math.sqrt(L_h * C_f))
        formatted = self._format_frequency(fc)
        
        return {
            "filter_type": filter_type.upper(),
            "inductance_mh": round(L_h * 1000, 2),
            "capacitance_uf": round(C_f * 1e6, 2),
            "cutoff_frequency": {
                "value": formatted["value"],
                "unit": formatted["unit"],
                "hz": round(fc, 2)
            },
            "formula": f"fc = 1/(2π√LC) = 1/(2π√({L_h}×{C_f})) = {fc:.2f}Hz"
        }


    def filter_active_lowpass(self, R: float, C: float, gain: float = 1):
        """
        Active low-pass filter (Sallen-Key).
        
        Formula: fc = 1 / (2πRC), Gain = 1 + Rf/Rg
        
        Args:
            R: Resistance (Ω) (both resistors equal for simple design)
            C: Capacitance (F) (both capacitors equal)
            gain: Desired gain (default 1)
        
        Returns:
            dict: Cutoff frequency and component values
        """
        fc = 1 / (2 * math.pi * R * C)
        formatted = self._format_frequency(fc)
        
        # For gain > 1, suggest feedback resistors
        if gain > 1:
            Rg = 1000  # 1kΩ
            Rf = Rg * (gain - 1)
        else:
            Rf = 0
            Rg = None
        
        return {
            "configuration": "Sallen-Key Low-Pass",
            "components": {
                "R_ohm": R,
                "R_kohm": round(R / 1000, 2),
                "C_f": C,
                "C_nf": round(C * 1e9, 2)
            },
            "cutoff_frequency": {
                "value": formatted["value"],
                "unit": formatted["unit"],
                "hz": round(fc, 2)
            },
            "gain": gain,
            "feedback_resistors": {
                "Rf_ohm": round(Rf, 0) if gain > 1 else None,
                "Rf_kohm": round(Rf / 1000, 2) if gain > 1 else None,
                "Rg_ohm": Rg,
                "Rg_kohm": round(Rg / 1000, 2) if Rg else None
            } if gain > 1 else None,
            "formula": f"fc = 1/(2πRC) = 1/(2π×{R}×{C}) = {fc:.2f}Hz"
        }


    def filter_bandpass(self, f_center_hz: float, Q: float = 10):
        """
        Band-pass filter calculator.
        
        Args:
            f_center_hz: Center frequency (Hz)
            Q: Quality factor (default 10)
        
        Returns:
            dict: Bandwidth and cutoff frequencies
        """
        bandwidth = f_center_hz / Q
        f_low = f_center_hz - (bandwidth / 2)
        f_high = f_center_hz + (bandwidth / 2)
        
        return {
            "center_frequency": {
                "hz": round(f_center_hz, 2),
                "khz": round(f_center_hz / 1000, 2),
                "mhz": round(f_center_hz / 1e6, 4)
            },
            "quality_factor_q": Q,
            "bandwidth_hz": round(bandwidth, 2),
            "cutoff_frequencies": {
                "lower_hz": round(f_low, 2),
                "upper_hz": round(f_high, 2)
            },
            "formula": f"BW = f0/Q = {f_center_hz}/{Q} = {bandwidth:.2f}Hz"
        }


    def filter_notch(self, f_notch_hz: float, Q: float = 10):
        """
        Notch (band-stop) filter calculator.
        
        Args:
            f_notch_hz: Notch frequency (Hz)
            Q: Quality factor (default 10)
        
        Returns:
            dict: Bandwidth and rejection band
        """
        bandwidth = f_notch_hz / Q
        f_low = f_notch_hz - (bandwidth / 2)
        f_high = f_notch_hz + (bandwidth / 2)
        
        return {
            "notch_frequency": {
                "hz": round(f_notch_hz, 2),
                "khz": round(f_notch_hz / 1000, 2),
                "mhz": round(f_notch_hz / 1e6, 4)
            },
            "quality_factor_q": Q,
            "rejection_bandwidth_hz": round(bandwidth, 2),
            "rejection_range": {
                "lower_hz": round(f_low, 2),
                "upper_hz": round(f_high, 2)
            },
            "formula": f"BW = f0/Q = {f_notch_hz}/{Q} = {bandwidth:.2f}Hz"
        }
    
    # ================================================================
    # RF & COMMUNICATION
    # ================================================================

    def rf_antenna_length(self, frequency_hz: float, wavelength_type: str = "quarter"):
        """
        Calculate antenna length.
        
        Formula: λ = c/f, length = λ × factor
        
        Args:
            frequency_hz: Frequency in Hz
            wavelength_type: "quarter" (λ/4), "half" (λ/2), "full" (λ), "dipole"
        
        Returns:
            dict: Wavelength and antenna length
        """
        c = 299792458  # Speed of light in m/s
        
        wavelength = c / frequency_hz
        
        if wavelength_type == "quarter":
            length = wavelength / 4
            type_name = "Quarter-wave (λ/4)"
        elif wavelength_type == "half":
            length = wavelength / 2
            type_name = "Half-wave (λ/2)"
        elif wavelength_type == "full":
            length = wavelength
            type_name = "Full-wave (λ)"
        elif wavelength_type == "dipole":
            length = wavelength / 2
            type_name = "Dipole (λ/2)"
        else:
            raise ValueError("wavelength_type must be 'quarter', 'half', 'full', or 'dipole'")
        
        return {
            "frequency": {
                "hz": frequency_hz,
                "mhz": round(frequency_hz / 1e6, 4),
                "ghz": round(frequency_hz / 1e9, 4)
            },
            "wavelength": {
                "meters": round(wavelength, 3),
                "cm": round(wavelength * 100, 1),
                "mm": round(wavelength * 1000, 1)
            },
            "antenna_type": type_name,
            "antenna_length": {
                "meters": round(length, 3),
                "cm": round(length * 100, 1),
                "inches": round(length * 39.37, 1)
            },
            "formula": f"λ = c/f = {c}/{frequency_hz} = {wavelength:.3f}m, Length = {wavelength:.3f}m × {wavelength_type} = {length:.3f}m"
        }


    def rf_db_conversion(self, power_w: float = None, power_mw: float = None, dbm: float = None):
        """
        dB, dBm, dBV, and power conversions.
        
        Formulas:
            dBm = 10 × log10(P_mW)
            P_mW = 10^(dBm/10)
            dBV = 20 × log10(V)
        
        Args:
            power_w: Power in Watts
            power_mw: Power in milliWatts
            dbm: Power in dBm
        
        Returns:
            dict: Conversions
        """
        if power_w is not None:
            power_mw = power_w * 1000
            dbm = 10 * math.log10(power_mw)
            result = {"power_w": power_w, "power_mw": power_mw, "dbm": round(dbm, 2)}
        elif power_mw is not None:
            dbm = 10 * math.log10(power_mw)
            result = {"power_mw": power_mw, "dbm": round(dbm, 2), "power_w": round(power_mw / 1000, 6)}
        elif dbm is not None:
            power_mw = 10 ** (dbm / 10)
            result = {"dbm": dbm, "power_mw": round(power_mw, 2), "power_w": round(power_mw / 1000, 6)}
        else:
            raise ValueError("Provide power_w, power_mw, or dbm")
        
        # Add power ratio
        result["power_ratio_db"] = round(10 * math.log10(result.get("power_mw", 1)), 2) if result.get("power_mw") else None
        
        return result


    def rf_am_modulation(self, carrier_amplitude: float, modulating_amplitude: float):
        """
        AM modulation calculator.
        
        Formula: m = Em / Ec (modulation index)
        
        Args:
            carrier_amplitude: Carrier amplitude (V)
            modulating_amplitude: Modulating signal amplitude (V)
        
        Returns:
            dict: Modulation index and percentages
        """
        m = modulating_amplitude / carrier_amplitude
        percent = m * 100
        
        if m < 0:
            status = "Negative (phase reversal)"
        elif m == 0:
            status = "No modulation (unmodulated carrier)"
        elif m < 1:
            status = "Under-modulated (safe)"
        elif m == 1:
            status = "100% modulation (maximum safe)"
        else:
            status = "Over-modulated (distortion)"
        
        return {
            "carrier_amplitude_v": carrier_amplitude,
            "modulating_amplitude_v": modulating_amplitude,
            "modulation_index": round(m, 3),
            "modulation_percent": round(percent, 1),
            "status": status,
            "formula": f"m = {modulating_amplitude}/{carrier_amplitude} = {m:.3f}"
        }


    def rf_fm_deviation(self, deviation_hz: float, modulating_freq_hz: float, max_deviation_hz: float = 75000):
        """
        FM deviation calculator.
        
        Args:
            deviation_hz: Frequency deviation (Hz)
            modulating_freq_hz: Modulating frequency (Hz)
            max_deviation_hz: Maximum allowed deviation (default 75kHz for broadcast FM)
        
        Returns:
            dict: Modulation index and bandwidth
        """
        mf = deviation_hz / modulating_freq_hz  # Modulation index
        bandwidth = 2 * (deviation_hz + modulating_freq_hz)  # Carson's rule
        
        if deviation_hz > max_deviation_hz:
            status = f"Exceeds maximum deviation ({max_deviation_hz/1000:.0f}kHz)"
        else:
            status = "Within limits"
        
        return {
            "deviation_hz": deviation_hz,
            "deviation_khz": round(deviation_hz / 1000, 2),
            "modulating_frequency_hz": modulating_freq_hz,
            "modulation_index": round(mf, 2),
            "bandwidth_hz": round(bandwidth, 2),
            "bandwidth_khz": round(bandwidth / 1000, 2),
            "status": status,
            "formula": f"mf = Δf/fm = {deviation_hz}/{modulating_freq_hz} = {mf:.2f}"
        }


    def rf_link_budget(self, tx_power_dbm: float, tx_gain_dbi: float, rx_gain_dbi: float, 
                        distance_km: float, frequency_mhz: float, rx_sensitivity_dbm: float,
                        cable_loss_db: float = 0, fade_margin_db: float = 10):
        """
        RF link budget calculator.
        
        Args:
            tx_power_dbm: Transmitter power (dBm)
            tx_gain_dbi: Transmitter antenna gain (dBi)
            rx_gain_dbi: Receiver antenna gain (dBi)
            distance_km: Distance in kilometers
            frequency_mhz: Frequency in MHz
            rx_sensitivity_dbm: Receiver sensitivity (dBm)
            cable_loss_db: Cable and connector loss (dB)
            fade_margin_db: Desired fade margin (dB)
        
        Returns:
            dict: Link budget analysis
        """
        # Free space path loss
        fspl = 20 * math.log10(distance_km) + 20 * math.log10(frequency_mhz) + 32.44
        
        # Received power
        rx_power_dbm = tx_power_dbm + tx_gain_dbi + rx_gain_dbi - fspl - cable_loss_db
        
        # Link margin
        link_margin = rx_power_dbm - rx_sensitivity_dbm
        
        # Feasibility
        if link_margin >= fade_margin_db:
            feasibility = "LINK FEASIBLE"
            status = f"Margin {link_margin:.1f}dB > fade margin {fade_margin_db}dB"
        else:
            feasibility = "LINK MARGINAL"
            status = f"Margin {link_margin:.1f}dB < fade margin {fade_margin_db}dB"
        
        return {
            "parameters": {
                "tx_power_dbm": tx_power_dbm,
                "tx_gain_dbi": tx_gain_dbi,
                "rx_gain_dbi": rx_gain_dbi,
                "distance_km": distance_km,
                "frequency_mhz": frequency_mhz,
                "rx_sensitivity_dbm": rx_sensitivity_dbm,
                "cable_loss_db": cable_loss_db,
                "fade_margin_db": fade_margin_db
            },
            "free_space_path_loss_db": round(fspl, 1),
            "received_power_dbm": round(rx_power_dbm, 1),
            "link_margin_db": round(link_margin, 1),
            "feasibility": feasibility,
            "status": status,
            "formula": f"FSPL = 20×log10({distance_km}) + 20×log10({frequency_mhz}) + 32.44 = {fspl:.1f}dB"
        }
    

    # ================================================================
    # COMPLETE BATTERY FUNCTIONS (Add to ElectronicsCalculator class)
    # ================================================================

    def battery_type_info(self, battery_type: str):
        """
        Internal: Get battery specifications by type.
        """
        types = {
            "li-ion": {
                "name": "Lithium-ion (LiCoO₂)",
                "nominal_v": 3.7, "full_v": 4.2, "cutoff_v": 2.8,
                "charge_c_max": 1.0, "discharge_c_max": 3.0,
                "rechargeable": True, "notes": "Most common, requires BMS"
            },
            "lifepo4": {
                "name": "Lithium Iron Phosphate (LiFePO₄)",
                "nominal_v": 3.2, "full_v": 3.65, "cutoff_v": 2.5,
                "charge_c_max": 1.0, "discharge_c_max": 5.0,
                "rechargeable": True, "notes": "Safer, longer cycle life"
            },
            "lead_acid": {
                "name": "Lead Acid (Flooded)",
                "nominal_v": 2.0, "full_v": 2.4, "cutoff_v": 1.75,
                "charge_c_max": 0.2, "discharge_c_max": 0.5,
                "rechargeable": True, "notes": "Heavy, cheap, needs maintenance"
            },
            "lead_acid_sla": {
                "name": "Lead Acid (AGM/SLA)",
                "nominal_v": 2.0, "full_v": 2.45, "cutoff_v": 1.8,
                "charge_c_max": 0.3, "discharge_c_max": 1.0,
                "rechargeable": True, "notes": "Sealed, no maintenance"
            },
            "nimh": {
                "name": "Nickel-Metal Hydride (NiMH)",
                "nominal_v": 1.2, "full_v": 1.4, "cutoff_v": 1.0,
                "charge_c_max": 1.0, "discharge_c_max": 2.0,
                "rechargeable": True, "notes": "AA/AAA rechargeable"
            },
            "nicd": {
                "name": "Nickel-Cadmium (NiCd)",
                "nominal_v": 1.2, "full_v": 1.4, "cutoff_v": 1.0,
                "charge_c_max": 1.0, "discharge_c_max": 5.0,
                "rechargeable": True, "notes": "High discharge, toxic"
            },
            "lto": {
                "name": "Lithium Titanate (LTO)",
                "nominal_v": 2.4, "full_v": 2.8, "cutoff_v": 1.8,
                "charge_c_max": 10.0, "discharge_c_max": 20.0,
                "rechargeable": True, "notes": "Very high charge/discharge"
            }
        }
        return types.get(battery_type.lower(), types["li-ion"])


    def battery_configuration(self, battery_type: str = "li-ion",
                            cell_voltage_v: float = None, cell_capacity_mah: float = None,
                            series_count: int = 1, parallel_count: int = 1,
                            load_ma: float = None, charge_current_ma: float = None):
        """
        Calculate battery pack configuration for ANY battery type.
        """
        batt = self.battery_type_info(battery_type)
        
        # Use provided voltage or default from type
        if cell_voltage_v:
            nominal_v = cell_voltage_v
        else:
            nominal_v = batt["nominal_v"]
        
        if not cell_capacity_mah:
            return {"error": "cell_capacity_mah is required"}
        
        total_cells = series_count * parallel_count
        pack_voltage = nominal_v * series_count
        pack_capacity_mah = cell_capacity_mah * parallel_count
        pack_energy_wh = (pack_voltage * pack_capacity_mah) / 1000
        pack_max_discharge_a = (pack_capacity_mah / 1000) * batt["discharge_c_max"]
        pack_max_charge_a = (pack_capacity_mah / 1000) * batt["charge_c_max"] if batt["rechargeable"] else None
        
        # Runtime
        runtime_hours = None
        if load_ma and load_ma > 0:
            runtime_hours = pack_capacity_mah / load_ma
        
        # Charge time
        charge_hours = None
        if charge_current_ma and charge_current_ma > 0 and batt["rechargeable"]:
            charge_hours = pack_capacity_mah / charge_current_ma
        
        # Configuration name
        if series_count == 1 and parallel_count == 1:
            config_name = "Single Cell"
        elif series_count == 1:
            config_name = f"{parallel_count}P (Parallel)"
        elif parallel_count == 1:
            config_name = f"{series_count}S (Series)"
        else:
            config_name = f"{series_count}S{parallel_count}P"
        
        return {
            "battery_type": batt["name"],
            "rechargeable": batt["rechargeable"],
            "configuration": {
                "name": config_name,
                "series": series_count,
                "parallel": parallel_count,
                "total_cells": total_cells
            },
            "cell_specs": {
                "type": battery_type.upper(),
                "nominal_voltage_v": nominal_v,
                "full_voltage_v": batt["full_v"],
                "cutoff_voltage_v": batt["cutoff_v"],
                "capacity_mah": cell_capacity_mah
            },
            "pack_specs": {
                "voltage_nominal_v": round(pack_voltage, 1),
                "voltage_full_v": round(batt["full_v"] * series_count, 1),
                "voltage_cutoff_v": round(batt["cutoff_v"] * series_count, 1),
                "capacity_mah": round(pack_capacity_mah, 0),
                "capacity_ah": round(pack_capacity_mah / 1000, 2),
                "energy_wh": round(pack_energy_wh, 1),
                "max_discharge_a": round(pack_max_discharge_a, 2),
                "max_charge_a": round(pack_max_charge_a, 2) if pack_max_charge_a else None
            },
            "runtime": {
                "load_ma": load_ma,
                "hours": round(runtime_hours, 2)
            } if load_ma else None,
            "charging": {
                "current_ma": charge_current_ma,
                "hours": round(charge_hours, 2)
            } if charge_current_ma and batt["rechargeable"] else None,
            "notes": batt["notes"]
        }


    def battery_compare_configurations(self, cell_voltage_v: float, cell_capacity_mah: float,
                                        series_cells: int = 1, parallel_cells: int = 1,
                                        load_ma: float = None, charge_current_ma: float = None):
        """
        Compare single battery vs different configurations.
        """
        # Get pack configuration
        pack = self.battery_configuration(
            battery_type="li-ion",
            cell_voltage_v=cell_voltage_v,
            cell_capacity_mah=cell_capacity_mah,
            series_count=series_cells,
            parallel_count=parallel_cells,
            load_ma=load_ma,
            charge_current_ma=charge_current_ma
        )
        
        # Get single cell reference
        single = self.battery_configuration(
            battery_type="li-ion",
            cell_voltage_v=cell_voltage_v,
            cell_capacity_mah=cell_capacity_mah,
            series_count=1,
            parallel_count=1,
            load_ma=load_ma,
            charge_current_ma=charge_current_ma
        )
        
        # Pros and Cons
        pros = []
        cons = []
        
        if series_cells > 1:
            pros.append(f"Higher voltage ({series_cells}×) for devices that need more power")
            pros.append("Reduces current for same power (P = V×I)")
            cons.append("Requires battery management system (BMS) for balancing")
            cons.append("If one cell fails, whole pack fails")
        
        if parallel_cells > 1:
            pros.append(f"Higher capacity ({parallel_cells}×) for longer runtime")
            pros.append("Higher maximum current capability")
            cons.append("Cells must be same voltage before connecting")
            cons.append("If one cell shorts, others discharge into it")
        
        if series_cells == 1 and parallel_cells == 1:
            pros.append("Simple, no balancing needed")
            pros.append("Safest configuration")
            cons.append("Limited voltage and capacity")
        
        return {
            "configuration": {
                "name": pack["configuration"]["name"],
                "series": series_cells,
                "parallel": parallel_cells,
                "total_cells": series_cells * parallel_cells
            },
            "single_cell": {
                "voltage_v": single["pack_specs"]["voltage_nominal_v"],
                "capacity_mah": single["pack_specs"]["capacity_mah"],
                "energy_wh": single["pack_specs"]["energy_wh"],
                "runtime_hours": single["runtime"]["hours"] if single["runtime"] else None
            },
            "battery_pack": {
                "voltage_v": pack["pack_specs"]["voltage_nominal_v"],
                "capacity_mah": pack["pack_specs"]["capacity_mah"],
                "energy_wh": pack["pack_specs"]["energy_wh"],
                "runtime_hours": pack["runtime"]["hours"] if pack["runtime"] else None,
                "max_discharge_a": pack["pack_specs"]["max_discharge_a"]
            },
            "comparison": {
                "voltage_x": series_cells,
                "capacity_x": parallel_cells,
                "energy_x": series_cells * parallel_cells
            },
            "pros_cons": {"pros": pros, "cons": cons},
            "notes": pack["notes"]
        }


    def battery_all_configurations(self, cell_voltage_v: float, cell_capacity_mah: float,
                                    cells_available: int = 4, load_ma: float = None):
        """
        Show ALL possible configurations for given number of cells.
        """
        configurations = []
        
        # Find all factor pairs (S × P = total cells)
        for s in range(1, cells_available + 1):
            for p in range(1, cells_available + 1):
                if s * p == cells_available:
                    config = self.battery_compare_configurations(
                        cell_voltage_v=cell_voltage_v,
                        cell_capacity_mah=cell_capacity_mah,
                        series_cells=s,
                        parallel_cells=p,
                        load_ma=load_ma
                    )
                    configurations.append(config)
        
        # Sort by voltage (lowest to highest)
        configurations.sort(key=lambda x: x["battery_pack"]["voltage_v"])
        
        # Find best runtime configuration
        best_runtime = max(configurations, key=lambda x: x["battery_pack"]["runtime_hours"] if x["battery_pack"]["runtime_hours"] else 0)
        
        return {
            "cell_specs": {
                "voltage_v": cell_voltage_v,
                "capacity_mah": cell_capacity_mah,
                "energy_wh": round((cell_voltage_v * cell_capacity_mah) / 1000, 2)
            },
            "cells_available": cells_available,
            "load_ma": load_ma,
            "configurations": [
                {
                    "name": cfg["configuration"]["name"],
                    "voltage_v": cfg["battery_pack"]["voltage_v"],
                    "capacity_mah": cfg["battery_pack"]["capacity_mah"],
                    "energy_wh": cfg["battery_pack"]["energy_wh"],
                    "runtime_hours": cfg["battery_pack"]["runtime_hours"]
                }
                for cfg in configurations
            ],
            "recommendation": f"Best runtime: {best_runtime['configuration']['name']} ({best_runtime['battery_pack']['runtime_hours']} hours at {load_ma}mA)" if load_ma else f"Best energy density: {best_runtime['configuration']['name']} ({best_runtime['battery_pack']['energy_wh']}Wh)"
        }


    def battery_compare_all_types(self, cell_capacity_mah: float,
                                    series_count: int = 1, parallel_count: int = 1,
                                    load_ma: float = None):
        """
        Compare SAME configuration across different battery types.
        """
        battery_types = ["li-ion", "lifepo4", "lead_acid", "lead_acid_sla", "nimh", "nicd", "lto"]
        
        comparisons = []
        
        for batt_type in battery_types:
            result = self.battery_configuration(
                battery_type=batt_type,
                cell_capacity_mah=cell_capacity_mah,
                series_count=series_count,
                parallel_count=parallel_count,
                load_ma=load_ma
            )
            
            if "error" not in result:
                comparisons.append({
                    "type": result["battery_type"],
                    "voltage_v": result["pack_specs"]["voltage_nominal_v"],
                    "capacity_mah": result["pack_specs"]["capacity_mah"],
                    "energy_wh": result["pack_specs"]["energy_wh"],
                    "runtime_hours": result["runtime"]["hours"] if result["runtime"] else None,
                    "max_discharge_a": result["pack_specs"]["max_discharge_a"],
                    "rechargeable": result["rechargeable"],
                    "notes": result["notes"]
                })
        
        # Find best energy density
        best = max(comparisons, key=lambda x: x["energy_wh"])
        
        return {
            "configuration": f"{series_count}S{parallel_count}P",
            "cell_capacity_mah": cell_capacity_mah,
            "load_ma": load_ma,
            "comparison": comparisons,
            "recommendation": f"{best['type']} has highest energy density ({best['energy_wh']}Wh at {best['voltage_v']}V)"
        }


    def battery_voltage_by_type(self, battery_type: str, cells_in_series: int = 1):
        """
        Get voltage ranges for specific battery type.
        """
        batt = self.battery_type_info(battery_type)
        
        return {
            "battery_type": batt["name"],
            "cells_in_series": cells_in_series,
            "nominal_voltage_v": round(batt["nominal_v"] * cells_in_series, 1),
            "full_voltage_v": round(batt["full_v"] * cells_in_series, 1),
            "cutoff_voltage_v": round(batt["cutoff_v"] * cells_in_series, 1),
            "rechargeable": batt["rechargeable"],
            "charge_c_rate_max": batt["charge_c_max"],
            "discharge_c_rate_max": batt["discharge_c_max"],
            "notes": batt["notes"]
        }
    

    # ================================================================
    # SOLAR PANEL CALCULATIONS
    # ================================================================

    def solar_panel_specs(self, voc: float, isc: float, vmp: float = None, imp: float = None):
        """
        Calculate solar panel specifications from datasheet values.
        
        Args:
            voc: Open Circuit Voltage (V)
            isc: Short Circuit Current (A)
            vmp: Maximum Power Voltage (V) — if not provided, estimate as 0.8 × voc
            imp: Maximum Power Current (A) — if not provided, estimate as 0.9 × isc
        
        Returns:
            dict: Panel specifications including max power (Wp)
        """
        if vmp is None:
            vmp = voc * 0.8
        if imp is None:
            imp = isc * 0.9
        
        pmp = vmp * imp  # Maximum power in Watts (Wp)
        fill_factor = (vmp * imp) / (voc * isc) if (voc * isc) > 0 else 0
        
        return {
            "panel_type": "Solar Panel",
            "specifications": {
                "voc_v": round(voc, 1),
                "isc_a": round(isc, 3),
                "vmp_v": round(vmp, 1),
                "imp_a": round(imp, 3),
                "pmp_w": round(pmp, 1),
                "fill_factor": round(fill_factor, 3)
            },
            "meaning": {
                "voc": "Open Circuit Voltage (no load, maximum voltage)",
                "isc": "Short Circuit Current (shorted, maximum current)",
                "vmp": "Voltage at Maximum Power Point",
                "imp": "Current at Maximum Power Point",
                "pmp": f"Maximum Power Output = {round(pmp,1)} Watts peak (Wp)",
                "ff": f"Fill Factor = {round(fill_factor*100,1)}% (higher is better)"
            }
        }


    def solar_parallel_series(self, panels: list, connection: str = "series"):
        """
        Calculate specifications for multiple solar panels connected in series or parallel.
        
        Args:
            panels: List of panel dicts with 'vmp', 'imp', 'pmp' or use solar_panel_specs output
            connection: "series" (voltage adds) or "parallel" (current adds)
        
        Returns:
            dict: Combined panel specifications
        """
        if not panels:
            return {"error": "No panels provided"}
        
        if connection.lower() == "series":
            total_v = sum(p.get("vmp", p.get("vmp", 0)) for p in panels)
            total_i = min(p.get("imp", p.get("imp", 0)) for p in panels)
            total_w = total_v * total_i
            config_name = f"{len(panels)} panels in SERIES"
            note = "Voltage adds, current limited by smallest panel"
        else:  # parallel
            total_v = min(p.get("vmp", p.get("vmp", 0)) for p in panels)
            total_i = sum(p.get("imp", p.get("imp", 0)) for p in panels)
            total_w = total_v * total_i
            config_name = f"{len(panels)} panels in PARALLEL"
            note = "Current adds, voltage limited by smallest panel"
        
        return {
            "configuration": config_name,
            "total_panels": len(panels),
            "total_vmp_v": round(total_v, 1),
            "total_imp_a": round(total_i, 2),
            "total_pmp_w": round(total_w, 1),
            "total_wh_per_day": round(total_w * 5, 0),  # 5 peak sun hours per day typical
            "note": note
        }


    def solar_charge_time(self, panel_w: float, battery_voltage_v: float, 
                        battery_capacity_ah: float, battery_type: str = "lead_acid",
                        panel_vmp: float = None, sun_hours_per_day: float = 5):
        """
        Calculate how long a solar panel takes to charge a battery.
        
        Args:
            panel_w: Solar panel power in Watts (Wp)
            battery_voltage_v: Battery bank voltage (V) — 12V, 24V
            battery_capacity_ah: Battery capacity in Ah
            battery_type: "lead_acid", "li_ion", "lifepo4"
            panel_vmp: Panel Vmp (if known, else estimated from voltage)
            sun_hours_per_day: Effective peak sun hours per day (default 5)
        
        Returns:
            dict: Charge time in hours and days
        """
        # Depth of Discharge (how much battery needs charging)
        dod_values = {"lead_acid": 0.5, "agm": 0.6, "li_ion": 0.8, "lifepo4": 0.9}
        dod = dod_values.get(battery_type.lower(), 0.5)
        
        # Usable battery energy needed
        battery_wh = battery_voltage_v * battery_capacity_ah
        needed_wh = battery_wh * dod
        
        # Panel output per hour (with losses)
        charge_controller_efficiency = 0.85  # PWM controller
        panel_output_wh_per_hour = panel_w * charge_controller_efficiency
        
        # Hours of direct sunlight needed
        hours_needed = needed_wh / panel_output_wh_per_hour
        
        # Days based on average sun hours per day
        days_needed = hours_needed / sun_hours_per_day
        
        return {
            "battery": {
                "type": battery_type.upper(),
                "voltage_v": battery_voltage_v,
                "capacity_ah": battery_capacity_ah,
                "total_wh": battery_wh,
                "needed_wh": round(needed_wh, 0)
            },
            "solar_panel": {
                "power_wp": panel_w,
                "charge_controller_efficiency": f"{charge_controller_efficiency*100:.0f}%",
                "output_wh_per_hour": round(panel_output_wh_per_hour, 1)
            },
            "charge_time": {
                "hours_direct_sun": round(hours_needed, 1),
                "days_average": round(days_needed, 1),
                "sun_hours_per_day_assumed": sun_hours_per_day
            },
            "formula": f"Time = ({battery_wh}Wh × {dod} DoD) / ({panel_w}W × {charge_controller_efficiency}) = {hours_needed:.1f}h"
        }


    def solar_panel_for_load(self, daily_load_wh: float, battery_voltage_v: float,
                            battery_type: str = "lead_acid", sun_hours_per_day: float = 5,
                            reserve_days: int = 1):
        """
        Calculate solar panel and battery size needed for a given daily load.
        
        Args:
            daily_load_wh: Daily energy consumption in Watt-hours
            battery_voltage_v: Battery bank voltage (12V, 24V, 48V)
            battery_type: Battery chemistry
            sun_hours_per_day: Average peak sun hours (Pakistan: 5-6 hours)
            reserve_days: Days of battery backup without sun
        
        Returns:
            dict: Recommended panel size and battery capacity
        """
        dod_values = {"lead_acid": 0.5, "agm": 0.6, "li_ion": 0.8, "lifepo4": 0.9}
        dod = dod_values.get(battery_type.lower(), 0.5)
        
        # Battery size needed
        battery_wh_needed = daily_load_wh * reserve_days
        battery_ah_needed = battery_wh_needed / battery_voltage_v
        battery_ah_recommended = battery_ah_needed / dod
        
        # Panel size needed (accounting for losses)
        panel_w_needed = (daily_load_wh / sun_hours_per_day) / 0.85  # 85% system efficiency
        
        return {
            "daily_load_wh": daily_load_wh,
            "location": {
                "assumed_sun_hours_per_day": sun_hours_per_day,
                "note": "Pakistan: 5-6 peak sun hours typical"
            },
            "battery": {
                "type": battery_type.upper(),
                "voltage_v": battery_voltage_v,
                "required_ah": round(battery_ah_needed, 1),
                "recommended_ah": round(battery_ah_recommended, 0),
                "reserve_days": reserve_days
            },
            "solar_panel": {
                "required_wp": round(panel_w_needed, 0),
                "recommended_wp": round(panel_w_needed * 1.2, 0),  # 20% margin
                "example_panels": f"Use {round(panel_w_needed/100,0)} × 100W panels or {round(panel_w_needed/50,0)} × 50W panels"
            },
            "formulas": {
                "battery": f"Battery Ah = ({daily_load_wh}Wh × {reserve_days} days) / {battery_voltage_v}V / {dod} = {round(battery_ah_recommended,0)}Ah",
                "panel": f"Panel Wp = {daily_load_wh}Wh / {sun_hours_per_day}h / 0.85 = {round(panel_w_needed,0)}W"
            }
        }


    def solar_panel_vs_battery(self, panel_w: float, sun_hours: float = 5):
        """
        Calculate how much energy a solar panel produces per day.
        
        Args:
            panel_w: Solar panel power in Watts (Wp)
            sun_hours: Peak sun hours per day (default 5)
        
        Returns:
            dict: Daily energy production
        """
        daily_wh = panel_w * sun_hours * 0.85  # 85% system efficiency
        
        # Equivalent device runtimes
        device_runtimes = {
            "LED Bulb (10W)": daily_wh / 10,
            "Laptop (40W)": daily_wh / 40,
            "TV (35W)": daily_wh / 35,
            "Fan (70W)": daily_wh / 70,
            "Router (8W)": daily_wh / 8,
            "Phone charger (5W)": daily_wh / 5
        }
        
        return {
            "panel_power_wp": panel_w,
            "sun_hours_per_day": sun_hours,
            "daily_energy_wh": round(daily_wh, 0),
            "monthly_energy_kwh": round(daily_wh * 30 / 1000, 1),
            "yearly_energy_kwh": round(daily_wh * 365 / 1000, 1),
            "can_run_devices_for_hours": device_runtimes
        }



    # ================================================================
    # TOROID INDUCTOR CALCULATOR
    # ================================================================

    @staticmethod
    def toroid_core_properties(od_mm: float, id_mm: float, ht_mm: float):
        """
        Calculate core physical properties from dimensions.
        
        Args:
            od_mm: Outer diameter (mm)
            id_mm: Inner diameter (mm)
            ht_mm: Height (mm)
        
        Returns:
            dict: Core constants and dimensions
        """
        mean_diameter_mm = (od_mm + id_mm) / 2
        mean_path_length_mm = math.pi * mean_diameter_mm
        cross_section_mm2 = ht_mm * (od_mm - id_mm) / 2
        core_constant = mean_path_length_mm / cross_section_mm2
        
        return {
            "dimensions_mm": {
                "outer_diameter": od_mm,
                "inner_diameter": id_mm,
                "height": ht_mm,
                "mean_diameter": round(mean_diameter_mm, 2)
            },
            "magnetic_path": {
                "mean_path_length_mm": round(mean_path_length_mm, 2),
                "mean_path_length_m": round(mean_path_length_mm / 1000, 4),
                "cross_sectional_area_mm2": round(cross_section_mm2, 2),
                "cross_sectional_area_m2": round(cross_section_mm2 / 1e6, 8),
                "core_constant_mm1": round(core_constant, 3)
            }
        }


    def toroid_al_factor(self, permeability: float, od_mm: float, id_mm: float, ht_mm: float):
        """
        Calculate A_L (inductance factor) for a toroid core.
        
        Formula: A_L = (µ₀ × µᵣ × A_e) / l_e
        
        Args:
            permeability: Relative permeability (µᵣ) of core material
            od_mm: Outer diameter (mm)
            id_mm: Inner diameter (mm)
            ht_mm: Height (mm)
        
        Returns:
            dict: A_L value in nH/N²
        """
        mu0 = 4 * math.pi * 1e-7  # H/m
        Ae = ht_mm * (od_mm - id_mm) / 2  # mm²
        Ae_m2 = Ae / 1e6
        le_m = math.pi * (od_mm + id_mm) / 2 / 1000
        
        al_henry = (mu0 * permeability * Ae_m2) / le_m
        al_nh = al_henry * 1e9
        
        return {
            "al_value_nh_per_turn2": round(al_nh, 2),
            "al_value_uh_per_turn2": round(al_nh / 1000, 4),
            "formula": f"A_L = (μ₀ × μᵣ × A_e) / l_e = {al_nh:.2f} nH/N²"
        }


    def toroid_inductance(self, turns: int, permeability: float, od_mm: float, id_mm: float, ht_mm: float):
        """
        Calculate inductance for a toroid winding.
        
        Formula: L = A_L × N²
        
        Args:
            turns: Number of turns (N)
            permeability: Relative permeability of core material
            od_mm: Outer diameter (mm)
            id_mm: Inner diameter (mm)
            ht_mm: Height (mm)
        
        Returns:
            dict: Inductance in various units
        """
        # Get A_L value
        al_nh = self.toroid_al_factor(permeability, od_mm, id_mm, ht_mm)["al_value_nh_per_turn2"]
        
        # Calculate inductance
        L_nh = al_nh * (turns ** 2)
        L_uh = L_nh / 1000
        L_mh = L_nh / 1_000_000
        L_h = L_nh / 1_000_000_000
        
        return {
            "inductance": {
                "nanohenry": round(L_nh, 1),
                "microhenry": round(L_uh, 3),
                "millihenry": round(L_mh, 5),
                "henry": round(L_h, 8)
            },
            "turns": turns,
            "al_value_nh_turn2": al_nh,
            "formula": f"L = A_L × N² = {al_nh:.1f} × {turns}² = {L_uh:.2f} µH"
        }


    def toroid_turns_for_target(self, target_uh: float, permeability: float, od_mm: float, id_mm: float, ht_mm: float):
        """
        Calculate required turns to achieve target inductance.
        
        Formula: N = √(L / A_L)
        
        Args:
            target_uh: Target inductance in microhenries (µH)
            permeability: Relative permeability of core material
            od_mm: Outer diameter (mm)
            id_mm: Inner diameter (mm)
            ht_mm: Height (mm)
        
        Returns:
            dict: Required turns and inductance after rounding
        """
        # Get A_L value in µH/N²
        al_uh = self.toroid_al_factor(permeability, od_mm, id_mm, ht_mm)["al_value_uh_per_turn2"]
        
        # Calculate turns needed
        turns_calculated = math.sqrt(target_uh / al_uh)
        turns_rounded = round(turns_calculated)
        
        # Actual inductance with rounded turns
        actual_uh = al_uh * (turns_rounded ** 2)
        error_pct = ((actual_uh - target_uh) / target_uh) * 100
        
        return {
            "target_inductance_uh": target_uh,
            "calculated_turns": round(turns_calculated, 1),
            "recommended_turns": turns_rounded,
            "actual_inductance_uh": round(actual_uh, 2),
            "error_percent": round(error_pct, 1),
            "al_value_uh_turn2": al_uh,
            "formula": f"N = √({target_uh} / {al_uh:.3f}) = {turns_calculated:.1f} turns → Use {turns_rounded} turns"
        }


    def toroid_wire_length(self, turns: int, od_mm: float, id_mm: float):
        """
        Calculate wire length needed for toroid winding.
        
        Args:
            turns: Number of turns
            od_mm: Outer diameter (mm)
            id_mm: Inner diameter (mm)
        
        Returns:
            dict: Wire length in various units
        """
        mean_diameter_mm = (od_mm + id_mm) / 2
        length_per_turn_mm = math.pi * mean_diameter_mm
        total_length_mm = length_per_turn_mm * turns
        total_length_m = total_length_mm / 1000
        
        return {
            "mean_diameter_mm": round(mean_diameter_mm, 2),
            "length_per_turn": {
                "mm": round(length_per_turn_mm, 1),
                "cm": round(length_per_turn_mm / 10, 2),
                "inches": round(length_per_turn_mm / 25.4, 2)
            },
            "total_length": {
                "mm": round(total_length_mm, 0),
                "m": round(total_length_m, 2),
                "cm": round(total_length_m * 100, 0),
                "inches": round(total_length_m * 39.37, 1)
            },
            "turns": turns
        }


    def toroid_max_turns(self, id_mm: float, wire_diameter_mm: float, fill_factor: float = 0.3):
        """
        Calculate maximum theoretical turns for a toroid core.
        
        Args:
            id_mm: Inner diameter (mm)
            wire_diameter_mm: Wire diameter including insulation (mm)
            fill_factor: Fill factor (0.2-0.4, typical 0.3 for hand-wound)
        
        Returns:
            dict: Maximum practical turns
        """
        # Available winding area (inner circumference)
        inner_circumference_mm = math.pi * id_mm
        
        # Theoretical maximum turns
        max_turns_theoretical = inner_circumference_mm / wire_diameter_mm
        
        # Practical with fill factor
        max_turns_practical = int(max_turns_theoretical * fill_factor)
        
        return {
            "inner_diameter_mm": id_mm,
            "wire_diameter_mm": wire_diameter_mm,
            "fill_factor": fill_factor,
            "theoretical_max_turns": round(max_turns_theoretical, 0),
            "practical_max_turns": max_turns_practical,
            "recommended_max_turns": max_turns_practical - 5,  # Safety margin
            "warning": f"For hand-winding, stay below {max_turns_practical} turns",
            "formula": f"Max turns = ({math.pi:.2f} × {id_mm}) / {wire_diameter_mm} × {fill_factor} = {max_turns_practical}"
        }


    def toroid_inductor_design(self, target_uh: float, core_permeability: float,
                            od_mm: float, id_mm: float, ht_mm: float,
                            wire_diameter_mm: float = None):
        """
        Complete toroid inductor design tool.
        
        Args:
            target_uh: Target inductance in µH
            core_permeability: Core material permeability (µᵣ)
            od_mm: Outer diameter (mm)
            id_mm: Inner diameter (mm)
            ht_mm: Height (mm)
            wire_diameter_mm: Wire diameter for winding (optional)
        
        Returns:
            dict: Complete inductor design
        """
        # Core properties
        core = self.toroid_core_properties(od_mm, id_mm, ht_mm)
        
        # A_L value
        al = self.toroid_al_factor(core_permeability, od_mm, id_mm, ht_mm)
        
        # Turns needed
        turns_result = self.toroid_turns_for_target(target_uh, core_permeability, od_mm, id_mm, ht_mm)
        turns = turns_result["recommended_turns"]
        
        # Actual inductance
        inductance = self.toroid_inductance(turns, core_permeability, od_mm, id_mm, ht_mm)
        
        result = {
            "target_inductance_uh": target_uh,
            "core": core,
            "al_value": al,
            "turns_required": turns_result,
            "achieved_inductance": inductance
        }
        
        # Add wire info if provided
        if wire_diameter_mm:
            wire_length = self.toroid_wire_length(turns, od_mm, id_mm)
            max_turns = self.toroid_max_turns(id_mm, wire_diameter_mm)
            result["wire_info"] = wire_length
            result["winding_limits"] = max_turns
            
            # Check feasibility (ALWAYS set either warning or feasibility)
            if turns > max_turns["practical_max_turns"]:
                result["warning"] = f"⚠️ Turns ({turns}) exceeds practical maximum ({max_turns['practical_max_turns']})! Use smaller wire or larger core."
                result["feasibility"] = f"❌ INFEASIBLE: {turns} turns > {max_turns['practical_max_turns']} turn limit"
            else:
                result["feasibility"] = f"✅ Design feasible: {turns} turns within {max_turns['practical_max_turns']} turn limit"
        
        return result


    def toroid_core_selector(self, target_uh: float, turns: int, id_mm: float = None, od_mm: float = None):
        """
        Find required core permeability for given inductance and turns.
        
        Formula: μᵣ = (L × l_e) / (µ₀ × A_e × N²)
        
        Args:
            target_uh: Target inductance in µH
            turns: Number of turns
            id_mm: Inner diameter (mm) - optional
            od_mm: Outer diameter (mm) - optional
        
        Returns:
            dict: Required permeability
        """
        mu0 = 4 * math.pi * 1e-7
        
        if id_mm and od_mm:
            # Use provided dimensions
            Ae = 10 * (od_mm - id_mm) / 2  # Approximate
            le = math.pi * (od_mm + id_mm) / 2
        else:
            # Standard core sizes
            Ae = 50  # mm² approximation
            le = 60  # mm approximation
        
        Ae_m2 = Ae / 1e6
        le_m = le / 1000
        L = target_uh / 1_000_000
        
        required_mu = (L * le_m) / (mu0 * Ae_m2 * (turns ** 2))
        
        # Common material permeabilities
        common_materials = [
            {"name": "Iron Powder (Micrometals)", "mu": 10, "use": "High frequency, low permeability"},
            {"name": "Ferrite (Material 43)", "mu": 850, "use": "EMI suppression, 1-100MHz"},
            {"name": "Ferrite (Material 75)", "mu": 3000, "use": "Power conversion, 50kHz-500kHz"},
            {"name": "Ferrite (Material 77)", "mu": 2000, "use": "Wideband transformers"},
            {"name": "Sendust", "mu": 60, "use": "Low core loss, high saturation"},
            {"name": "MPP (Molypermalloy)", "mu": 550, "use": "High Q filters"},
            {"name": "High Flux", "mu": 160, "use": "High DC bias"},
            {"name": "Air Core", "mu": 1, "use": "Very high frequency, no saturation"}
        ]
        
        # Find nearest material
        nearest = min(common_materials, key=lambda x: abs(x["mu"] - required_mu))
        
        return {
            "target_inductance_uh": target_uh,
            "turns": turns,
            "required_permeability_mu": round(required_mu, 0),
            "recommended_material": nearest,
            "closest_materials": [m for m in common_materials if abs(m["mu"] - required_mu) < 100],
            "formula": f"μᵣ = (L × l_e) / (μ₀ × A_e × N²) = {required_mu:.0f}"
        }
 

    # ================================================================
    # TRANSFORMER CALCULATIONS
    # ================================================================

    def transformer_voltage_ratio(self, Np: float, Ns: float, Vp: float = None, Vs: float = None) -> dict:
        """
        Calculate voltage transformation based on turns ratio.
        
        Formula: Vp / Vs = Np / Ns = a
        
        Args:
            Np: Primary turns
            Ns: Secondary turns
            Vp: Primary voltage (optional)
            Vs: Secondary voltage (optional)
        
        Returns:
            dict: Turns ratio, voltages, and transformer type
        """
        a = Np / Ns
        
        result = {
            "turns_ratio": round(a, 3),
            "Np": Np,
            "Ns": Ns,
            "type": "Step-down" if a > 1 else "Step-up" if a < 1 else "Isolation"
        }
        
        if Vp is not None:
            Vs_calc = Vp / a
            result["primary_voltage_v"] = Vp
            result["secondary_voltage_v"] = round(Vs_calc, 2)
            result["formula"] = f"Vs = Vp / a = {Vp} / {a:.3f} = {Vs_calc:.2f}V"
        
        if Vs is not None:
            Vp_calc = Vs * a
            result["secondary_voltage_v"] = Vs
            result["primary_voltage_v"] = round(Vp_calc, 2)
            result["formula"] = f"Vp = Vs × a = {Vs} × {a:.3f} = {Vp_calc:.2f}V"
        
        return result


    def transformer_current_ratio(self, Np: float, Ns: float, Ip: float = None, Is: float = None) -> dict:
        """
        Calculate current transformation based on turns ratio.
        
        Formula: Ip / Is = Ns / Np = 1/a
        
        Args:
            Np: Primary turns
            Ns: Secondary turns
            Ip: Primary current (A)
            Is: Secondary current (A)
        
        Returns:
            dict: Currents and turns ratio relationship
        """
        a = Np / Ns
        result = {"turns_ratio": round(a, 3)}
        
        if Ip is not None:
            Is_calc = Ip * a
            result["primary_current_a"] = Ip
            result["secondary_current_a"] = round(Is_calc, 3)
            result["formula"] = f"Is = Ip × a = {Ip} × {a:.3f} = {Is_calc:.3f}A"
        
        if Is is not None:
            Ip_calc = Is / a
            result["secondary_current_a"] = Is
            result["primary_current_a"] = round(Ip_calc, 3)
            result["formula"] = f"Ip = Is / a = {Is} / {a:.3f} = {Ip_calc:.3f}A"
        
        return result


    def transformer_impedance(self, Np: float, Ns: float, Z_secondary: float = None, Z_primary: float = None) -> dict:
        """
        Calculate impedance transformation (square of turns ratio).
        
        Formula: Zp = (Np/Ns)² × Zs = a² × Zs
        
        Args:
            Np: Primary turns
            Ns: Secondary turns
            Z_secondary: Load impedance on secondary (Ω)
            Z_primary: Source impedance on primary (Ω)
        
        Returns:
            dict: Reflected impedances
        """
        a = Np / Ns
        a_sq = a ** 2
        
        result = {
            "turns_ratio": round(a, 3),
            "impedance_ratio": round(a_sq, 2)
        }
        
        if Z_secondary is not None:
            Z_primary_reflected = a_sq * Z_secondary
            result["secondary_load_ohm"] = Z_secondary
            result["primary_reflected_impedance_ohm"] = round(Z_primary_reflected, 1)
            result["formula"] = f"Zp = a² × Zs = {a_sq:.2f} × {Z_secondary} = {Z_primary_reflected:.1f}Ω"
        
        if Z_primary is not None:
            Z_secondary_reflected = Z_primary / a_sq
            result["primary_source_ohm"] = Z_primary
            result["secondary_reflected_impedance_ohm"] = round(Z_secondary_reflected, 2)
            result["formula"] = f"Zs = Zp / a² = {Z_primary} / {a_sq:.2f} = {Z_secondary_reflected:.2f}Ω"
        
        return result


    def transformer_power(self, Vp: float = None, Ip: float = None, Vs: float = None, Is: float = None,
                        efficiency: float = 0.95) -> dict:
        """
        Calculate power transfer and efficiency.
        
        Formula: P = V × I, Pin = Pout (ideal)
        
        Args:
            Vp: Primary voltage (V)
            Ip: Primary current (A)
            Vs: Secondary voltage (V)
            Is: Secondary current (A)
            efficiency: Transformer efficiency (0-1, default 0.95)
        
        Returns:
            dict: Power calculations
        """
        result = {"efficiency_assumed": efficiency * 100}
        
        if Vp is not None and Ip is not None:
            Pin = Vp * Ip
            result["primary_power_w"] = round(Pin, 2)
        
        if Vs is not None and Is is not None:
            Pout = Vs * Is
            result["secondary_power_w"] = round(Pout, 2)
        
        if "primary_power_w" in result and "secondary_power_w" in result:
            eff_actual = result["secondary_power_w"] / result["primary_power_w"]
            result["calculated_efficiency_percent"] = round(eff_actual * 100, 1)
            Pin_est = result["secondary_power_w"] / efficiency
            result["estimated_primary_power_w"] = round(Pin_est, 2)
        
        return result


    def transformer_wire_size(self, current_a: float, current_density: float = 3.0) -> dict:
        """
        Calculate required wire size for transformer winding.
        
        Formula: A = I / J, d = 2 × √(A/π)
        
        Args:
            current_a: RMS current (A)
            current_density: Current density (A/mm², default 3.0)
        
        Returns:
            dict: Wire size recommendations
        """
        Aw_mm2 = current_a / current_density
        d_mm = 2 * (Aw_mm2 / math.pi) ** 0.5
        
        # Standard AWG lookup (simplified)
        awg_approx = max(18, min(40, int(round(-20 * math.log10(d_mm / 0.8128)))))
        
        return {
            "current_a": current_a,
            "current_density_a_per_mm2": current_density,
            "wire_area_mm2": round(Aw_mm2, 3),
            "wire_diameter_mm": round(d_mm, 2),
            "approx_awg": awg_approx,
            "formula": f"A = I/J = {current_a}/{current_density} = {Aw_mm2:.3f}mm²"
        }


    def transformer_turns_calculation(self, voltage: float, Ae_cm2: float, 
                                    B_max_tesla: float = 1.2, frequency_hz: float = 50) -> dict:
        """
        Calculate required primary turns for given core and voltage.
        
        Formula: N = V / (4.44 × f × B_max × Ae)
        
        Args:
            voltage: RMS voltage (V)
            Ae_cm2: Core cross-sectional area (cm²)
            B_max_tesla: Maximum flux density (T, typical 1.0-1.4 for silicon steel)
            frequency_hz: Operating frequency (Hz)
        
        Returns:
            dict: Required turns for primary winding
        """
        Ae_m2 = Ae_cm2 / 10000  # Convert cm² to m²
        N = voltage / (4.44 * frequency_hz * B_max_tesla * Ae_m2)
        
        return {
            "voltage_v": voltage,
            "core_area_cm2": Ae_cm2,
            "frequency_hz": frequency_hz,
            "B_max_tesla": B_max_tesla,
            "required_turns": round(N, 0),
            "turns_per_volt": round(N / voltage, 2),
            "formula": f"N = V / (4.44 × f × B × Ae) = {voltage} / (4.44 × {frequency_hz} × {B_max_tesla} × {Ae_m2:.6f}) = {round(N,0)} turns"
        }


    def transformer_design(self, Vp: float, Vs: float, Power_VA: float, 
                            frequency_hz: float = 50, J_A_per_mm2: float = 3.0,
                            Ae_cm2: float = 10, B_max_tesla: float = 1.2) -> dict:
        """
        Complete transformer design calculator.
        
        Args:
            Vp: Primary voltage (V)
            Vs: Secondary voltage (V)
            Power_VA: Power rating (VA)
            frequency_hz: Operating frequency (Hz)
            J_A_per_mm2: Current density (A/mm²)
            Ae_cm2: Core area (cm²) - estimated if not known
            B_max_tesla: Max flux density (T)
        
        Returns:
            dict: Complete transformer specifications
        """
        # Electrical parameters
        a = Vp / Vs
        Ip = Power_VA / Vp
        Is = Power_VA / Vs
        
        # Core sizing
        turns_result = self.transformer_turns_calculation(Vp, Ae_cm2, B_max_tesla, frequency_hz)
        Np = turns_result["required_turns"]
        Ns = Np / a
        
        # Wire sizing
        primary_wire = self.transformer_wire_size(Ip, J_A_per_mm2)
        secondary_wire = self.transformer_wire_size(Is, J_A_per_mm2)
        
        return {
            "specifications": {
                "primary_voltage_v": Vp,
                "secondary_voltage_v": Vs,
                "power_va": Power_VA,
                "frequency_hz": frequency_hz,
                "turns_ratio": round(a, 3),
                "type": "Step-down" if a > 1 else "Step-up"
            },
            "currents": {
                "primary_a": round(Ip, 2),
                "secondary_a": round(Is, 2)
            },
            "windings": {
                "primary_turns": round(Np, 0),
                "secondary_turns": round(Ns, 0),
                "primary_wire_mm": primary_wire["wire_diameter_mm"],
                "secondary_wire_mm": secondary_wire["wire_diameter_mm"],
                "primary_awg": primary_wire["approx_awg"],
                "secondary_awg": secondary_wire["approx_awg"]
            },
            "core": {
                "area_cm2": Ae_cm2,
                "B_max_tesla": B_max_tesla,
                "turns_per_volt": turns_result["turns_per_volt"]
            },
            "formulas": {
                "turns_ratio": f"a = {Vp}/{Vs} = {a:.3f}",
                "primary_current": f"Ip = {Power_VA}/{Vp} = {Ip:.2f}A",
                "secondary_current": f"Is = {Power_VA}/{Vs} = {Is:.2f}A"
            }
        }


    def transformer_center_tap(self, V_secondary_total: float, Np: float, Ns_total: float) -> dict:
        """
        Calculate center-tapped transformer voltages and turns.
        
        Args:
            V_secondary_total: Total secondary voltage (end-to-end)
            Np: Primary turns
            Ns_total: Total secondary turns (end-to-end)
        
        Returns:
            dict: Center-tapped voltages and turns
        """
        a = Np / Ns_total
        V_center = V_secondary_total / 2
        Ns_half = Ns_total / 2
        
        return {
            "secondary_total_voltage_v": V_secondary_total,
            "center_tap_voltage_v": round(V_center, 2),
            "primary_turns": Np,
            "secondary_total_turns": Ns_total,
            "secondary_half_turns": Ns_half,
            "turns_ratio": round(a, 3),
            "formula": f"V_ct = V_total/2 = {V_secondary_total}/2 = {V_center:.2f}V"
        }


    def transformer_example_designs(self) -> dict:
        """
        Common transformer design examples for reference.
        
        Returns:
            dict: Example transformer designs
        """
        return {
            "mains_230v_to_12v": {
                "Vp": 230, "Vs": 12, "Power_VA": 50,
                "description": "Typical wall adapter transformer"
            },
            "audio_output": {
                "Np": 2000, "Ns": 100, "Z_primary": 5000,
                "description": "Tube amp output transformer"
            },
            "speaker_matching": {
                "Z_primary": 8000, "Z_secondary": 8,
                "description": "Tube amp to 8Ω speaker matching"
            },
            "current_transformer": {
                "Np": 1, "Ns": 1000, "Ip": 10,
                "description": "Current transformer for metering"
            }
        }

electronic_calculator=ElectronicsCalculator()