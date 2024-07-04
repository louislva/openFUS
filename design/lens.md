# [Design](/design.md) → Lens

**Material:** PP (Polypropylene)

**About PP:**

Density = 0.92 g/cm³
Speed of sound = 2470-2565 m/s

Acoustic impedance = 2.360 MRayl
Reflection with water = 5%

**Shape:** We can use the lens maker's formula to calculate the radius of curvature of the lens. We've created `make_lens.py` to help with this calculation, which exports the design to a `.obj` file.

**Validation:** TODO: Validate the lens in simulation using `k-wave` or `Field II`.

**Machining:** CNC machining is the best way. Working on converting `.obj` lenses to g-code paths.

Other options are:
- 3d printing: beware of small airgaps (since plastics may cool too quickly)
- Injection molding: no clue where to even start with this, feel free to submit a PR if you know how to do this