import math

def peak_to_rms(peak: float):
    return peak / math.sqrt(2)

MAX_CURRENT = peak_to_rms(0.31)

def wattage_to_op_amps(W: float, load_R: float = 1.9):
    # P = V^2 / R
    # V = sqrt(P * R)
    V = math.sqrt(W * load_R)
    I = V / load_R

    print("Actual:", I / MAX_CURRENT)
    n_opamps = math.ceil(I / MAX_CURRENT)
    return f"{n_opamps} op-amps @ {V:.2f} V = {W:.2f} W"

print(wattage_to_op_amps(0.09))
print(wattage_to_op_amps(0.36))
print(wattage_to_op_amps(0.82))
print(wattage_to_op_amps(1.46))
print(wattage_to_op_amps(2.28))