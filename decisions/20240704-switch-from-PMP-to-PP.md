# Switch from PMP (polymethylpentene, aka TPX) to PP (polypropylene) for the accoustic lens

The constraints on the lens is:
- **Impedence match next layer** (ultrasound gel) best possible, to minimize interface reflections
- **Large IOR** (the number that determines it's lensing-power; derived from ratio of speed of sound in lens vs next layer)
- **Low cost**

Originally we were planning to use PMP, since it impedence matches water/gel/tissue very well & is common in sonography for this reason.

However, I've decided we will switch to PP, since:
- We don't care as much about impedence matching in focused ultrasound as in imaging (since there is no image which reflections will distort). See [below]() for the difference in reflection %
- Much higher IOR, meaning lens can be **47% thinner**, which will make it easier to fill up with ultrasound gel
- **82% cheaper** + we need **34% less volume** for same lensing, making it a total of **89% reduction in cost**
- Easier to source and machine, since PP is much more common

### Spec differences

| Property                | PMP (Polymethylpentene)                                                                 | PP (Polypropylene)                                                                 |
|-------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Price (goodfellow)      | [€2,781](https://www.goodfellow.com/eu/tpx-mx004-pmp-rod-1000003171)                    | [€482 (€241 * 2)](https://www.goodfellow.com/eu/pp-rod-1000170613)                |
| Speed of sound          | [2095 m/s](https://www.sciencedirect.com/science/article/abs/pii/S0301562911002857), [2097 m/s](https://www.osti.gov/servlets/purl/1574369) | [2565 m/s](https://www.ndt.net/links/proper.htm), [2470 m/s](https://www.signal-processing.com/table.php) |
| Density                 | [0.83 g/cm³](https://en.wikipedia.org/wiki/Polymethylpentene)                           | [between 0.895 and 0.92 g/cm³](https://plasticseurope.org/plastics-explained/a-large-family/polyolefins/#:~:text=PP%20(polypropylene)%3A%20The%20density,plastic%20with%20the%20lowest%20density.) |
| Acoustic impedance      | 0.83 g/cm³ * 2095 m/s = 1.7385 MRayl                                                    | 0.92 g/cm³ * 2565 m/s = 2.360 MRayl                                             |
| Reflection with water   | ((1.7385 - 1.48) / (1.7385 + 1.48))^2 = 0.006 (0.6%)                                      | ((2.328 - 1.48) / (2.328 + 1.48))^2 = 0.050 (5.0%)                                  |