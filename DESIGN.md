# openFUS design (subject to change)

This document serves as the reference for the current design of the openFUS device. It is not final, and subject to change as we iterate & learn.

## Option A

- [Off-the-shelf function generator](/design/driving-and-wattage.md)
    - Need sine waves, square waves are dangerous; this means we need a kind of expensive machine, probably.
    - Check how much reflection it can take (typically will say a %)
    - If needed, can use [Component I don't remember what's called (think, Isolator?) to redirect reflected waves]
    - How much power?
- Ultrasound transducer (from back to front)
    - **Angled back panel**, to reflect any waves that end up making it through backing, away orthogonally
    - **Backing:** absorb waves that go out through the back (non-skull side), so they don't reflect back and interfere
        - Casting epoxy + tungsten powder: Has low impedence (not quite water, but close), and tungsten powder will reflect waves around, so they can be attenuated for a longer time, on a longer path  
    - **Impedance matching (backing):** Quarter-wave transformer
        - Impedence needs to = sqrt(Z1 * Z2), where Z1 is the impedence of the backing, and Z2 is the impedence of the PZT-5H
        - Then you spread a quarter-wavelength of it, which will match the impedence between the two elements, theoretically bringing the reflection to 0
        - Manufacturing: ?? Ideally an epoxy, so it can be spread thin? Calculate how much weight needed for 1/4th wavelength for entire surface area, and put that amount on
    - **PZT-5H disc:** raw transducer element
    - **[Impedance matching (lens):](/design/impedance-matching-lens.md)** Quarter-wave transformer
        - Same trick, except now the impedence is between the PZT-5H and the lens
    - **[Lens:](/design/lens.md)** concave lens, to focus the ultrasound waves
        - Material: Probably TPX/Polymethylpentene, which has almost same impedence as water/ultrasound gel/tissue
        - Shape: concave, since accoustic lenses are opposite of optical lenses (concave to focus, convex to diverge)
        - Exact shape: Use [`make_lens.py`](/make_lens.py) to design a lens - unsure this is actually right, let's see
        - Manufacturing: Probably buy a rod of TPX, slice it, and machine it
    - **Ultrasound gel:** to fill the lens, and couple the ultrasound waves to the skull
    - Note: The electrodes to power the PZT-5H can be run through the impedance matching, if it's conductive (e.g. silver epoxy might be)

