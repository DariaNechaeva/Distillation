from uncertainties import ufloat # Floating numbers with uncertainty

def difference(base, deduct):
    return base - deduct

# Function for SGA, SGEA, SGER. Reference:
# Series: Analytica EBC
# Document: 8.2.1 SPECIFIC GRAVITY OF WORT USING A PYKNOMETER – 2004
# Section: 9.1.1 Calculate the specific gravity (SG) of the wort
# SGA = SG of the distillate (references between documents: 9.2.1 -> 9.43.1 -> 8.2.1)
# SGEA = SG of the decarbonated beer (references between documents: 9.2.1 -> 9.43.1 -> 8.2.1)
# SGER = SG of the residue solution (references between documents: 9.4 -> 9.43.1 -> 8.2.1)
def specific_gravity_using_pycnometer(mass_with_substance, mass_empty, mass_with_water):
    return (mass_with_substance - mass_empty) / (mass_with_water - mass_empty)

# Function for alcohol content by mass. Reference:
# Series: Analytica EBC
# Document: 9.2.1 ALCOHOL IN BEER BY DISTILLATION – 2008
# Section: 9.1 Alcohol as % (m/m)
def alcohol_content_by_mass(SGA):
    return 517.4 * (1 - SGA) + 5084 * (1 - SGA)**2 + 33503 * (1 - SGA)**3

# Function for alcohol content by volume (ABV). Reference:
# Series: Analytica EBC
# Document: 9.2.1 ALCOHOL IN BEER BY DISTILLATION – 2008
# Section: 9.2 Alcohol as % (V/V)
def alcohol_content_by_volume(A_by_mass, SGEA):
    return A_by_mass * SGEA / 0.791

# Function for real extract (ER) and apparent extract (EA). Reference:
# Series: Analytica EBC
# Document: 9.4 ORIGINAL, REAL AND APPARENT EXTRACT AND ORIGINAL GRAVITY OF BEER – 2004
# Section: 9.1.1 Real extract, 9.1.2 Apparent extract
def extract(specific_gravity):
    return -460.234 + 662.649 * specific_gravity - 202.414 * specific_gravity**2

# Function for original extract. Reference:
# Series: Analytica EBC
# Document: 9.4 ORIGINAL, REAL AND APPARENT EXTRACT AND ORIGINAL GRAVITY OF BEER – 2004
# Section: 9.1.4.1 Calculate the original extract (% Plato) of the beer
def original_extract(A_by_mass, real_extract):
    return (2.0665 * A_by_mass + real_extract) * 100 / (100 + 1.0665 * A_by_mass)

# Function for real degree of fermentation of beer (RDF). Reference:
# Series: Analytica EBC
# Document: 9.5 REAL DEGREE OF FERMENTATION OF BEER 1997
# Section: 5.1.1 Calculate real degree of fermentation of beer
def real_degree_of_fermentation(A_by_mass, real_extract):
    return 100 * 2.0665 * A_by_mass / (2.0665 * A_by_mass + real_extract)

# Function for apparent degree of fermentation or apparent attenuation (ADF). Reference:
# Series: Analytica EBC
# Document: 4.11.2 FERMENTABILITY, FINAL ATTENUATION OF LABORATORY WORT FROM MALT: RAPID METHOD – 1999
# Section: 9.1.2 Obtain the fermentability (apparent attenuation)
def apparent_degree_of_fermentation(original_extract, apparent_extract):
    return 100 * (original_extract - apparent_extract) / original_extract

# Function for spirit indication. Reference:
# Series: Analytica EBC
# Document: 9.4 ORIGINAL, REAL AND APPARENT EXTRACT AND ORIGINAL GRAVITY OF BEER – 2004
# Section: 9.1.5.1 Calculate the spirit indication (S)
def spirit_indication(SGA):
    return 1000 * (1-SGA)

# Function for degrees of gravity lost. Reference:
# Series: Analytica EBC
# Document: 9.4 ORIGINAL, REAL AND APPARENT EXTRACT AND ORIGINAL GRAVITY OF BEER – 2004
# Section: 9.1.5.2 Calculate the corresponding degrees of gravity lost (D)
def degrees_of_gravity_lost(S):
    if        S < 2:   D = S * 4.24
    elif 2 <= S < 4:   D = S * 4.38411 - 0.32055
    elif 4 <= S < 5:   D = S * 4.4812 - 0.70952
    elif 5 <= S < 6:   D = S * 4.5051 - 0.81757
    elif 6 <= S < 7:   D = S * 4.54437 - 1.05698
    elif 7 <= S < 8:   D = S * 4.55892 - 1.16411
    elif 8 <= S < 9:   D = S * 4.57624 - 1.30303
    elif 9 <= S < 10:  D = S * 4.5982 - 1.50326
    elif 10 <= S < 11: D = S * 4.71954 - 2.72814
    elif 11 <= S < 12: D = S * 4.8558 - 4.2204
    elif 12 <= S < 13: D = S * 4.9327 - 5.1375
    elif 13 <= S < 14: D = S * 4.9442 - 5.2861
    elif 14 <= S < 15: D = S * 5.0030 - 6.0788
    elif 15 <= S < 16: D = S * 5.0630 - 6.97582
    elif       S>= 16: D = S * 5.07 - 7.08
    return D

# Function for residue gravity (RG). Reference:
# Series: Analytica EBC
# Document: 9.4 ORIGINAL, REAL AND APPARENT EXTRACT AND ORIGINAL GRAVITY OF BEER – 2004
# Section: 9.1.5.3 Calculate the residue gravity (RG)
def residue_gravity(SGER):
    return 1000 * (SGER-1)

# Function for original gravity. Reference:
# Series: Analytica EBC
# Document: 9.4 ORIGINAL, REAL AND APPARENT EXTRACT AND ORIGINAL GRAVITY OF BEER – 2004
# Section: 9.1.5.4 Calculate the original gravity
def original_gravity(D, RG):
    return D + RG

# Function for average alcohol content by volume. Reference:
# Series: Analytica EBC
# Document: 9.2.1 ALCOHOL IN BEER BY DISTILLATION – 2008
# Section: 10.1 1995/1996 trial Alcohol in % (V/V)
def average_alcohol_content_by_volume(alcohol_content_S1, alcohol_content_S2):
    mean = (alcohol_content_S1 + alcohol_content_S2) / 2
    repeatability = 0.062
    if  (0.84 <= alcohol_content_S1 <= 7.27) \
    and (0.84 <= alcohol_content_S2 <= 7.27) \
    and (abs(alcohol_content_S1 - alcohol_content_S2) <= repeatability):
        R95 = 0.07 + 0.02 * mean
        uncertainty = (R95 / 2.77) * 2
        return ufloat(mean, uncertainty)
    else:
        return None

# Function for average alcohol content by mass. Reference:
# Series: Analytica EBC
# Document: 9.2.1 ALCOHOL IN BEER BY DISTILLATION – 2008
# Section: 10.2 1996 trial - 10.2.1 Alcohol in % (m/m)
def average_alcohol_content_by_mass(alcohol_content_S1, alcohol_content_S2):
    mean = (alcohol_content_S1 + alcohol_content_S2) / 2
    repeatability = 0.03 + 0.005 * mean
    if  (1.72 <= alcohol_content_S1 <=7.00) \
    and (1.72 <= alcohol_content_S2 <=7.00) \
    and (abs(alcohol_content_S1 - alcohol_content_S2) <= repeatability):
        R95 = 0.03 + 0.02 * mean
        uncertainty = (R95 / 2.77) * 2
        return ufloat(mean, uncertainty)
    else:
        return None

#If duplicate determinations give specific gravities which differ by more than two units in the fourth decimal place repeat the analysis.
def average_specific_gravity_of_beer(specific_gravity_S1, specific_gravity_S2):
    return (specific_gravity_S1 + specific_gravity_S2) / 2

def average_original_extract(original_extract_S1, original_extract_S2):
    return (original_extract_S1 + original_extract_S2) / 2

def average_real_extract(real_extract_S1, real_extract_S2):
    return (real_extract_S1 + real_extract_S2) / 2

def average_apparent_extract(apparent_extract_S1, apparent_extract_S2):
    return (apparent_extract_S1 + apparent_extract_S2) / 2

def average_real_degree_of_fermentation (real_degree_of_fermentation_S1, real_degree_of_fermentation_S2):
    return (real_degree_of_fermentation_S1 + real_degree_of_fermentation_S2) / 2

def average_apparent_degree_of_fermentation(apparent_degree_of_fermentation_S1, apparent_degree_of_fermentation_S2):
    return (apparent_degree_of_fermentation_S1 + apparent_degree_of_fermentation_S2) /2

def average_original_gravity(original_gravity_S1, original_gravity_S2):
    return (original_gravity_S1 + original_gravity_S2) / 2

def average_beer_pH(pH_S1, pH_S2):
    return (pH_S1 + pH_S2) / 2
