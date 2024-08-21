# Given values
Z_A = 2.4
Z_M = 7
Z_B = 35

# Transmitted wave ratios
T_A = 2 * Z_A / (Z_A + Z_M)
T_B = 2 * Z_M / (Z_M + Z_B)

# Corrected reflected wave ratios
R_A = (Z_M - Z_A) / (Z_M + Z_A)
R_B = (Z_B - Z_M) / (Z_B + Z_M)

# Energy transmission formula
box_T_corrected = ((T_A * T_B) / (1 - R_A * R_B))**2 * (Z_B / Z_A)

print("T_A, T_B, R_A, R_B", T_A, T_B, R_A, R_B)
print("Transmitted energy:", box_T_corrected)
