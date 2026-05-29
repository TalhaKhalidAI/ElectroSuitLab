# test_mosfet.py
import sys
import os
sys.path.append('.')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.core.ElectronicsCalculator import ElectronicsCalculator

def main():
    calc = ElectronicsCalculator()
    
    print("=" * 80)
    print("MOSFET AMPLIFIER TESTS - COMPLETE")
    print("=" * 80)
    
    # ================================================================
    # COMMON SOURCE MOSFET TESTS
    # ================================================================
    print("\n" + "=" * 80)
    print("COMMON SOURCE MOSFET")
    print("=" * 80)
    
    # Test 1: Cutoff (Vg < Vth)
    print("\n1. CS - CUTOFF (Vg < Vth) - BAD BIAS")
    result = calc.common_source_mosfet(
        Vdd=12, Rd=4700, R1=100000, R2=10000,
        Vth=2.5, K=0.0007, Rs=0
    )
    print(f"   Vg={result['voltages']['Vg']}V, Vth=2.5V → Vg < Vth")
    print(f"   Id={result['currents']['Id_mA']}mA, Vds={result['voltages']['Vds']}V")
    print(f"   Region: {result['region']}")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 2: Weak Active (Vg just above Vth)
    print("\n2. CS - WEAK ACTIVE (Vg slightly > Vth) - POOR BIAS")
    result = calc.common_source_mosfet(
        Vdd=12, Rd=4700, R1=100000, R2=27000,
        Vth=2.5, K=0.0007, Rs=0
    )
    print(f"   Vg={result['voltages']['Vg']}V, Vth=2.5V → Vg just above Vth")
    print(f"   Id={result['currents']['Id_mA']}mA, Vds={result['voltages']['Vds']}V")
    print(f"   Region: {result['region']}")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 3: Good Active (Optimal bias)
    print("\n3. CS - GOOD ACTIVE (Optimal bias) - GOOD BIAS")
    result = calc.common_source_mosfet(
        Vdd=12, Rd=4700, R1=100000, R2=47000,
        Vth=2.5, K=0.0007, Rs=0
    )
    print(f"   Vg={result['voltages']['Vg']}V, Vth=2.5V, Vov={result['voltages']['Vov']}V")
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Vds={result['voltages']['Vds']}V, Vgs={result['voltages']['Vgs']}V")
    print(f"   Region: {result['region']}")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    print(f"   Zin: {result['impedance']['Zin_kohm']}kΩ")
    
    # Test 4: High Active (Vg too high)
    print("\n4. CS - HIGH ACTIVE (Vg too high) - WORSE BIAS")
    result = calc.common_source_mosfet(
        Vdd=12, Rd=4700, R1=100000, R2=100000,
        Vth=2.5, K=0.0007, Rs=0
    )
    print(f"   Vg={result['voltages']['Vg']}V, Vth=2.5V")
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Region: {result['region']}")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 5: Saturated (Low Rd)
    print("\n5. CS - SATURATED (Low Rd) - BAD BIAS")
    result = calc.common_source_mosfet(
        Vdd=12, Rd=1000, R1=100000, R2=100000,
        Vth=2.5, K=0.0007, Rs=0
    )
    print(f"   Vg={result['voltages']['Vg']}V")
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Region: {result['region']}")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 6: With Source Resistor
    print("\n6. CS - WITH SOURCE RESISTOR (Rs=100Ω) - IMPROVED BIAS")
    result = calc.common_source_mosfet(
        Vdd=12, Rd=4700, R1=100000, R2=47000,
        Vth=2.5, K=0.0007, Rs=100
    )
    print(f"   Vg={result['voltages']['Vg']}V, Vs={result['voltages']['Vs']}V")
    print(f"   Vgs={result['voltages']['Vgs']}V")
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Region: {result['region']}")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 7: With Load Resistor
    print("\n7. CS - WITH LOAD (RL=10kΩ) - EFFECT ON GAIN")
    result = calc.common_source_mosfet(
        Vdd=12, Rd=4700, R1=100000, R2=47000,
        Vth=2.5, K=0.0007, Rs=0, RL=10000
    )
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Gain without load: ~8.8x")
    print(f"   Gain with 10k load: {result['gain']['voltage_gain']}x")
    
    # ================================================================
    # COMMON DRAIN MOSFET TESTS
    # ================================================================
    print("\n" + "=" * 80)
    print("COMMON DRAIN MOSFET (Source Follower)")
    print("=" * 80)
    
    # Test 8: Cutoff
    print("\n8. CD - CUTOFF (Vg < Vth) - BAD BIAS")
    result = calc.common_drain_mosfet(
        Vdd=12, R1=100000, R2=10000, Rs=1000,
        Vth=2.5, K=0.05
    )
    print(f"   Vg={result['voltages']['Vg']}V, Vth=2.5V → Vg < Vth")
    print(f"   Vs={result['voltages']['Vs']}V, Id={result['currents']['Id_mA']}mA")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 9: Weak Active
    print("\n9. CD - WEAK ACTIVE (Poor bias)")
    result = calc.common_drain_mosfet(
        Vdd=12, R1=100000, R2=27000, Rs=1000,
        Vth=2.5, K=0.05
    )
    print(f"   Vg={result['voltages']['Vg']}V (just above Vth=2.5V)")
    print(f"   Vs={result['voltages']['Vs']}V, Id={result['currents']['Id_mA']}mA")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 10: Good Active
    print("\n10. CD - GOOD ACTIVE (Optimal buffer) - GOOD BIAS")
    result = calc.common_drain_mosfet(
        Vdd=12, R1=100000, R2=47000, Rs=1000,
        Vth=2.5, K=0.05
    )
    print(f"   Vg={result['voltages']['Vg']}V")
    print(f"   Vs={result['voltages']['Vs']}V, Vgs={result['voltages']['Vgs']}V")
    print(f"   Id={result['currents']['Id_mA']}mA")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    print(f"   Zin: {result['impedance']['Zin_kohm']}kΩ")
    print(f"   Zout: {result['impedance']['Zout_ohm']}Ω")
    
    # Test 11: High Bias
    print("\n11. CD - HIGH BIAS (Vg too high) - WORSE BIAS")
    result = calc.common_drain_mosfet(
        Vdd=12, R1=100000, R2=100000, Rs=1000,
        Vth=2.5, K=0.05
    )
    print(f"   Vg={result['voltages']['Vg']}V")
    print(f"   Vs={result['voltages']['Vs']}V, Vgs={result['voltages']['Vgs']}V")
    print(f"   Id={result['currents']['Id_mA']}mA")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 12: With Source Resistance
    print("\n12. CD - WITH SOURCE RESISTANCE (Rsource=1kΩ) - EFFECT ON GAIN")
    result = calc.common_drain_mosfet(
        Vdd=12, R1=100000, R2=47000, Rs=1000,
        Vth=2.5, K=0.05, Rsource=1000
    )
    print(f"   Gain without Rsource: ~0.94x")
    print(f"   Gain with Rsource=1k: {result['gain']['voltage_gain']}x")
    
    # ================================================================
    # COMMON GATE MOSFET TESTS
    # ================================================================
    print("\n" + "=" * 80)
    print("COMMON GATE MOSFET")
    print("=" * 80)
    
    # Test 13: Cutoff
    print("\n13. CG - CUTOFF (Vbias < Vth) - BAD BIAS")
    result = calc.common_gate_mosfet(
        Vdd=12, Rd=4700, Rs=470, Vbias=2.0,
        Vth=2.5, K=0.005
    )
    print(f"   Vbias={result['voltages']['Vg']}V, Vth=2.5V → Vg < Vth")
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 14: Weak Active
    print("\n14. CG - WEAK ACTIVE (Vbias slightly > Vth) - POOR BIAS")
    result = calc.common_gate_mosfet(
        Vdd=12, Rd=4700, Rs=470, Vbias=2.7,
        Vth=2.5, K=0.005
    )
    print(f"   Vbias={result['voltages']['Vg']}V, Vth=2.5V")
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 15: Good Active
    print("\n15. CG - GOOD ACTIVE (Optimal bias) - GOOD BIAS")
    result = calc.common_gate_mosfet(
        Vdd=12, Rd=4700, Rs=470, Vbias=3.5,
        Vth=2.5, K=0.005
    )
    print(f"   Vbias={result['voltages']['Vg']}V")
    print(f"   Vs={result['voltages']['Vs']}V, Vgs={result['voltages']['Vgs']}V")
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    print(f"   Zin: {result['impedance']['Zin_ohm']}Ω (very low)")
    
    # Test 16: High Bias
    print("\n16. CG - HIGH BIAS (Vbias too high) - WORSE BIAS")
    result = calc.common_gate_mosfet(
        Vdd=12, Rd=4700, Rs=470, Vbias=5.0,
        Vth=2.5, K=0.005
    )
    print(f"   Vbias={result['voltages']['Vg']}V")
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Gain: {result['gain']['voltage_gain']}x")
    
    # Test 17: With Load
    print("\n17. CG - WITH LOAD (RL=10kΩ) - EFFECT ON GAIN")
    result = calc.common_gate_mosfet(
        Vdd=12, Rd=4700, Rs=470, Vbias=3.5,
        Vth=2.5, K=0.005, RL=10000
    )
    print(f"   Gain without load: ~22x")
    print(f"   Gain with 10k load: {result['gain']['voltage_gain']}x")
    
    # Test 18: Low Rd
    print("\n18. CG - LOW Rd (High current) - DIFFERENT LOAD")
    result = calc.common_gate_mosfet(
        Vdd=12, Rd=1000, Rs=100, Vbias=3.5,
        Vth=2.5, K=0.05
    )
    print(f"   Id={result['currents']['Id_mA']}mA, Vd={result['voltages']['Vd']}V")
    print(f"   Gain: {result['gain']['voltage_gain']}x")

    print("\n" + "=" * 80)
    print("ALL 18 TESTS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    main()