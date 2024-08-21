# Okay, so there are a number of cool pre-made silver epoxy's that double as electrodes & quarter-wavelength transformers.
# 
# Primarily these:
# - 8330S: https://mgchemicals.com/downloads/tds/tds-8330S-2parts.pdf
# - 8330D: https://mgchemicals.com/downloads/tds/tds-8330D-2parts.pdf
# - 8331D: https://mgchemicals.com/downloads/tds/tds-8331D-2parts.pdf
# - 8331S: https://mgchemicals.com/downloads/tds/tds-8331S-2parts.pdf
# 
# Legacy versions:
# - 8330: https://www.mgchemicals.com/downloads/tds/tds-8330-2parts.pdf
# - 8331: https://www.mgchemicals.com/downloads/tds/tds-8331-2parts.pdf
# 
# They DO NOT list the speed of sound and the acoustic impedance, which are the values we care about. They don't even mention the ratio between epoxy and silver. So we have to do a little guessing?

import math

SILVER_YOUNG_MODULUS = 83 * 10**9 # Pa = N/m^2
EPOXY_YOUNG_MODULUS = 2.5 * 10**9 # Pa = N/m^2

def calc_speed_of_sound(young_modulus, density):
    return math.sqrt(young_modulus / (density * 1000))

def mixture_linear_volume(v1, n1, v2, n2):
    # This rule applies for (at least):
    # - Young's modulus
    # 
    return (v1 * n1 + v2 * n2)

def ratio_of_mixture_volumes(v1, n1, v2, n2):
    return v1 / (v1 + v2)

def calc_impedance(density, speed_of_sound):
    return (density * speed_of_sound) / 1000


EPOXY_DENSITY = 2.11
SILVER_DENSITY = 10.49 # g/cm^3

def guess_silver_mix_by_density(density):
    return (density - EPOXY_DENSITY) / (SILVER_DENSITY - EPOXY_DENSITY)

class Properties:
    def __init__(self, density: float, mixture: float, speed_of_sound: float, impedance: float):
        self.density = density
        self.mixture = mixture
        self.speed_of_sound = speed_of_sound
        self.impedance = impedance

    @classmethod
    def from_density(cls, density: float):
        silver_mix = guess_silver_mix_by_density(density)
        speed_of_sound = calc_speed_of_sound(mixture_linear_volume(SILVER_YOUNG_MODULUS, silver_mix, EPOXY_YOUNG_MODULUS, 1 - silver_mix), density)
        impedance = calc_impedance(density, speed_of_sound)
        return Properties(density, silver_mix, speed_of_sound, impedance)

    @classmethod
    def from_mixture_volume(cls, mixture: float):
        density = mixture_linear_volume(SILVER_DENSITY, mixture, EPOXY_DENSITY, 1 - mixture)
        return cls.from_density(density)

    @classmethod
    def from_mixture_weight(cls, weight: float):
        # Calculate the volume fraction of silver in the mixture based on weight
        silver_volume_fraction = weight / (weight + (1 - weight) * (SILVER_DENSITY / EPOXY_DENSITY))
        return cls.from_mixture_volume(silver_volume_fraction)
    
    def get_wavelength(self, frequency):
        return (self.speed_of_sound / frequency) * 1000
       
    def get_quarter_wave_volume(self, frequency):
        mm3 = math.pi * (15**2) * self.get_wavelength(frequency)/4
        return mm3 * 0.001

def report(name: str, props: Properties):
    print("===", name, "===")
    print(f"- Silver mix: {props.mixture:.2f}")    
    print(f"- Speed of sound: {props.speed_of_sound:.0f}m/s")
    print(f"- Density: {props.density:.2f}g/cm^3")
    print(f"- Impedance: {props.impedance:.2f}MRayls")
    print(f"- Wavelength: {props.get_wavelength(500000):.2f}mm")
    print(f"- Quarter wavelength: {(props.get_wavelength(500000) / 4):.2f}mm")
    print(f"- Quarter-wave volume: {props.get_quarter_wave_volume(500000):.2f}ml")
    print()

def report_by_density(name: str, density: float):
    props = Properties.from_density(density)
    report(name, props)

def report_by_mixture_weight(name: str, weight: float):
    props = Properties.from_mixture_weight(weight)
    report(name, props)

if __name__ == "__main__":
    # report_by_density("MG 8330S", 3.06)
    # report_by_density("MG 8330D", 3.22)
    # report_by_density("MG 8331D", 2.4)
    # report_by_density("MG 8331S", 2.42)
    # report_by_mixture_weight("Em-Tec AG29", 0.76)
    # report_by_density("Em-Tec AG29", 3.22) # Shows roughly the same as the other approach
    # report_by_mixture_weight("Em-Tec AG32", 0.65)
    # report_by_density("BONDLINE 2080", 3.89)
    report_by_density("CircuitWorks CW2400", 4)
    
    # report_by_mixture_weight("Epoxy", 0)
    # report_by_mixture_weight("Silver", 1)
    print("imp by principle CW2400", calc_impedance(4, 1089))