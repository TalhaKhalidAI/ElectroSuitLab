# test_impedance.py

import sys
import os

# Add parent directory to path so 'App' can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from App.core.ElectronicsCalculator import ElectronicsCalculator
 
# Quick test
ec = ElectronicsCalculator()

print("100 mH to H:", ec.inductance_convertor(100, "mH", "H"))      # 0.1
print("100 uH to H:", ec.inductance_convertor(100, "uH", "H"))      # 0.0001
print("1 H to mH:", ec.inductance_convertor(1, "H", "mH"))          # 1000
print("10 uH to nH:", ec.inductance_convertor(10, "uH", "nH"))      # 10000
print("100 nH to uH:", ec.inductance_convertor(100, "nH", "uH"))    # 0.1
print("1000 pH to nH:", ec.inductance_convertor(1000, "pH", "nH"))  # 1