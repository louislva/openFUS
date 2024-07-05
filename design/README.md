# openFUS design (subject to change)

This document serves as the reference for the current design of the openFUS device. It is not final, and subject to change as we iterate & learn.

## Stack

Here are the components, roughly listed from back to front:

- **"Driver" box**
    - **RF-proof case** (is this necessary?)
    - **Arduino** or Raspberry Pi
    - **[Driver electronics](/design/driving-and-wattage.md)**
- **"Pointer" handheld**
    - **Housing (water-proof)**
    - **Angled back panel**, to reflect any waves that end up making it through backing away orthogonally
    - **[Backing](/design/backing.md):** absorb waves that come out through the back, so they don't reflect and interfere in the forward direction
        - Casting epoxy + tungsten powder: Has low impedence (not quite water, but close), and tungsten powder will reflect waves around, so they can be attenuated for a longer time, on a longer path
    - **Wires** that connect silver electrodes & the Driver
    - **[Impedance matching (backing)](/design/impedance-matching.md):** Quarter-wave transformer
        - Impedence needs to = sqrt(Z1 * Z2), where Z1 is the impedence of the backing, and Z2 is the impedence of the PZT-5H
        - Then you spread a quarter-wavelength of it, which will match the impedence between the two elements, theoretically bringing the reflection to 0
        - Manufacturing: ?? Ideally an epoxy, so it can be spread thin? Calculate how much weight needed for 1/4th wavelength for entire surface area, and put that amount on
    - **[PZT-5H disc](/design/piezoelectric-element.md):** raw transducer element
    - **[Impedance matching (lens)](/design/impedance-matching.md):** Quarter-wave transformer
        - Same trick, except now the impedence is between the PZT-5H and the lens
    - **[Lens](/design/lens.md):** concave lens, to focus the ultrasound waves
        - Material: Probably TPX/Polymethylpentene, which has almost same impedence as water/ultrasound gel/tissue
        - Shape: concave, since accoustic lenses are opposite of optical lenses (concave to focus, convex to diverge)
        - Exact shape: Use [`make_lens.py`](/make_lens.py) to design a lens - unsure this is actually right, let's see
        - Manufacturing: Probably buy a rod of TPX, slice it, and machine it
- **Ultrasound gel:** to fill the lens & make contact with skull or water tank, and couple the ultrasound waves to the skull
- Note: The electrodes to power the PZT-5H can be run through the impedance matching, if it's conductive (e.g. silver epoxy might be)

## Bill of materials (priced for 10 units)

- Arduino: $10
- AD9833: $12
- Coupling capacitor: ??
- RF amplifier: $300
- Housing: ??
- Backing: ??
- PZT-5H: $25
- Lens: $25
- Silver epoxy: $100
- Ultrasound gel: $10

Known costs: $482

Guess at the rest: $200

Guess at unknowns: $200