# ~~Get more power + void the transformer problem~~ (REVERTED, because stupid idea)

Current problems:
- Even if no transformer problems, our op-amp only gives about 2.32W. This may not be enough power, depending on physics of PZT, lens, etc.
- Regardless, transformers suck ass & make the circuit more complicated. To limit to 300mA, we need to add resistance, which I think gives impedence mismatch problems.

Big solution: Put n op-amps in parallel, giving us n * 300mA of max current.

## How big n?

Ideally, we add no resistance, and only lower the voltage, such that the PZT (at 1.9 ohms), draws the power it needs. Let's assume we want to bring at max 5W to the PZT:

Given 5W, and 1.9ohms, we can calulate the voltage should be:

P = V^2 / R
V = sqrt(P * R)
V = sqrt(5W * 1.9ohms)
V = 3.08V

With 3.08V, the current draw will be:

I = V / R
I = 3.08V / 1.9ohms
I = 1.62A

Which means:

n = ceil(1.62A / 300mA) 
n = 6

So we need 6 op-amps in parallel to get 5W with no transformers or added impedence. We should, in this scenario also make the gain lower, since we don't need or want 15V.

## A more general python script to calculate:

```python
import math

def peak_to_rms(peak: float):
    return peak / math.sqrt(2)

MAX_CURRENT = peak_to_rms(0.31)

def wattage_to_op_amps(W: float, load_R: float = 1.9):
    # P = V^2 / R
    # V = sqrt(P * R)
    V = math.sqrt(W * load_R)
    I = V / load_R

    n_opamps = math.ceil(I / MAX_CURRENT)
    return n_opamps, V

print(wattage_to_op_amps(5))
```

The cost for, let's say 8 opamps is $12 * 8 = $96. This is more expensive than transformers (by a lot), but simpler.