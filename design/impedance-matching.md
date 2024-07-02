# [Design](/design.md) → Impedance Matching: Lens & backing

We need to impedence match the [lens](/design/lens.md) (TPX; 1.66 MRayl) and the piezoceramic (PZT-5H; 34.2 MRayl).

To do that, we need a material with an acoustic impedance that is:

sqrt(1.66 * 34.2) = 7.53 MRayl

We want this to be epoxy-based, since it'll be easy to customize, spread, and serve a dual purpose as an adhesive ("glue") for the lens. Ideally, we'd also want it to be conductive, so that it can used to power the piezoceramic (with electrodes on the side, not in the way of the wave).

When mixing two materials (like epoxy and a filler), the formula for the acoustic impedance is:

\[ Z_{\text{mix}} = \sqrt{(Z_1 \cdot v_1 + Z_2 \cdot v_2)(v_1 + v_2)} \]

Here:
- \( Z_{\text{mix}} \) is the acoustic impedance of the mixture.
- \( Z_1 \) and \( Z_2 \) are the acoustic impedances of materials 1 and 2, respectively.
- \( v_1 \) and \( v_2 \) are the volume fractions of materials 1 and 2, respectively, where \( v_1 + v_2 = 1 \).

### Approach: Epoxy + Silver

[Per ChatGPT](#appendix-chatgpt-calculates-epoxy-silver-ratio), we can use a 7.5% mixture of epoxy and silver (by volume) to get an acoustic impedance of around 7.5 MRayls. The advantage of silver is that it's highly conductive, which is useful for powering the piezoceramic.

[Per ChatGPT](#apendix-chatgpt-calculates-epoxy-silver-speed-of-sound), the speed of sound in this mixture would be around 3951 m/s. TODO: calculate this by hand, seems fishy.

**How do we mix silver & epoxy?**

*Easy answer: Buy a premade silver-epoxy,** like [this one](https://www.mouser.com/ProductDetail/MG-Chemicals/8330S-21G?qs=yK3xcw%2FedWGxbq%252BycI%252BFew%3D%3D&utm_id=17222215321&gad_source=1) (or for the [europoors](https://www.praud.pl/kleje_do_elektroniki/kleje_przewodzace_prad_elektryczny/dwuskladnikowe_kleje_epoksydowe/8331d_mg_chemicals))

Otherwise, my current understanding is: As long as the silver particles are small enough (like < 1/10th the wavelength, or something like that), evenly distributed, and similar sizes, they won't scatter or reflect the ultrasound.

For 500khz ultrasound, with a speed of sound of 3951 m/s, the wavelength is:

3951 m / 500000 = 0.007902 m = 7.902 mm

Which means the silver particles should be < 0.79 mm in size.

- Sigma Aldrich sells silver nanoparticles that are 8 μm (0.008 mm) in size. This is well under the 0.79 mm limit.

**How do we apply it precisely?**

From the wavelength we calculated, the **thickness of the layer** should be 7.902 / 4 = 1.975 mm, to act as a quarter-wave matching layer.

Current idea: Calcuate the weight of silver-epoxy needed for a 1.975 mm layer, on the area of the piezoceramic disc. Use a high-precision scale to measure the weight of the piezoceramic disc. Add silver-epoxy in the middle until the weight target is reached. Press the piezoceramic disc into the lens, spreading the silver epoxy evenly, and let it cure.

The lens should probably be wider than the piezoceramic disc, and have a machined inset in the bottom, to insert the piezoceramic disc into.

### Appendix: ChatGPT calculates epoxy-silver ratio

To find a mixture of epoxy and silver that gives an acoustic impedance around 7.5 MRayls, we use the weighted average formula for acoustic impedance:

\[ Z_{\text{mix}} = Z_1 \cdot v_1 + Z_2 \cdot v_2 \]

Here:
- \( Z_{\text{mix}} = 7.5 \times 10^6 \) Rayls
- \( Z_1 \) is the acoustic impedance of epoxy.
- \( Z_2 \) is the acoustic impedance of silver.
- \( v_1 \) and \( v_2 \) are the volume fractions of epoxy and silver, respectively, where \( v_1 + v_2 = 1 \).

Assuming:
- Acoustic impedance of epoxy (\( Z_{\text{epoxy}} \)): ~3 MRayls
- Acoustic impedance of silver (\( Z_{\text{silver}} \)): ~63 MRayls

Using these values:

\[ 7.5 \times 10^6 = (3 \times 10^6) \cdot v_1 + (63 \times 10^6) \cdot (1 - v_1) \]

Solving for \( v_1 \):

\[ 7.5 \times 10^6 = 3 \times 10^6 \cdot v_1 + 63 \times 10^6 \cdot (1 - v_1) \]
\[ 7.5 \times 10^6 = 3 \times 10^6 \cdot v_1 + 63 \times 10^6 - 63 \times 10^6 \cdot v_1 \]
\[ 7.5 \times 10^6 = 63 \times 10^6 - 60 \times 10^6 \cdot v_1 \]
\[ 7.5 \times 10^6 - 63 \times 10^6 = -60 \times 10^6 \cdot v_1 \]
\[ -55.5 \times 10^6 = -60 \times 10^6 \cdot v_1 \]
\[ v_1 = \frac{55.5 \times 10^6}{60 \times 10^6} \]
\[ v_1 = 0.925 \]

So, the volume fraction of epoxy (\( v_1 \)) is approximately 0.925 (or 92.5%), and the volume fraction of silver (\( v_2 \)) is approximately 0.075 (or 7.5%).

### Apendix: ChatGPT calculates epoxy-silver speed of sound

To find the speed of sound in a mixture of epoxy and silver with a given acoustic impedance, we use the relationship between acoustic impedance, density, and the speed of sound:

\[ Z = \rho \cdot c \]

where:
- \( \rho \) is the density of the mixture.
- \( c \) is the speed of sound in the mixture.

First, we estimate the density of the mixture. Assuming we know the densities of epoxy and silver:

- Density of epoxy (\( \rho_{\text{epoxy}} \)): ~1.2 g/cm³ (1200 kg/m³)
- Density of silver (\( \rho_{\text{silver}} \)): ~10.5 g/cm³ (10500 kg/m³)

Using the volume fractions \( v_1 \) and \( v_2 \) calculated previously:

\[ v_1 = 0.925 \]
\[ v_2 = 0.075 \]

The density of the mixture (\( \rho_{\text{mix}} \)) can be calculated as:

\[ \rho_{\text{mix}} = \rho_{\text{epoxy}} \cdot v_1 + \rho_{\text{silver}} \cdot v_2 \]

Plugging in the values:

\[ \rho_{\text{mix}} = (1200 \, \text{kg/m}^3) \cdot 0.925 + (10500 \, \text{kg/m}^3) \cdot 0.075 \]
\[ \rho_{\text{mix}} = 1110 \, \text{kg/m}^3 + 787.5 \, \text{kg/m}^3 \]
\[ \rho_{\text{mix}} = 1897.5 \, \text{kg/m}^3 \]

Now we use the acoustic impedance \( Z_{\text{mix}} = 7.5 \times 10^6 \) Rayls to find the speed of sound \( c_{\text{mix}} \):

\[ Z_{\text{mix}} = \rho_{\text{mix}} \cdot c_{\text{mix}} \]
\[ 7.5 \times 10^6 = 1897.5 \cdot c_{\text{mix}} \]
\[ c_{\text{mix}} = \frac{7.5 \times 10^6}{1897.5} \]
\[ c_{\text{mix}} \approx 3951 \, \text{m/s} \]
