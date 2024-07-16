# Make function generation cheap

Previously was thinking something like use \~whatever function generator\~ you have. However, this was stupid, for a few reasons:
- Function generators cost $400
- They don't actually give a lot of wattage: so you'd still need amplification

If you already need amplification, there's no reason to use a function generator, instead of a cheap Signal Generator like the AD9833, paired with an amplifier + a microcontroller (for pulsing, safety limits, etc.)

### AD9833

This generates positive-only sine waves, from a Raspberry Pi or Arduino.

- Clock rate: 25 MHz 
    - This means that at 500khz, we get 50 steps per wave.
    - Per my calculations, this results in 0.8% THD (total harmonic distortion), which is negligible.
- Voltage: it goes 0.038V to 0.65V

### AC coupling: Capacitor

So, AD9833 generates positive-only "unipolar" sine waves.

Let's imagine it's just from 0V to 1V, for simplicity. The way you should think about it is that the output is *really* a combination of:
- An AC signal, from -0.5V to 0.5V
- A constant DC signal, at 0.5V

That means the peak becomes: 0.5V + 0.5V = 1V

And the trough becomes: -0.5V + 0.5V = 0V

Now, we want to convert this into a proper, bipolar signal. What we can do is use a **coupling capacitor** to "strip" the DC signal away, leaving us only with the -0.5V to 0.5V AC signal, centered around 0V.

The value of the capacitor should be *at least* 1 µF, in order to support the coupling of a 500khz signal. This we can calculate with the cutoff frequency formula:

fc = 1 / (2 * π * R * C)

Where:
- fc is the cutoff frequency (which should be 1/10th of the desired signal frequency, 500khz, to not cutoff the actual signal)
- R is the load impedance,
- C is the capacitance.

Which we can solve for C:

C = 1 / (2 * π * R * fc)

If **R = 50 (standard impedence)**, then:

C = 1 / (2 * π * 50Ω * 50khz)

C = 6.36619772e-8

C = 64 nF

<u>So we need a 64 nF capacitor.</u>

However, if **R = 0.7 MΩ** (as is the case in THS3091 amp), it becomes:

C = 1 / (2 * π * 0.7MΩ * 50khz)

C = 4.5472841e-12 F

C = 4.5 pF

<u>So a 4.5 pF capacitor would be more appropriate.</u>

Increasing the capacitor *decreases* the minimum cutoff frequency, so I think most small-ish capacitors are "small enough" to block DC, actually.

Here's a [link to browse 0.056uF-0.068uF](https://eu.mouser.com/c/rf-wireless/rf-capacitors/?capacitance=0.056%20uF~~0.068%20uF&rp=rf-wireless%2Frf-capacitors%7C~Capacitance)

### Op-amp circuit

May be a cheaper alternative to the amplifier below.

Need an op-amp capable of handling 500khz (meaning high slew rate), needs high voltage (around 30V will give 5W, current permitting), and needs high current (at least 166mA, to do 5W at 30V).

I quite like: [THS3091](https://www.ti.com/product/THS3091)

I think we can expect the gain to be 610 V/V, because the GBWP (gain bandwidth product) is 305 MHz, and we're at 500khz:

305 MHz / 500 kHz = 610

Let's assume we'll get about -15 V to +15 V output, since power supply is 32 V.

If we max out the AD9833, we'll get about -300mV to 300mV (post coupling capacitor). If we put it to it's minimum, I believe we'll get about 5% of that, meaning -15mV to 15mV (5%, because we need ~50 power levels out of the 2^10 possible ones, since we have 50 samples. Will probably need more in practice, bc sine waves aren't linear, but around there should be okay).

Let's choose the -300mV to 300mV configuration. This means we need 50 V/V to get to +15V. This means we need the following resistors in a non-inverting configuration:

1. **Feedback Resistor (Rf):** This resistor will be placed between the output of the op-amp and the inverting input.
2. **Input Resistor (Rin):** This resistor will be placed between the inverting input and the ground.

Because:

gain = 1 + Rf/Rin

For a gain of 50 V/V:

50 = 1 + Rf/Rin

Rf/Rin = 49

Rf = 49 * Rin

So, if you choose Rin = 1kΩ

Rf = 49 * 1kΩ = 49kΩ

Therefore, you can use a 1 kΩ resistor for Rin and a 49 kΩ resistor for Rf to achieve the desired gain of 50 V/V.

This configuration should provide the required amplification to achieve a peak output of ±15V from the input signal of ±300mV, enabling the generation of a higher voltage sine wave signal suitable for your application.

We might wanna get a 40kΩ resistor for Rin, to get a bit less gain, in case 50 results in clipping.

###### Impedence matching

Before the op-amp, I do not believe impedence matching is necessary, because the op-amp has such high input impedance that no current will flow.

After the op-amp, you have the following:
- [Op-amp output impedance](https://www.ti.com/lit/ds/symlink/ths3091.pdf): 0.06 Ω
- PZT-5H disc: 1.9 Ω

ChatGPT seems to be very confident that this won't be a problem, because:
- Low impedences overall, and the source is lower than the load (good).
- It's a small circuit, and a 500khz signal is a 600 meter wavelength, won't have reflections.

However, at 1.9 Ω, the PZT will draw > 5A, which is way to high. The op-amp is rated for 310mA.

###### Transformation

**Source (THS3091, op-amp):**

Voltage (peak): 15V
Voltage (rms): V_peak / sqrt(2) = 10.6V
Max current: 310mA
Max current (rms): I_peak / sqrt(2) = 219mA
Max power: 10.6V * 219mA = 2.32W

**Load (PZT-5H disc):**

Impedence: 1.9Ω

This means, to get it to draw 2.32W, the voltage must be:

V = sqrt(P * R)
V = sqrt(2.32W * 1.9Ω)
V = 2.09V

We can double check:

I = 2.09V / 1.9 = 1.1A
W = 1.1A * 2.09V = 2.299W

**Transformer:**

Since the load needs 2.09V, and the source gives 15V, we need a step-down ratio of:

15V / 2.09V = 7.35

Which is <u>7.35 : 1</u> or <u>1 : 0.14</u> depending on how you look.

Sourcing a transformer seems hard, but this website has some interesting search tools: https://www.coilcraft.com/en-us/products/transformers/

(Note to self: I can't for the life of me find a good tranformer, but I can find 0.25W transformers, so could probably just put in parallel)

### (Maybe: Isolator)

It might be a problem for the Amp & AD9833 that waves come back from reflections. Let's just test this emperically, these components are cheap. If it's a problem, we need an isolator.
