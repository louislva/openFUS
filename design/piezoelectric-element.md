# [Design](/design.md) → Piezoelectric Element

The piezoelectric element is the material that converts between electric and mechanical signals. There are lots of such materials. If you want high power for medical applications, you'll generally want PZT, specifically PZT-5H.

The wavelength is equal to double the thickness of the element.

So if you want a 500khz element:
- You can divide the speed of sound in PZT-5H (~4000m/s) to get the wavelength: 4000m/s / 500000khz = 8mm
- You can then divide by 2 to get the thickness (~4mm)

STEMINC is a reputable site, which sells PZT-5H discs (with no minimum order quantity): [30x4.2mm disc](https://www.steminc.com/PZT/en/pzt-ceramic-disc-30x42mm-s-500-khz)

### Why 500khz?

With tFUS, you get a tradeoff between resolution (higher frequency is better) and skull penetration (lower frequency is attenuated less, and can make it into the brain).

500khz is the sweetspot. In tissue, the speed of sound is approximately 1500m/s, meaning a 500khz wave is about 3mm. However, if you go much higher, you'll run into a lot of attenuation.

