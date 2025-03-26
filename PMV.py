import math
#Fanger 1970
def calculate_pmv(T_a, RH, Met, Clo, v, T_r):
    """
    Calculate PMV (Predicted Mean Vote) for given environmental and personal factors.

    Parameters:
    T_a (float): Air temperature in °C
    RH (float): Relative humidity in %
    Met (float): Metabolic rate in Met units (default is 1.0 for light activities)
    Clo (float): Clothing insulation in Clo units (default is 0.5 for light clothing)
    v (float): Air velocity in m/s (default is 0.1 m/s for indoor calm air)
    T_r (float): Mean radiant temperature in °C (default is equal to T_a if not provided)

    Returns:
    float: PMV value
    """
    # Constants
    M = Met * 58.15  # Metabolic rate in W/m² (1 Met = 58.15 W/m²)
    W = 0  # External work, assumed 0 W/m² for most indoor activities
    I_cl = Clo * 0.155  # Clothing insulation in m²K/W (1 Clo = 0.155 m²K/W)

    if T_r is None:
        T_r = T_a  # Assume mean radiant temperature is equal to air temperature

    # Clothing area factor
    f_cl = 1.0 + 0.2 * Clo

    # Calculate air vapor pressure in Pa
    p_a = RH / 100 * 6.112 * math.exp(17.67 * T_a / (T_a + 243.5))  # In hPa, convert to Pa

    # Convective heat transfer coefficient
    h_c = 12.1 * math.sqrt(v) if v > 0.1 else 2.38 * abs(T_a - T_r) ** 0.25

    # Calculate clothing surface temperature (T_cl)
    T_cl = 35.7 - 0.028 * (M - W) - h_c * (T_a - T_r)

    # Thermal load (L)
    L = (M - W) - 3.96 * 10 ** (-8) * f_cl * ((T_cl + 273) ** 4 - (T_r + 273) ** 4) \
        - f_cl * h_c * (T_cl - T_a) - 3.05 * 10 ** (-3) * (5733 - 6.99 * (M - W) - p_a) \
        - 0.42 * ((M - W) - 58.15) - 1.7 * 10 ** (-5) * M * (5867 - p_a) \
        - 0.0014 * M * (34 - T_a)

    # PMV calculation
    PMV = (0.303 * math.exp(-0.036 * M) + 0.028) * L
    PPD = 100 - 95 * math.exp(-0.03353 * PMV ** 4 - 0.2179 * PMV ** 2)

    return PMV, PPD
