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

\[ f_c = \frac{1}{2\pi RC} \]

Where:
- \( f_c \) is the cutoff frequency (which should be 1/10th of the desired signal frequency, 500khz, to not cutoff the actual signal)
- \( R \) is the load impedance,
- \( C \) is the capacitance.

Which we can solve for \( C \):

\[ C = \frac{1}{2\pi R f_c} \]

Which gives us

C = 1/(2*pi*R*50khz)

C = 1/(314000*R)

Let's assume R = 50 (standard impedence)

C = 1/(314000*50)

C = 0.0636942675 µF

So we simply need a 0.0636942675 µF (64 nF) capacitor.

Increasing the capacitor *decreases* the minimum cutoff frequency.

Here's a [link to browse 0.056uF-0.068uF](https://eu.mouser.com/c/rf-wireless/rf-capacitors/?capacitance=0.056%20uF~~0.068%20uF&rp=rf-wireless%2Frf-capacitors%7C~Capacitance)

### Amplifier

Without amplification, we have about 0.032 W (according to [ChatGPT](#appendix-pre-amplification-wattage)).

Back of the envelope says we need up to 5W (since FDA safety limit is 720mW/cm2, and our surface area is about 7cm2).

Going from 0.032 W to 5W is a 20 dB gain.

[This link searches for RF amplifiers that give > 20dB of gain, and work for 500khz](https://eu.mouser.com/c/semiconductors/wireless-rf-semiconductors/wireless-rf-integrated-circuits/rf-amplifier/?gain=20%20dB~~38%20dB&operating%20frequency=0%20Hz%20to%201%20GHz~~500%20kHz%20to%204%20GHz&rp=semiconductors%2Fwireless-rf-semiconductors%2Fwireless-rf-integrated-circuits%2Frf-amplifier%7C~Operating%20Frequency%7C~Gain)

You should [sort by max current](https://eu.mouser.com/c/semiconductors/wireless-rf-semiconductors/wireless-rf-integrated-circuits/rf-amplifier/?gain=20%20dB~~38%20dB&operating%20frequency=0%20Hz%20to%201%20GHz~~500%20kHz%20to%204%20GHz&rp=semiconductors%2Fwireless-rf-semiconductors%2Fwireless-rf-integrated-circuits%2Frf-amplifier%7C~Operating%20Frequency%7C~Gain&sort=operating%20supply%20current%7C1) however, because most of these are not capable of doing 5W, even if the gain is 20dB.

The strongest RF amplifier seems to be [this guy](https://eu.mouser.com/datasheet/2/1030/ZHL_6A_2b-3368481.pdf), which does 24 V * 350 mA = 8.4 W.

However, it also surges when turned on; TODO: surge protection (this might be fine? only thing after it is PZT)

### (Maybe: Isolator)

It might be a problem for the Amp & AD9833 that waves come back from reflections. Let's just test this emperically, these components are cheap. If it's a problem, we need an isolator.

# Appendix: Pre-amplification Wattage

**Me:**
```
I have a -0.35V to 0.35V sine wave at 500khz

The load is a PZT disc, with an impedence of < 1.9 ohms

What is the wattage?
```

**ChatGPT:**
```
To calculate the wattage, we need to determine the power delivered to the load. Here's how we can calculate it:

1. **Amplitude of the sine wave (V_peak)**: The peak voltage of the sine wave is 0.35V.
2. **Impedance of the load (Z)**: The impedance is 1.9 ohms.

The formula to calculate the power delivered to a load in an AC circuit is:
\[ P = \frac{V_{rms}^2}{Z} \]

Where:
- \( V_{rms} \) is the root mean square (RMS) voltage.
- \( Z \) is the impedance of the load.

For a sine wave, the RMS voltage is given by:
\[ V_{rms} = \frac{V_{peak}}{\sqrt{2}} \]

Let's calculate it step by step.

1. Calculate the RMS voltage:
\[ V_{rms} = \frac{0.35V}{\sqrt{2}} \approx 0.247V \]

2. Calculate the power using the RMS voltage and the impedance:
\[ P = \frac{(0.247V)^2}{1.9 \, \Omega} \approx \frac{0.061 \, V^2}{1.9 \, \Omega} \approx 0.032W \]

So, the wattage delivered to the PZT disc is approximately **0.032 watts**.
```