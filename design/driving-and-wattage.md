# [Design](/design.md) → Driving and Wattage

This is still very much in flux.

### Components

- Raspberry Pi or Arduino
- Breadboard
- Male and female jumper wires
- AD9833: Digital function generator (DIP variant)
- TODO: Power supply for AD9833 ??? (think Raspberry Pi can handle, actually)
- Coupling capacitor: Go from positive only AC signal, to positive and negative AC signal
- n * Op-amp circuit (in parallel)
    - THS3091: High-frequency op-amp
    - SOIC-8 Breakout Board
    - 49k ohm resistor in
    - 1k ohm resistor b
    - Power supply. Either [this](https://dk.rs-online.com/web/p/switch-mode-stromforsyninger-smps/0413655) or [this](https://dk.rs-online.com/web/p/switch-mode-stromforsyninger-smps/1368987); can use experimentation variable power supply for now
    - TODO: coupling capacitor on output
    - TODO: decoupling capacitor on power supply
- *Either: Send to PZT or have a 1.9 ohm resistor to mimic*
- *For prototyping: convert to cables for oscilloscope (this should be easy, since most oscilloscopes have those clamp-thingies you could just apply to male-ended jumper)*
- *Coaxial cable*
- *RF proof enclosure*

You can see a rough simulation in [driver-circuit.asc](/driver-circuit.asc) with LTSpice.

### Making it

You will need soldering equipment, particularly for soldering AD9833 and THS3091 onto their respective breakout boards.