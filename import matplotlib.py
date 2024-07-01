import matplotlib.pyplot as plt
import numpy as np

# Define the input voltage range
Vin = np.linspace(0, 12, 500)

# Zener voltage
Vz = 5

# Define the output voltage
Vout = np.where(Vin < Vz, Vin, Vz)

# Plotting the voltage diagram
plt.figure(figsize=(10, 6))
plt.plot(Vin, Vout, label='Vout (Output Voltage)', color='blue')
plt.axhline(y=Vz, color='red', linestyle='--', label='Zener Voltage (Vz)')
plt.title('Voltage Diagram of Zener Diode Protection Circuit')
plt.xlabel('Input Voltage (Vin)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)
plt.ylim(0, 12)
plt.xlim(0, 12)
plt.show()
