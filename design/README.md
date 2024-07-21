# openFUS design (subject to change)

This document serves as the reference for the current design of the openFUS device. It is not final, and subject to change as we iterate & learn.

## Stack

Here are the components, roughly listed from back to front:

- **"Driver" box**
    - **RF-proof case** (is this necessary?)
    - **Arduino** or Raspberry Pi
    - **[Driver electronics](/design/driving-and-wattage.md)**
        - AD9833
        - Coupling capacitor
        - Amplifier
- **"Pointer" handheld**
    - **Housing (water-proof)**
    - **Angled back panel**, to reflect any waves that end up making it through backing away orthogonally
    - **[Backing](/design/backing.md):** absorb waves that come out through the back, so they don't reflect and interfere in the forward direction
    - **Wires** that connect silver electrodes & the Driver
    - **[PZT-5H disc](/design/piezoelectric-element.md):** raw transducer element
    - **[Impedance matching (PZT to lens)](/design/impedance-matching.md):** Quarter-wave transformer
    - **[Lens](/design/lens.md):** concave lens, to focus the ultrasound waves
        - Material: Probably TPX/Polymethylpentene, which has almost same impedence as water/ultrasound gel/tissue
        - Shape: concave, since accoustic lenses are opposite of optical lenses (concave to focus, convex to diverge)
        - Exact shape: Use [`make_lens.py`](/make_lens.py) to design a lens - unsure this is actually right, let's see
        - Manufacturing: Probably buy a rod of TPX, slice it, and machine it
- **Ultrasound gel:** to fill the lens & make contact with skull or water tank, and couple the ultrasound waves to the skull
- Note: The electrodes to power the PZT-5H can be run through the impedance matching, if it's conductive (e.g. silver epoxy might be)

## Bill of materials (priced for 10 units)

- Arduino: $25
- AD9833: $12
- THS3091: $12
- Power Supply: $100
- RF box for housing Driver: ??
- 3d-printed housing for Pointer: ??
- Backing epoxy: ??
- Backing tungsten: ??
- PZT-5H: $25
- Lens: $25
- Silver epoxy: $20
- Ultrasound gel: $10
- PCB: ~$5
- Small electrical components (coupling capacitor, resistors, etc.): ~$10

Known costs: $245

Guess at the rest: $250

Guess at unknowns: $200