# [Design](/design.md) → Driving and Wattage

This is still very much in flux.

### Components

- Raspberry Pi or Arduino
- Breadboard
- Male and female jumper wires
- AD9833: Digital function generator
- MSOP-10 Breakout Board
- TODO: Power supply for AD9833 ??? 
- Coupling capacitor: Go from positive only AC signal, to positive and negative AC signal
- n * Op-amp circuit (in parallel)
    - THS3091: High-frequency op-amp
    - SOIC-8 Breakout Board
    - 49k ohm resistor in
    - 1k ohm resistor b
    - TODO: Power supply for THS3091 ???
- *Either: Send to PZT or have a 1.9 ohm resistor to mimic*
- *For prototyping: convert to cables for oscilloscope (this should be easy, since most oscilloscopes have those clamp-thingies you could just apply to male-ended jumper)*
- *Coaxial cable*
- *RF proof enclosure*

You can see a rough simulation in [driver-circuit.asc](/driver-circuit.asc) with LTSpice.

### Making it

You will need soldering equipment, particularly for soldering AD9833 and THS3091 onto their respective breakout boards.