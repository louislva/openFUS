# [Design](/design.md) → Lens

**Material:** TPX (Polymethylpentene)
- Rod or pre-machined from [Boedeker](https://www.boedeker.com/Product/TPX)
- Rod from [Sigma Aldrich](https://www.sigmaaldrich.com/DK/en/search/polymethylpentene?focus=products&page=1&perpage=30&sort=relevance&term=polymethylpentene&type=product)
- Rod from [Goodfellow](https://www.goodfellow.com/uk/material/polymers/pmp-polymethylpentene/mx004-pmp-rod)

**About TPX (Polymethylpentene):**

Density = 0.83 g/cm³
Speed of sound = 2000-2200 m/s (per ChatGPT; own research says ~2100 m/s)

Acoustic impedance = 830kg/m³ * 2000m/s = 1.66 * 10^6 kg/(m^2 s)
Acoustic impedance = 1.66 * 10^6 kg/(m^2 s) = <u>1.66 MRayl</u>

**Shape:** We can use the lens maker's formula to calculate the radius of curvature of the lens. We've created `make_lens.py` to help with this calculation, which exports the design to a `.obj` file.

**Validation:** TODO: Validate the lens in simulation using `k-wave` or `Field II`.

**Machining:**

CNC machining is the best way, as I understand it. I know nothing about CNC machining. TODO: figure out how to machine TPX.