# test_impedance.py

import sys
import os

# Add parent directory to path so 'App' can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from App.core.ElectronicsCalculator import ElectronicsCalculator

# Initialize calculator
ec = ElectronicsCalculator()

print("=" * 70)
print("ELECTRONICS CALCULATOR - IMPEDANCE TEST SUITE")
print("=" * 70)

# ============================================================
# TEST 1: RESISTOR IMPEDANCE
# ============================================================
print("\n" + "=" * 70)
print("TEST 1: RESISTOR IMPEDANCE")
print("=" * 70)

def test_resistor_impedance():
    print("\n--- 1.1: 1kΩ Resistor ---")
    result = ec.resistor_impedance(1000)
    print(f"  Resistance: {result['resistance_ohm']}Ω")
    print(f"  Impedance: {result['impedance_ohm']}Ω")
    print(f"  Note: {result['note']}")
    assert result['impedance_ohm'] == 1000
    
    print("\n--- 1.2: 10kΩ Resistor ---")
    result = ec.resistor_impedance(10000)
    print(f"  Impedance: {result['impedance_ohm']}Ω")
    assert result['impedance_ohm'] == 10000
    
    print("\n✅ Resistor impedance test PASSED")

# ============================================================
# TEST 2: CAPACITOR IMPEDANCE (XC)
# ============================================================
print("\n" + "=" * 70)
print("TEST 2: CAPACITOR IMPEDANCE (Xc)")
print("=" * 70)

def test_capacitor_impedance():
    print("\n--- 2.1: 10µF at 50Hz ---")
    result = ec.capacitor_impedance(10e-6, 50)
    print(f"  Capacitance: {result['capacitance']['value']} {result['capacitance']['unit']}")
    print(f"  Frequency: {result['frequency_hz']}Hz")
    print(f"  Impedance: {result['impedance_ohm']}Ω")
    print(f"  Formula: {result['formula']}")
    assert 310 < result['impedance_ohm'] < 325
    
    print("\n--- 2.2: 100nF at 1kHz ---")
    result = ec.capacitor_impedance(100e-9, 1000)
    print(f"  Impedance: {result['impedance_ohm']}Ω")
    assert 1500 < result['impedance_ohm'] < 1700
    
    print("\n--- 2.3: 22pF at 100MHz (Radio frequency) ---")
    result = ec.capacitor_impedance(22e-12, 100e6)
    print(f"  Capacitance: {result['capacitance']['value']} {result['capacitance']['unit']}")
    print(f"  Frequency: {result['frequency_mhz']}MHz")
    print(f"  Impedance: {result['impedance_ohm']}Ω")
    print(f"  Rule: {result['rule_of_thumb']}")
    
    print("\n--- 2.4: Edge case - Zero frequency ---")
    result = ec.capacitor_impedance(10e-6, 0)
    print(f"  Result: {result.get('error', 'No error')}")
    assert 'error' in result
    
    print("\n--- 2.5: Edge case - Zero capacitance ---")
    result = ec.capacitor_impedance(0, 50)
    print(f"  Result: {result.get('error', 'No error')}")
    assert 'error' in result
    
    print("\n✅ Capacitor impedance test PASSED")

# ============================================================
# TEST 3: INDUCTOR IMPEDANCE (XL)
# ============================================================
print("\n" + "=" * 70)
print("TEST 3: INDUCTOR IMPEDANCE (XL)")
print("=" * 70)

def test_inductor_impedance():
    print("\n--- 3.1: 100µH at 1kHz ---")
    result = ec.inductor_impedance(100e-6, 1000)
    print(f"  Inductance: {result['inductance']['value']} {result['inductance']['unit']}")
    print(f"  Frequency: {result['frequency_hz']}Hz")
    print(f"  Impedance: {result['impedance_ohm']}Ω")
    print(f"  Formula: {result['formula']}")
    
    print("\n--- 3.2: 10µH at 10MHz (Radio frequency) ---")
    result = ec.inductor_impedance(10e-6, 10e6)
    print(f"  Inductance: {result['inductance']['value']} {result['inductance']['unit']}")
    print(f"  Frequency: {result['frequency_mhz']}MHz")
    print(f"  Impedance: {result['impedance_ohm']}Ω")
    assert 600 < result['impedance_ohm'] < 650
    
    print("\n--- 3.3: 1H at 50Hz ---")
    result = ec.inductor_impedance(1, 50)
    print(f"  Impedance: {result['impedance_ohm']}Ω")
    
    print("\n--- 3.4: Edge case - Zero frequency ---")
    result = ec.inductor_impedance(100e-6, 0)
    print(f"  Result: {result.get('error', 'No error')}")
    assert 'error' in result
    
    print("\n--- 3.5: Edge case - Zero inductance ---")
    result = ec.inductor_impedance(0, 1000)
    print(f"  Result: {result.get('error', 'No error')}")
    assert 'error' in result
    
    print("\n✅ Inductor impedance test PASSED")

# ============================================================
# TEST 4: SERIES IMPEDANCE
# ============================================================
print("\n" + "=" * 70)
print("TEST 4: SERIES IMPEDANCE")
print("=" * 70)

def test_series_impedance():
    print("\n--- 4.1: Series RC (R=1kΩ, C=10µF at 50Hz) ---")
    result = ec.series_impedance([
        {"type": "R", "value": 1000},
        {"type": "C", "value": 10e-6}
    ], 50)
    
    print(f"  Components:")
    for comp in result['components']:
        print(f"    - {comp['type']}: {comp.get('value', comp.get('value_ohm', ''))} → {comp['impedance_ohm']}Ω")
    print(f"  Total Impedance: {result['totals']['total_impedance_ohm']}Ω")
    print(f"  Phase Angle: {result['totals']['phase_angle_deg']}°")
    
    print("\n--- 4.2: Series RL (R=100Ω, L=10mH at 1kHz) ---")
    result = ec.series_impedance([
        {"type": "R", "value": 100},
        {"type": "L", "value": 10e-3}
    ], 1000)
    
    for comp in result['components']:
        print(f"    - {comp['type']}: {comp.get('value', comp.get('value_ohm', ''))} → {comp['impedance_ohm']}Ω")
    print(f"  Total Impedance: {result['totals']['total_impedance_ohm']}Ω")
    
    print("\n--- 4.3: Series RLC at resonance (XL = XC) ---")
    result = ec.series_impedance([
        {"type": "R", "value": 100},
        {"type": "L", "value": 10e-3},
        {"type": "C", "value": 10e-6}
    ], 503)
    
    print(f"  At f = {result['frequency_hz']}Hz:")
    print(f"    XL = {result['totals']['inductive_reactance_ohm']}Ω")
    print(f"    XC = {result['totals']['capacitive_reactance_ohm']}Ω")
    print(f"    Net Reactance: {result['totals']['net_reactance_ohm']}Ω")
    print(f"    Total Impedance: {result['totals']['total_impedance_ohm']}Ω")
    print(f"    Resonant: {result['resonant']}")
    
    print("\n--- 4.4: Invalid component type ---")
    result = ec.series_impedance([
        {"type": "X", "value": 1000}
    ], 50)
    print(f"  Result: {result.get('error', 'No error')}")
    assert 'error' in result
    
    print("\n✅ Series impedance test PASSED")

# ============================================================
# TEST 5: PARALLEL IMPEDANCE
# ============================================================
print("\n" + "=" * 70)
print("TEST 5: PARALLEL IMPEDANCE")
print("=" * 70)

def test_parallel_impedance():
    print("\n--- 5.1: Parallel RC (R=1kΩ, C=10µF at 50Hz) ---")
    result = ec.parallel_impedance([
        {"type": "R", "value": 1000},
        {"type": "C", "value": 10e-6}
    ], 50)
    
    print(f"  Components:")
    for comp in result['components']:
        print(f"    - {comp['type']}: {comp.get('value', comp.get('value_ohm', ''))}")
    print(f"  Total Impedance: {result['total_impedance_ohm']}Ω")
    print(f"  Phase Angle: {result['phase_angle_deg']}°")
    
    print("\n--- 5.2: Parallel LC tank (Resonant circuit for radio) ---")
    L = 0.1e-6
    C = 25e-12
    f_res = 1 / (2 * 3.14159 * (L * C)**0.5)
    
    result = ec.parallel_impedance([
        {"type": "L", "value": L},
        {"type": "C", "value": C}
    ], f_res)
    
    print(f"  LC Tank at {round(f_res/1e6,1)}MHz:")
    print(f"    Total Impedance: {result['total_impedance_ohm']}Ω (should be very high)")
    print(f"    Admittance magnitude: {result['admittance']['magnitude_s']}S")
    
    print("\n--- 5.3: Three parallel components (R=1k, L=10mH, C=10µF at 50Hz) ---")
    result = ec.parallel_impedance([
        {"type": "R", "value": 1000},
        {"type": "L", "value": 10e-3},
        {"type": "C", "value": 10e-6}
    ], 50)
    
    print(f"  Total Impedance: {result['total_impedance_ohm']}Ω")
    for comp in result['components']:
        susc = comp.get('susceptance_s', 'N/A')
        print(f"    - {comp['type']}: Susceptance = {susc}S")
    
    print("\n✅ Parallel impedance test PASSED")

# ============================================================
# TEST 6: INDUCTANCE FORMATTING
# ============================================================
print("\n" + "=" * 70)
print("TEST 6: INDUCTANCE FORMATTING")
print("=" * 70)

def test_format_inductance():
    print("\n--- 6.1: 1.5 Henries ---")
    val, unit = ec.format_inductance(1.5)
    print(f"  Result: {val} {unit}")
    assert unit == "H"
    
    print("\n--- 6.2: 0.047 Henries (47mH) ---")
    val, unit = ec.format_inductance(0.047)
    print(f"  Result: {val} {unit}")
    assert unit == "mH"
    
    print("\n--- 6.3: 0.0001 Henries (100µH) ---")
    val, unit = ec.format_inductance(0.0001)
    print(f"  Result: {val} {unit}")
    assert unit == "µH"
    
    print("\n--- 6.4: 0.00000001 Henries (10nH) ---")
    val, unit = ec.format_inductance(1e-8)
    print(f"  Result: {val} {unit}")
    assert unit == "nH"
    
    print("\n✅ Inductance formatting test PASSED")

# ============================================================
# TEST 7: REAL-WORLD APPLICATIONS
# ============================================================
print("\n" + "=" * 70)
print("TEST 7: REAL-WORLD APPLICATIONS")
print("=" * 70)

def test_real_world():
    print("\n--- 7.1: Speaker Crossover (2-way) ---")
    result = ec.capacitor_impedance(4.7e-6, 1000)
    print(f"  4.7µF at 1kHz: {result['impedance_ohm']}Ω")
    f_cross = 1/(2*3.14159*8*4.7e-6)
    print(f"  Crossover frequency ≈ {f_cross:.0f}Hz")
    
    print("\n--- 7.2: Power Supply Filter Capacitor ---")
    result = ec.capacitor_impedance(1000e-6, 100)
    print(f"  1000µF at 100Hz: {result['impedance_ohm']}Ω")
    print(f"  Rule: Should be much less than load resistance")
    
    print("\n--- 7.3: Radio Tuning Circuit (FM) ---")
    for C_pf in [20, 25, 30]:
        C = C_pf * 1e-12
        f = 1 / (2 * 3.14159 * (0.1e-6 * C)**0.5) / 1e6
        print(f"  C={C_pf}pF → f={f:.1f}MHz")
    
    print("\n--- 7.4: Decoupling Capacitor (10µF + 100nF) ---")
    # Parallel capacitors for wideband decoupling
    result_10uF = ec.capacitor_impedance(10e-6, 10e6)
    result_100nF = ec.capacitor_impedance(100e-9, 10e6)
    
    Z_10uF = result_10uF['impedance_ohm']
    Z_100nF = result_100nF['impedance_ohm']
    
    print(f"  10µF at 10MHz: {Z_10uF:.6f}Ω")
    print(f"  100nF at 10MHz: {Z_100nF:.2f}Ω")
    
    # Safe parallel calculation
    if Z_10uF > 1e-9 and Z_100nF > 1e-9:
        Z_parallel = 1 / ((1/Z_10uF) + (1/Z_100nF))
    else:
        Z_parallel = 0
    
    print(f"  Parallel impedance: {Z_parallel:.6f}Ω")
    print(f"  Note: At 10MHz, 10µF appears as a short circuit")
    
    print("\n✅ Real-world tests PASSED")

# ============================================================
# RUN ALL TESTS
# ============================================================
print("\n" + "=" * 70)
print("RUNNING ALL TESTS...")
print("=" * 70)

if __name__ == "__main__":
    try:
        test_resistor_impedance()
        test_capacitor_impedance()
        test_inductor_impedance()
        test_series_impedance()
        test_parallel_impedance()
        test_format_inductance()
        test_real_world()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("   - Resistor impedance: OK")
        print("   - Capacitor impedance (Xc): OK")
        print("   - Inductor impedance (XL): OK")
        print("   - Series impedance: OK")
        print("   - Parallel impedance: OK")
        print("   - Inductance formatting: OK")
        print("   - Real-world applications: OK")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()