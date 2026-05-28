# test_calculator.py
import sys
import math

sys.path.append('.')  # Add current directory to path

from App.core.ElectronicsCalculator import ElectronicsCalculator

def main():
    calc = ElectronicsCalculator()
    
    print("=" * 70)
    print("ELECTRONICS CALCULATOR - COMPLETE TEST SUITE")
    print("=" * 70)
    
    # ================================================================
    # TEST 1: Ohm's Law
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 1: Ohm's Law")
    print("=" * 70)
    
    result = calc.ohms_law(voltage=9, current=0.002)
    print(f"Ohm's Law (V=9, I=0.002): R = {result['resistance']} Ω")
    
    result = calc.ohms_law(voltage=9, resistance=470)
    print(f"Ohm's Law (V=9, R=470): I = {result['current']} A")
    
    result = calc.ohms_law(current=0.002, resistance=470)
    print(f"Ohm's Law (I=0.002, R=470): V = {result['voltage']} V")
    
    # ================================================================
    # TEST 2: Voltage Divider
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 2: Voltage Divider")
    print("=" * 70)
    
    result = calc.voltage_divider(Vcc=9, R1=100000, R2=22000)
    print(f"Voltage Divider (9V, 100k, 22k): Vout = {result['Vout']} V")
    
    # ================================================================
    # TEST 3: RC Cutoff Frequency
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 3: RC Cutoff Frequency")
    print("=" * 70)
    
    result = calc.rc_cutoff(R=10000, C=0.0000001)
    print(f"RC Cutoff (10kΩ, 100nF): f = {result['cutoff_freq_hz']} Hz")
    
    # ================================================================
    # TEST 4: Common Emitter BJT Amplifier
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 4: Common Emitter BJT Amplifier (9V, 2.2k, 470, 100k, 22k, β=200)")
    print("=" * 70)
    
    result = calc.common_emitter(
        Vcc=9, Rc=2200, Re=470, R1=100000, R2=22000, beta=200
    )
    print(f"Configuration: {result['configuration']}")
    print(f"Voltages: Vb={result['voltages']['Vb']}V, Ve={result['voltages']['Ve']}V, Vc={result['voltages']['Vc']}V")
    print(f"Currents: Ic={result['currents']['Ic_mA']}mA, Ib={result['currents']['Ib_uA']}µA")
    print(f"Gain: {result['gain']['approx']}x")
    print(f"Bias: {result['bias_status']}")
    
    # ================================================================
    # TEST 5: Common Base BJT Amplifier
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 5: Common Base BJT Amplifier (9V, 2.2k, 470, Vbias=1.6V, β=200)")
    print("=" * 70)
    
    result = calc.common_base(
        Vcc=9, Rc=2200, Re=470, Vbias=1.6, beta=200
    )
    print(f"Configuration: {result['configuration']}")
    print(f"Voltages: Vb={result['voltages']['Vb']}V, Ve={result['voltages']['Ve']}V, Vc={result['voltages']['Vc']}V")
    print(f"Gain: {result['gain']['approx']}x")
    print(f"Phase: {result['phase_shift']}")
    
    # ================================================================
    # TEST 6: Common Collector BJT Amplifier (Emitter Follower)
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 6: Common Collector BJT (9V, 470Ω, 100k, 22k, β=200)")
    print("=" * 70)
    
    result = calc.common_collector(
        Vcc=9, Re=470, R1=100000, R2=22000, beta=200
    )
    print(f"Configuration: {result['configuration']}")
    print(f"Voltages: Vb={result['voltages']['Vb']}V, Ve={result['voltages']['Ve']}V")
    print(f"Gain: {result['gain']['approx']}x")
    print(f"Input Z: {result['impedance']['Zin_ohm']}Ω, Output Z: {result['impedance']['Zout_ohm']}Ω")
    
    # ================================================================
    # TEST 7: Common Source MOSFET
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 7: Common Source MOSFET (12V, 2.2k, 100k, 22k, Vth=2.5V, K=0.05)")
    print("=" * 70)
    
    result = calc.common_source_mosfet(
        Vdd=12, Rd=2200, R1=100000, R2=22000, Vth=2.5, K=0.05
    )
    print(f"Configuration: {result['configuration']}")
    print(f"Voltages: Vg={result['voltages']['Vg']}V, Vd={result['voltages']['Vd']}V")
    print(f"Current: Id={result['currents']['Id_mA']}mA")
    print(f"Gain: {result['gain']['voltage_gain']}x, Region: {result['region']}")
    
    # ================================================================
    # TEST 8: LC Resonance
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 8: LC Resonance (L=100µH, C=100pF)")
    print("=" * 70)
    
    result = calc.lc_resonance(L=0.0001, C=0.0000000001)
    print(f"Frequency: {result['frequency']['value']} {result['frequency']['unit']}")
    print(f"  (Raw: {result['frequency']['hz']} Hz, {result['frequency']['khz']} kHz, {result['frequency']['mhz']} MHz)")
    
    # ================================================================
    # TEST 9: Colpitts Oscillator
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 9: Colpitts Oscillator (L=10µH, C1=100pF, C2=470pF)")
    print("=" * 70)
    
    result = calc.colpitts_frequency(L=0.00001, C1=0.0000000001, C2=0.00000000047)
    print(f"Frequency: {result['frequency']['value']} {result['frequency']['unit']}")
    print(f"C_total = {result['C_total']['pf']} pF")
    
    # ================================================================
    # TEST 10: Hartley Oscillator
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 10: Hartley Oscillator (L1=10µH, L2=10µH, C=100pF)")
    print("=" * 70)
    
    result = calc.hartley_frequency(L1=0.00001, L2=0.00001, C=0.0000000001)
    print(f"Frequency: {result['frequency']['value']} {result['frequency']['unit']}")
    print(f"L_total = {result['L_total']['uh']} µH")
    
    # ================================================================
    # TEST 11: 555 Astable (Forward)
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 11: 555 Astable (R1=10kΩ, R2=10kΩ, C=100nF)")
    print("=" * 70)
    
    result = calc.ne555_astable(R1=10000, R2=10000, C=0.0000001)
    print(f"Frequency: {result['frequency']['value']} {result['frequency']['unit']}")
    print(f"t_high = {result['timing']['t_high']['value']} {result['timing']['t_high']['unit']}")
    print(f"t_low = {result['timing']['t_low']['value']} {result['timing']['t_low']['unit']}")
    print(f"Duty cycle: {result['duty_cycle_percent']}%")
    
    # ================================================================
    # TEST 12: 555 Astable Inverse (Get components)
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 12: 555 Astable Inverse (f=1kHz, get components)")
    print("=" * 70)
    
    # First get suggestion
    result = calc.ne555_astable_inverse(target_freq_hz=1000)
    print(f"Suggestion: {result['suggestion']['message']}")
    print(f"Recommended C = {result['suggestion']['recommended_C_uF']} µF")
    
    # Then with C provided
    result = calc.ne555_astable_inverse(target_freq_hz=1000, C=0.0000001)
    print(f"Recommended: R1={result['recommended']['R1_kohm']}kΩ, R2={result['recommended']['R2_kohm']}kΩ")
    print(f"Resulting frequency: {result['resulting_frequency']['value']} {result['resulting_frequency']['unit']}")
    print(f"Resulting duty cycle: {result['resulting_duty_cycle']}%")
    
    # ================================================================
    # TEST 13: Unit Conversion
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 13: Unit Conversion")
    print("=" * 70)
    
    result = calc.convert_resistance(2.2, 'k', 'ohm')
    print(f"2.2kΩ = {result} Ω")
    
    result = calc.convert_resistance(2200, 'ohm', 'k')
    print(f"2200Ω = {result} kΩ")
    
    result = calc.convert_capacitance(100, 'n', 'f')
    print(f"100nF = {result} F")
    
    result = calc.convert_capacitance(0.0000001, 'f', 'n')
    print(f"0.0000001F = {result} nF")
    
    # ================================================================
    # TEST 14: Frequency Formatter
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 14: Frequency Formatter")
    print("=" * 70)
    
    test_freqs = [50, 1000, 2500000, 1000000000]
    for f in test_freqs:
        result = calc._format_frequency(f)
        print(f"{f} Hz → {result['value']} {result['unit']}")
    
    # ================================================================
    # TEST 15-18: KVL/KCL/Voltage Divider
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 15: KVL Series Circuit (9V, R1=1k, R2=2.2k, R3=470)")
    print("=" * 70)

    result = calc.kvl_series_circuit(Vsupply=9, resistors=[1000, 2200, 470])
    print(f"Supply: {result['supply_voltage']}V")
    print(f"Total current: {result['total_current']['milliamperes']} mA")
    print("Voltage drops:")
    for v in result['voltage_drops']:
        print(f"  {v['resistor']} ({v['resistance_ohm']}Ω): {v['voltage_v']}V")
    print(f"KVL verified: {result['kvl_check']['verified']}")
    print(f"Total power: {result['total_power_mw']} mW")

    print("\n" + "=" * 70)
    print("TEST 16: KVL with Load (9V, R1=1k, R2=1k, Load=10k at end)")
    print("=" * 70)

    result = calc.kvl_with_load(Vsupply=9, R_load=10000, resistors=[1000, 1000], load_position=-1)
    print(f"Load voltage: {result['load_info']['load_voltage_v']}V ({result['load_info']['load_voltage_percent']}% of supply)")
    print(f"Load power: {result['load_info']['load_power_mw']} mW")

    print("\n" + "=" * 70)
    print("TEST 17: KCL Parallel Circuit (9V, Branches: 470Ω, 1kΩ, 2.2kΩ)")
    print("=" * 70)

    result = calc.kvl_parallel_branch(Vsupply=9, branch_resistors=[470, 1000, 2200])
    print(f"Total current: {result['total_current_ma']} mA")
    for branch in result['branch_currents']:
        print(f"  Branch {branch['branch']} ({branch['resistance_ohm']}Ω): {branch['current_ma']} mA")
    print(f"KCL verified: {result['kcl_check']['verified']}")

    print("\n" + "=" * 70)
    print("TEST 18: Voltage Divider (9V, R1=10k, R2=10k, No Load vs 10k Load)")
    print("=" * 70)

    result = calc.voltage_divider_load(Vcc=9, R1=10000, R2=10000)
    print(f"No load: Vout = {result['output_voltage']}V, I_total = {result['currents']['I_R1_mA']} mA")
    result = calc.voltage_divider_load(Vcc=9, R1=10000, R2=10000, R_load=10000)
    print(f"With 10k load: Vout = {result['output_voltage']}V, I_load = {result['currents']['I_load_mA']} mA")
    print(f"R2 effective: {result['effective_resistance']['R2_effective_kohm']} kΩ")

    # ================================================================
    # POWER SUPPLY & RECTIFIER TESTS
    # ================================================================
    print("\n" + "=" * 60)
    print("TEST 19: Half-Wave Rectifier (220V AC, 100mA, 500mV ripple)")
    print("=" * 60)

    result = calc.half_wave_rectifier(vrms=220, load_ma=100, ripple_mv=500)
    print(f"Vpeak: {result['input']['vpeak_v']}V")
    print(f"Vdc (no load): {result['output']['vdc_no_load_v']}V")
    print(f"Capacitor voltage rating: {result['capacitor_rating']['recommended_voltage_v']}V")
    if 'ripple_calculation' in result:
        print(f"Required capacitance: {result['ripple_calculation']['required_capacitance']['value']} {result['ripple_calculation']['required_capacitance']['unit']}")

    print("\n" + "=" * 60)
    print("TEST 20: Full-Wave Rectifier (220V AC, 100mA, 500mV ripple)")
    print("=" * 60)

    result = calc.full_wave_rectifier(vrms=220, load_ma=100, ripple_mv=500)
    print(f"Vpeak: {result['input']['vpeak_v']}V")
    print(f"Vdc (with diode drop): {result['output']['vdc_with_diode_drop_v']}V")
    print(f"Capacitor voltage rating: {result['capacitor_rating']['recommended_voltage_v']}V")
    print(f"Ripple frequency: {result['output']['ripple_frequency_hz']}Hz")
    if 'ripple_calculation' in result:
        print(f"Required capacitance: {result['ripple_calculation']['required_capacitance']['value']} {result['ripple_calculation']['required_capacitance']['unit']}")

    print("\n" + "=" * 60)
    print("TEST 21: Diode Selection (220V AC, 500mA load)")
    print("=" * 60)

    result = calc.diode_selection(vrms=220, load_ma=500)
    print(f"Min PIV required: {result['input']['min_piv_v']}V")
    print(f"Recommended diode: {result['recommended_diode']['name']} ({result['recommended_diode']['piv_v']}V, {result['recommended_diode']['current_a']}A)")

    print("\n" + "=" * 60)
    print("TEST 22: Capacitor Filter (100mA load, 500mV ripple, full-wave)")
    print("=" * 60)

    result = calc.capacitor_filter_calculator(load_ma=100, ripple_mv=500, voltage_v=12)
    print(f"Required capacitance: {result['calculated']['required_capacitance']['value']} {result['calculated']['required_capacitance']['unit']}")
    print(f"Recommended: {result['recommendations']['capacitor_uf']}µF")
    print(f"Actual ripple: {result['recommendations']['actual_ripple_mv']}mV")

    print("\n" + "=" * 60)
    print("TEST 23: Ripple Calculator (100mA load, 1000µF cap, full-wave)")
    print("=" * 60)

    result = calc.ripple_calculator(load_ma=100, capacitor_uf=1000)
    print(f"Ripple: {result['ripple']['voltage_mv']}mV")
    print(f"Quality: {result['quality']}")

    print("\n" + "=" * 60)
    print("TEST 24: Zener Regulator (12V to 5.1V, 50mA load)")
    print("=" * 60)

    result = calc.zener_regulator(vin=12, vz=5.1, i_load_ma=50)
    print(f"Input: {result['input']['voltage_v']}V → {result['input']['zener_voltage_v']}V")
    print(f"Series resistor: {result['series_resistor']['recommended_ohm']}Ω, {result['series_resistor']['use_wattage']}")
    print(f"Zener current: {result['zener_diode']['current_ma']}mA")
    print(f"Zener power: {result['zener_diode']['power_mw']}mW")
    print(f"Zener safe: {result['zener_diode']['safe']}")
    print(f"Max load current: {result['output']['max_current_ma']}mA")

    # ================================================================
    # NEW OP-AMP TESTS
    # ================================================================
    print("\n" + "=" * 70)
    print("NEW TEST 25: Op-Amp Inverting Amplifier (Rf=10k, Rin=1k)")
    print("=" * 70)
    
    result = calc.opamp_inverting(Rf=10000, Rin=1000)
    print(f"Gain: {result['gain']['ratio']}x ({result['gain']['db']}dB)")
    print(f"Output for 1V input: {result['output_for_1v_input_v']}V")
    print(f"Phase: {result['phase_shift']}")
    
    print("\n" + "=" * 70)
    print("NEW TEST 26: Op-Amp Non-Inverting Amplifier (Rf=9k, Rg=1k)")
    print("=" * 70)
    
    result = calc.opamp_non_inverting(Rf=9000, Rg=1000)
    print(f"Gain: {result['gain']['ratio']}x")
    print(f"Output for 1V input: {result['output_for_1v_input_v']}V")
    
    print("\n" + "=" * 70)
    print("NEW TEST 27: Op-Amp Voltage Follower (Buffer)")
    print("=" * 70)
    
    result = calc.opamp_buffer()
    print(f"Gain: {result['gain']['ratio']}x")
    print(f"Input Z: {result['input_impedance']}, Output Z: {result['output_impedance']}")
    
    print("\n" + "=" * 70)
    print("NEW TEST 28: Op-Amp Summing Amplifier (V1=1V, V2=0.5V, R1=R2=Rf=10k)")
    print("=" * 70)
    
    result = calc.opamp_summing(V_inputs=[1, 0.5], R_inputs=[10000, 10000], Rf=10000)
    print(f"Output voltage: {result['output_voltage_v']}V")
    print(f"Formula: {result['formula']}")
    
    print("\n" + "=" * 70)
    print("NEW TEST 29: Op-Amp Differential Amplifier (V1=1V, V2=1.5V, all resistors 10k)")
    print("=" * 70)
    
    result = calc.opamp_differential(V1=1, V2=1.5, R1=10000, R2=10000, R3=10000, R4=10000)
    print(f"Output voltage: {result['output_voltage_v']}V")
    print(f"Gain: {result['gain']}x")
    
    print("\n" + "=" * 70)
    print("NEW TEST 30: Op-Amp Comparator (Vref=2.5V, Vsense=3V)")
    print("=" * 70)
    
    result = calc.opamp_comparator(Vref=2.5, Vsense=3)
    print(f"Output: {result['output_state']} ({result['output_voltage_v']}V)")
    
    print("\n" + "=" * 70)
    print("NEW TEST 31: Schmitt Trigger (Vcc=12V, R1=10k, R2=100k)")
    print("=" * 70)
    
    result = calc.opamp_schmitt_trigger(Vcc=12, R1=10000, R2=100000)
    print(f"Upper threshold: {result['thresholds']['upper_v']}V")
    print(f"Lower threshold: {result['thresholds']['lower_v']}V")
    print(f"Hysteresis: {result['thresholds']['hysteresis_v']}V")
    
    # ================================================================
    # NEW AC CIRCUITS TESTS
    # ================================================================
    print("\n" + "=" * 70)
    print("NEW TEST 32: Capacitive Reactance (f=50Hz, C=100µF)")
    print("=" * 70)
    
    result = calc.ac_capacitive_reactance(f_hz=50, C_f=0.0001)
    print(f"Xc = {result['reactance_ohm']}Ω")
    
    print("\n" + "=" * 70)
    print("NEW TEST 33: Inductive Reactance (f=50Hz, L=100mH)")
    print("=" * 70)
    
    result = calc.ac_inductive_reactance(f_hz=50, L_h=0.1)
    print(f"XL = {result['reactance_ohm']}Ω")
    
    print("\n" + "=" * 70)
    print("NEW TEST 34: Series RLC Impedance (R=100Ω, L=10mH, C=100µF, f=50Hz)")
    print("=" * 70)
    
    result = calc.ac_series_rlc(R=100, L_h=0.01, C_f=0.0001, f_hz=50)
    print(f"XL = {result['reactances']['xl_ohm']}Ω, XC = {result['reactances']['xc_ohm']}Ω")
    print(f"Impedance Z = {result['impedance_ohm']}Ω")
    print(f"Phase angle = {result['phase_angle_deg']}°")
    print(f"Power factor = {result['power_factor']}")
    
    print("\n" + "=" * 70)
    print("NEW TEST 35: Resonant Frequency (L=10mH, C=100µF)")
    print("=" * 70)
    
    result = calc.ac_resonant_frequency(L_h=0.01, C_f=0.0001)
    print(f"f0 = {result['resonant_frequency']['value']} {result['resonant_frequency']['unit']}")
    
    print("\n" + "=" * 70)
    print("NEW TEST 36: Q Factor (R=100Ω, L=10mH, C=100µF)")
    print("=" * 70)
    
    result = calc.ac_q_factor(R=100, L_h=0.01, C_f=0.0001, f_hz=50)
    print(f"Q (series) = {result['q_factor_series']}")
    print(f"Q (parallel) = {result['q_factor_parallel']}")
    
    # ================================================================
    # NEW FILTER TESTS
    # ================================================================
    print("\n" + "=" * 70)
    print("NEW TEST 37: RC Low-pass Filter (R=1kΩ, C=100nF)")
    print("=" * 70)
    
    result = calc.filter_rc_lowpass(R=1000, C=0.0000001)
    print(f"Cutoff frequency: {result['cutoff_frequency']['value']} {result['cutoff_frequency']['unit']}")
    
    print("\n" + "=" * 70)
    print("NEW TEST 38: RC High-pass Filter (R=1kΩ, C=100nF)")
    print("=" * 70)
    
    result = calc.filter_rc_highpass(R=1000, C=0.0000001)
    print(f"Cutoff frequency: {result['cutoff_frequency']['value']} {result['cutoff_frequency']['unit']}")
    
    print("\n" + "=" * 70)
    print("NEW TEST 39: Band-pass Filter (f0=1kHz, Q=10)")
    print("=" * 70)
    
    result = calc.filter_bandpass(f_center_hz=1000, Q=10)
    print(f"Bandwidth: {result['bandwidth_hz']}Hz")
    print(f"Lower cutoff: {result['cutoff_frequencies']['lower_hz']}Hz")
    print(f"Upper cutoff: {result['cutoff_frequencies']['upper_hz']}Hz")
    
    print("\n" + "=" * 70)
    print("NEW TEST 40: Notch Filter (f0=1kHz, Q=10)")
    print("=" * 70)
    
    result = calc.filter_notch(f_notch_hz=1000, Q=10)
    print(f"Rejection bandwidth: {result['rejection_bandwidth_hz']}Hz")
    print(f"Rejection range: {result['rejection_range']['lower_hz']}Hz - {result['rejection_range']['upper_hz']}Hz")
    
    # ================================================================
    # NEW RF & COMMUNICATION TESTS
    # ================================================================
    print("\n" + "=" * 70)
    print("NEW TEST 41: Antenna Length (100MHz, Quarter-wave)")
    print("=" * 70)
    
    result = calc.rf_antenna_length(frequency_hz=100000000, wavelength_type="quarter")
    print(f"Wavelength: {result['wavelength']['meters']}m")
    print(f"Antenna length: {result['antenna_length']['cm']}cm")
    
    print("\n" + "=" * 70)
    print("NEW TEST 42: dB Conversion (1W to dBm)")
    print("=" * 70)
    
    result = calc.rf_db_conversion(power_w=1)
    print(f"1W = {result['dbm']} dBm = {result['power_mw']} mW")
    
    print("\n" + "=" * 70)
    print("NEW TEST 43: AM Modulation (Carrier=5V, Modulating=2.5V)")
    print("=" * 70)
    
    result = calc.rf_am_modulation(carrier_amplitude=5, modulating_amplitude=2.5)
    print(f"Modulation index: {result['modulation_index']} ({result['modulation_percent']}%)")
    print(f"Status: {result['status']}")
    
    print("\n" + "=" * 70)
    print("NEW TEST 44: FM Deviation (Δf=75kHz, fm=15kHz)")
    print("=" * 70)
    
    result = calc.rf_fm_deviation(deviation_hz=75000, modulating_freq_hz=15000)
    print(f"Modulation index: {result['modulation_index']}")
    print(f"Bandwidth: {result['bandwidth_khz']}kHz")
    
    print("\n" + "=" * 70)
    print("NEW TEST 45: Link Budget (2.4GHz, 1km, 20dBm TX, 2dBi antennas)")
    print("=" * 70)
    
    result = calc.rf_link_budget(
        tx_power_dbm=20, tx_gain_dbi=2, rx_gain_dbi=2,
        distance_km=1, frequency_mhz=2400, rx_sensitivity_dbm=-90,
        cable_loss_db=0, fade_margin_db=10
    )
    print(f"Free space path loss: {result['free_space_path_loss_db']}dB")
    print(f"Received power: {result['received_power_dbm']}dBm")
    print(f"Link margin: {result['link_margin_db']}dB")
    print(f"Feasibility: {result['feasibility']}")

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED - 45 TESTS TOTAL")
    print("=" * 70)
### Battery test

    # ================================================================
    # TEST BATTERY FUNCTIONS
    # ================================================================
    print("\n" + "=" * 70)
    print("BATTERY TESTS")
    print("=" * 70)

    # Test 1: Single cell
    print("\n1. Single Cell (1S) - Li-ion 2000mAh")
    result = calc.battery_configuration(cell_capacity_mah=2000, series_count=1, parallel_count=1)
    print(f"   {result['pack_specs']['voltage_nominal_v']}V, {result['pack_specs']['capacity_mah']}mAh, {result['pack_specs']['energy_wh']}Wh")

    # Test 2: 3S (series)
    print("\n2. Series (3S) - Li-ion 2000mAh")
    result = calc.battery_configuration(cell_capacity_mah=2000, series_count=3, parallel_count=1)
    print(f"   {result['pack_specs']['voltage_nominal_v']}V, {result['pack_specs']['capacity_mah']}mAh")

    # Test 3: 1S2P (parallel)
    print("\n3. Parallel (1S2P) - Li-ion 2000mAh")
    result = calc.battery_configuration(cell_capacity_mah=2000, series_count=1, parallel_count=2)
    print(f"   {result['pack_specs']['voltage_nominal_v']}V, {result['pack_specs']['capacity_mah']}mAh")

    # Test 4: 3S2P (series-parallel)
    print("\n4. Series-Parallel (3S2P) - Li-ion 2000mAh")
    result = calc.battery_configuration(cell_capacity_mah=2000, series_count=3, parallel_count=2)
    print(f"   {result['pack_specs']['voltage_nominal_v']}V, {result['pack_specs']['capacity_mah']}mAh, {result['pack_specs']['energy_wh']}Wh")

    # Test 5: All configurations for 4 cells
    print("\n5. All Configurations for 4 Cells (2000mAh Li-ion)")
    result = calc.battery_all_configurations(cell_voltage_v=3.7, cell_capacity_mah=2000, cells_available=4, load_ma=200)
    print(f"   Cells: {result['cells_available']}, Load: {result['load_ma']}mA")
    for cfg in result['configurations']:
        print(f"   {cfg['name']:12} → {cfg['voltage_v']}V, {cfg['capacity_mah']}mAh, {cfg['runtime_hours']}h runtime")
    print(f"   Recommendation: {result['recommendation']}")

    # Test 6: Compare battery types
    print("\n6. Compare Battery Types (3S, 2000mAh)")
    result = calc.battery_compare_all_types(cell_capacity_mah=2000, series_count=3, parallel_count=1)
    for comp in result['comparison'][:4]:
        print(f"   {comp['type']:25} → {comp['voltage_v']}V, {comp['energy_wh']}Wh")
    print(f"   Recommendation: {result['recommendation']}")

    # Test 7: Voltage by type
    print("\n7. Voltage Ranges (4S)")
    for batt_type in ["li-ion", "lifepo4", "lead_acid", "nimh"]:
        result = calc.battery_voltage_by_type(battery_type=batt_type, cells_in_series=4)
        print(f"   {batt_type.upper()}: {result['nominal_voltage_v']}V nom, {result['full_voltage_v']}V full, {result['cutoff_voltage_v']}V cutoff")

    # Test 8: Runtime with load
    print("\n8. Runtime Calculation (3S2P, 2000mAh cells, 500mA load)")
    result = calc.battery_configuration(cell_capacity_mah=2000, series_count=3, parallel_count=2, load_ma=500)
    print(f"   Runtime: {result['runtime']['hours']} hours at 500mA")
    print(f"   Max discharge: {result['pack_specs']['max_discharge_a']}A")


    # ================================================================
    # TEST SOLAR PANEL FUNCTIONS
    # ================================================================
    print("\n" + "=" * 70)
    print("SOLAR PANEL CALCULATIONS")
    print("=" * 70)

    # Test 1: Solar panel specifications
    print("\n1. Solar Panel Specs (100W panel typical values)")
    result = calc.solar_panel_specs(voc=22.5, isc=5.8, vmp=18.5, imp=5.4)
    print(f"   Vmp: {result['specifications']['vmp_v']}V")
    print(f"   Imp: {result['specifications']['imp_a']}A")
    print(f"   Power: {result['specifications']['pmp_w']}Wp")

    # Test 2: Multiple panels in series (for higher voltage)
    print("\n2. Two 100W panels in SERIES (for 24V system)")
    panels = [{"vmp": 18.5, "imp": 5.4}, {"vmp": 18.5, "imp": 5.4}]
    result = calc.solar_parallel_series(panels=panels, connection="series")
    print(f"   Total voltage: {result['total_vmp_v']}V")
    print(f"   Total power: {result['total_pmp_w']}W")

    # Test 3: Solar charge time for 12V 100Ah battery
    print("\n3. Solar Charge Time (100W panel → 12V 100Ah lead acid battery)")
    result = calc.solar_charge_time(panel_w=100, battery_voltage_v=12, 
                                    battery_capacity_ah=100, battery_type="lead_acid")
    print(f"   Hours needed: {result['charge_time']['hours_direct_sun']}h")
    print(f"   Days average: {result['charge_time']['days_average']} days")

    # Test 4: Solar panel for daily load
    print("\n4. Solar System Sizing (500Wh daily load, 12V system)")
    result = calc.solar_panel_for_load(daily_load_wh=500, battery_voltage_v=12)
    print(f"   Battery needed: {result['battery']['recommended_ah']}Ah")
    print(f"   Panel needed: {result['solar_panel']['required_wp']}Wp")

    # Test 5: Daily production
    print("\n5. Daily Production (100W panel, 5 sun hours)")
    result = calc.solar_panel_vs_battery(panel_w=100, sun_hours=5)
    print(f"   Daily: {result['daily_energy_wh']}Wh")
    print(f"   Can run LED bulb: {result['can_run_devices_for_hours']['LED Bulb (10W)']:.0f} hours")

 
    print("=" * 70)
    print(" TOROID INDUCTOR CALCULATOR TEST SUITE")
    print("=" * 70)

    # ================================================================
    # TEST 1: Core Properties
    # ================================================================
    print("\n📐 TEST 1: Core Physical Properties")
    print("-" * 50)

    # T50-52 toroid core (common for filters)
    od = 12.7      # mm
    id = 7.7       # mm  
    ht = 4.8       # mm

    core = calc.toroid_core_properties(od, id, ht)
    print(f"Core dimensions: OD={od}mm, ID={id}mm, Ht={ht}mm")
    print(f"  Mean path length: {core['magnetic_path']['mean_path_length_mm']} mm")
    print(f"  Cross-sectional area: {core['magnetic_path']['cross_sectional_area_mm2']} mm²")
    print(f"  Core constant: {core['magnetic_path']['core_constant_mm1']} mm⁻¹")

    # ================================================================
    # TEST 2: A_L (Inductance Factor)
    # ================================================================
    print("\n📐 TEST 2: A_L (Inductance Factor) Calculation")
    print("-" * 50)

    # Material 52 (Iron powder) has µr ≈ 75
    permeability = 75
    al = calc.toroid_al_factor(permeability, od, id, ht)
    print(f"Material permeability (µr): {permeability}")
    print(f"  A_L = {al['al_value_nh_per_turn2']} nH/N²")
    print(f"  Formula: {al['formula']}")

    # ================================================================
    # TEST 3: Inductance for given turns
    # ================================================================
    print("\n📐 TEST 3: Inductance for Given Number of Turns")
    print("-" * 50)

    turns_list = [10, 20, 30, 40, 50]
    for turns in turns_list:
        L = calc.toroid_inductance(turns, permeability, od, id, ht)
        print(f"  {turns:2d} turns → {L['inductance']['microhenry']} µH")

    # ================================================================
    # TEST 4: Turns needed for target inductance
    # ================================================================
    print("\n📐 TEST 4: Turns Required for Target Inductance")
    print("-" * 50)

    targets = [10, 22, 47, 100, 220]
    for target in targets:
        result = calc.toroid_turns_for_target(target, permeability, od, id, ht)
        print(f"  Target {target:3d} µH → {result['recommended_turns']:2d} turns (actual: {result['actual_inductance_uh']:.1f} µH, error: {result['error_percent']:.1f}%)")

    # ================================================================
    # TEST 5: Wire length calculation
    # ================================================================
    print("\n📐 TEST 5: Wire Length Calculation")
    print("-" * 50)

    turns = 25
    wire_len = calc.toroid_wire_length(turns, od, id)
    print(f"  {turns} turns on T50 core")
    print(f"  Length per turn: {wire_len['length_per_turn']['mm']:.1f} mm")
    print(f"  Total wire needed: {wire_len['total_length']['m']:.2f} meters")
    print(f"  Total wire needed: {wire_len['total_length']['inches']:.1f} inches")

    # ================================================================
    # TEST 6: Maximum turns (winding limit)
    # ================================================================
    print("\n📐 TEST 6: Maximum Turns (Winding Limit)")
    print("-" * 50)

    wire_diameters = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]  # mm
    print(f"Inner diameter: {id} mm")
    for wd in wire_diameters:
        max_t = calc.toroid_max_turns(id, wd, fill_factor=0.3)
        print(f"  Wire {wd:.1f}mm → max {max_t['practical_max_turns']} turns (theoretical: {max_t['theoretical_max_turns']:.0f})")
        print(f"      {max_t['warning']}")

    # ================================================================
    # TEST 7: Complete inductor design
    # ================================================================
    print("\n📐 TEST 7: Complete Inductor Design")
    print("-" * 50)

    # Design a 47 µH inductor
    design = calc.toroid_inductor_design(
        target_uh=47,
        core_permeability=75,
        od_mm=od,
        id_mm=id,
        ht_mm=ht,
        wire_diameter_mm=0.5
    )

    print(f"Target inductance: {design['target_inductance_uh']} µH")
    print(f"Core dimensions: OD={od}mm, ID={id}mm, Ht={ht}mm")
    print(f"Required turns: {design['turns_required']['recommended_turns']}")
    print(f"Actual inductance: {design['achieved_inductance']['inductance']['microhenry']} µH")
    print(f"Error: {design['turns_required']['error_percent']}%")

    if 'wire_info' in design:
        print(f"Wire length needed: {design['wire_info']['total_length']['m']:.2f} m")
        print(f"Feasibility: {design['feasibility']}")

    # ================================================================
    # TEST 8: Core selector (find material for given L and N)
    # ================================================================
    print("\n📐 TEST 8: Core Material Selector")
    print("-" * 50)

    # You want 100 µH with 20 turns
    selector = calc.toroid_core_selector(target_uh=100, turns=20)
    print(f"Target: 100 µH with 20 turns")
    print(f"Required permeability: {selector['required_permeability_mu']}")
    print(f"Recommended material: {selector['recommended_material']['name']} (µ={selector['recommended_material']['mu']})")
    print(f"  Use: {selector['recommended_material']['use']}")

    # ================================================================
    # TEST 9: Common core examples
    # ================================================================
    print("\n📐 TEST 9: Common Toroid Core Examples")
    print("-" * 50)

    cores = [
        {"name": "T37-6", "od": 9.5, "id": 4.7, "ht": 3.2, "mu": 8.5, "desc": "RF inductor"},
        {"name": "T50-52", "od": 12.7, "id": 7.7, "ht": 4.8, "mu": 75, "desc": "Power filter"},
        {"name": "T80-26", "od": 20.3, "id": 12.6, "ht": 6.4, "mu": 75, "desc": "High current"},
        {"name": "FT82-43", "od": 21.0, "id": 13.5, "ht": 6.5, "mu": 850, "desc": "EMI suppression"},
        {"name": "FT50-77", "od": 12.7, "id": 7.7, "ht": 4.8, "mu": 2000, "desc": "Power transformer"},
    ]

    for core in cores:
        al_val = calc.toroid_al_factor(core["mu"], core["od"], core["id"], core["ht"])
        L_10 = calc.toroid_inductance(10, core["mu"], core["od"], core["id"], core["ht"])
        L_20 = calc.toroid_inductance(20, core["mu"], core["od"], core["id"], core["ht"])
        print(f"\n  {core['name']} ({core['desc']})")
        print(f"    A_L = {al_val['al_value_nh_per_turn2']:.1f} nH/N²")
        print(f"    10 turns → {L_10['inductance']['microhenry']:.1f} µH")
        print(f"    20 turns → {L_20['inductance']['microhenry']:.1f} µH")

    # ================================================================
    # TEST 10: Different wire size comparison
    # ================================================================
    print("\n📐 TEST 10: Wire Size Comparison for 25 Turns")
    print("-" * 50)

    turns = 25
    wire_sizes = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]
    print(f"Turns: {turns}\n")

    for wd in wire_sizes:
        max_t = calc.toroid_max_turns(id, wd, fill_factor=0.3)
        if turns <= max_t["practical_max_turns"]:
            status = "✅ OK"
        else:
            status = "❌ Too many turns"
        print(f"  Wire {wd:.1f}mm: max {max_t['practical_max_turns']:2d} turns → {turns} turns is {status}")

    # ================================================================
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 70)

    # Summary
    print("\n📊 SUMMARY TABLE")
    print("-" * 50)
    print(f"{'Turns':<8} {'Inductance (µH)':<18} {'Wire length (m)':<16} {'Fill factor':<12}")
    print("-" * 50)

    for turns in [10, 20, 30, 40, 50]:
        L = calc.toroid_inductance(turns, permeability, od, id, ht)
        wire = calc.toroid_wire_length(turns, od, id)
        max_t = calc.toroid_max_turns(id, 0.5, 0.3)
        fill = turns / max_t["practical_max_turns"]
        print(f"{turns:<8} {L['inductance']['microhenry']:<18.2f} {wire['total_length']['m']:<16.2f} {fill:<12.2f}")


    # ================================================================
    # TRANSFORMER CALCULATIONS
    # ================================================================
 

    print("=" * 80)
    print(" TRANSFORMER CALCULATOR TEST SUITE")
    print("=" * 80)

    # ================================================================
    # TEST 1: Voltage Ratio (Turns Ratio)
    # ================================================================
    print("\n📐 TEST 1: Voltage Ratio (Turns Ratio)")
    print("-" * 50)

    print("Case 1: Given turns, calculate secondary voltage")
    result = calc.transformer_voltage_ratio(Np=1000, Ns=100, Vp=230)
    print(f"  1000:100 turns, 230V primary → {result['secondary_voltage_v']}V secondary")
    print(f"  Type: {result['type']}")
    print(f"  Formula: {result.get('formula', 'N/A')}")

    print("\nCase 2: Given voltages, calculate required turns")
    result = calc.transformer_voltage_ratio(Np=1000, Ns=100, Vs=12)
    print(f"  1000:100 turns, 12V secondary → {result['primary_voltage_v']}V primary")

    # ================================================================
    # TEST 2: Current Ratio
    # ================================================================
    print("\n📐 TEST 2: Current Ratio")
    print("-" * 50)

    result = calc.transformer_current_ratio(Np=1000, Ns=100, Ip=2)
    print(f"  1000:100 turns, 2A primary → {result['secondary_current_a']}A secondary")
    print(f"  Formula: {result.get('formula', 'N/A')}")

    result = calc.transformer_current_ratio(Np=1000, Ns=100, Is=20)
    print(f"  1000:100 turns, 20A secondary → {result['primary_current_a']}A primary")

    # ================================================================
    # TEST 3: Impedance Transformation
    # ================================================================
    print("\n📐 TEST 3: Impedance Transformation")
    print("-" * 50)

    print("Case 1: 8Ω speaker on secondary, what impedance on primary?")
    result = calc.transformer_impedance(Np=1000, Ns=100, Z_secondary=8)
    print(f"  1000:100 turns, 8Ω load → {result['primary_reflected_impedance_ohm']}Ω primary")
    print(f"  Impedance ratio: {result['impedance_ratio']}:1")
    print(f"  Formula: {result.get('formula', 'N/A')}")

    print("\nCase 2: Tube amp wants 5000Ω load, what secondary for 8Ω speaker?")
    result = calc.transformer_impedance(Np=1000, Ns=100, Z_primary=5000)
    print(f"  1000:100 turns, 5000Ω source → {result['secondary_reflected_impedance_ohm']}Ω secondary")

    # ================================================================
    # TEST 4: Power Calculations
    # ================================================================
    print("\n📐 TEST 4: Power Calculations")
    print("-" * 50)

    result = calc.transformer_power(Vp=230, Ip=0.217, Vs=12, Is=4.17)
    print(f"  Primary: 230V × 0.217A = {result.get('primary_power_w', 'N/A')}W")
    print(f"  Secondary: 12V × 4.17A = {result.get('secondary_power_w', 'N/A')}W")
    print(f"  Efficiency: {result.get('calculated_efficiency_percent', 'N/A')}%")

    # ================================================================
    # TEST 5: Wire Size Calculator
    # ================================================================
    print("\n📐 TEST 5: Wire Size Calculator")
    print("-" * 50)

    for current in [0.5, 1, 2, 5, 10]:
        result = calc.transformer_wire_size(current, current_density=3.0)
        print(f"  {current}A → {result['wire_diameter_mm']}mm (AWG {result['approx_awg']})")

    # ================================================================
    # TEST 6: Turns Calculation for Core
    # ================================================================
    print("\n📐 TEST 6: Turns Calculation for Core")
    print("-" * 50)

    print("50Hz mains transformer, 230V primary, 10cm² core:")
    result = calc.transformer_turns_calculation(voltage=230, Ae_cm2=10, frequency_hz=50, B_max_tesla=1.2)
    print(f"  Required primary turns: {result['required_turns']}")
    print(f"  Turns per volt: {result['turns_per_volt']}")
    print(f"  Formula: {result['formula']}")

    print("\n400Hz aircraft transformer, 115V primary, 5cm² core:")
    result = calc.transformer_turns_calculation(voltage=115, Ae_cm2=5, frequency_hz=400, B_max_tesla=1.0)
    print(f"  Required primary turns: {result['required_turns']}")
    print(f"  Turns per volt: {result['turns_per_volt']}")

    # ================================================================
    # TEST 7: Complete Transformer Design
    # ================================================================
    print("\n📐 TEST 7: Complete Transformer Design")
    print("-" * 50)

    print("Design a 230V to 12V, 50VA mains transformer:")
    design = calc.transformer_design(Vp=230, Vs=12, Power_VA=50, frequency_hz=50, J_A_per_mm2=3.0, Ae_cm2=10)
    print(f"  Turns ratio: {design['specifications']['turns_ratio']} ({design['specifications']['type']})")
    print(f"  Primary current: {design['currents']['primary_a']}A")
    print(f"  Secondary current: {design['currents']['secondary_a']}A")
    print(f"  Primary turns: {design['windings']['primary_turns']}")
    print(f"  Secondary turns: {design['windings']['secondary_turns']}")
    print(f"  Primary wire: {design['windings']['primary_wire_mm']}mm (AWG {design['windings']['primary_awg']})")
    print(f"  Secondary wire: {design['windings']['secondary_wire_mm']}mm (AWG {design['windings']['secondary_awg']})")
    print(f"  Turns per volt: {design['core']['turns_per_volt']}")

    # ================================================================
    # TEST 8: Center-Tapped Transformer
    # ================================================================
    print("\n📐 TEST 8: Center-Tapped Transformer")
    print("-" * 50)

    result = calc.transformer_center_tap(V_secondary_total=24, Np=1000, Ns_total=100)
    print(f"  Secondary total: {result['secondary_total_voltage_v']}V (end-to-end)")
    print(f"  Center-tap voltage: {result['center_tap_voltage_v']}V (to either end)")
    print(f"  Secondary half turns: {result['secondary_half_turns']}")
    print(f"  Formula: {result['formula']}")

    # ================================================================
    # TEST 9: Real-World Examples
    # ================================================================
    print("\n📐 TEST 9: Real-World Transformer Examples")
    print("-" * 50)

    examples = calc.transformer_example_designs()
    for name, params in examples.items():
        print(f"\n  {name.upper().replace('_', ' ')}:")
        print(f"    {params.get('description', 'No description')}")
        if 'Vp' in params:
            print(f"    {params.get('Vp')}V → {params.get('Vs')}V, {params.get('Power_VA')}VA")

    # ================================================================
    # TEST 10: Impedance Matching for Audio
    # ================================================================
    print("\n📐 TEST 10: Audio Impedance Matching")
    print("-" * 50)

    print("Tube amp (8kΩ) to 8Ω speaker:")
    # Calculate required turns ratio
    Z_ratio = 8000 / 8
    turns_ratio = Z_ratio ** 0.5
    print(f"  Impedance ratio needed: {Z_ratio}:1")
    print(f"  Turns ratio needed: {turns_ratio:.1f}:1")
    print(f"  Example: {int(turns_ratio*100)} primary turns, 100 secondary turns")

    # Calculate with formula
    result = calc.transformer_impedance(Np=316, Ns=100, Z_secondary=8)
    print(f"  {result['primary_reflected_impedance_ohm']}Ω primary from 8Ω secondary")
    print(f"  Formula: {result.get('formula', 'N/A')}")

    # ================================================================
    # TEST 11: High Frequency Transformer (SMPS)
    # ================================================================
    print("\n📐 TEST 11: High Frequency Transformer (SMPS)")
    print("-" * 50)

    print("100kHz SMPS transformer, 12V to 5V, 10W:")
    design_hf = calc.transformer_design(Vp=12, Vs=5, Power_VA=10, frequency_hz=100000, J_A_per_mm2=5.0, Ae_cm2=2, B_max_tesla=0.2)
    print(f"  Frequency: 100kHz → much fewer turns!")
    print(f"  Primary turns: {design_hf['windings']['primary_turns']}")
    print(f"  Secondary turns: {design_hf['windings']['secondary_turns']}")
    print(f"  Primary wire: {design_hf['windings']['primary_wire_mm']}mm")
    print(f"  Core area: {design_hf['core']['area_cm2']}cm²")
    print(f"  Turns per volt at 100kHz: {design_hf['core']['turns_per_volt']}")

    # ================================================================
    # TEST 12: Comparison with Toroid Core
    # ================================================================
    print("\n📐 TEST 12: Comparison with Existing Toroid Calculator")
    print("-" * 50)

    print("Using toroid core (T50-52, µ=75) as transformer:")
    # Same core as toroid test
    od = 12.7
    id = 7.7
    ht = 4.8
    mu = 75

    # A_L value from toroid calculator
    al = calc.toroid_al_factor(mu, od, id, ht)
    print(f"  Core A_L = {al['al_value_nh_per_turn2']} nH/N²")

    # Calculate turns for 230V primary at 50Hz (using toroid as transformer)
    # For transformer, need primary inductance ~ 10H for 50Hz
    L_target = 10  # Henrys
    L_uh = L_target * 1_000_000
    turns_result = calc.toroid_turns_for_target(L_uh, mu, od, id, ht)
    print(f"  Turns needed for 10H primary: {turns_result['recommended_turns']} turns")
    print(f"  This is NOT practical for mains transformer!")

    # ================================================================
    print("\n" + "=" * 80)
    print("✅ ALL TRANSFORMER TESTS COMPLETED")
    print("=" * 80)

    # ================================================================
    # SUMMARY TABLE
    # ================================================================
    print("\n📊 QUICK REFERENCE TABLE")
    print("-" * 80)
    print(f"{'Function':<35} {'Purpose':<45}")
    print("-" * 80)
    print(f"{'transformer_voltage_ratio()':<35} {'Calculate voltages from turns ratio'}")
    print(f"{'transformer_current_ratio()':<35} {'Calculate currents from turns ratio'}")
    print(f"{'transformer_impedance()':<35} {'Impedance matching (square of turns ratio)'}")
    print(f"{'transformer_power()':<35} {'Power and efficiency calculations'}")
    print(f"{'transformer_wire_size()':<35} {'Wire gauge from current'}")
    print(f"{'transformer_turns_calculation()':<35} {'Turns needed for core'}")
    print(f"{'transformer_design()':<35} {'Complete transformer design'}")
    print(f"{'transformer_center_tap()':<35} {'Center-tapped transformer'}")
    print(f"{'transformer_example_designs()':<35} {'Reference examples'}")
    print("-" * 80)

    print("\n🎯 KEY FORMULAS IMPLEMENTED:")
    print("  • Vp/Vs = Np/Ns (Voltage transformation)")
    print("  • Ip/Is = Ns/Np (Current transformation)")
    print("  • Zp = (Np/Ns)² × Zs (Impedance transformation)")
    print("  • N = V / (4.44 × f × B × Ae) (Turns calculation)")
    print("  • A = I / J (Wire sizing)")
    print("  • P = V × I (Power)")


if __name__ == "__main__":
    main()