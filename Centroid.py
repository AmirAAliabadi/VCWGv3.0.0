import numpy as np

# Define the temperature range
temperature_range = np.arange(-1, 1, 0.01)

# Define the triangular membership functions manually
def trimf(x, abc):
    a, b, c = abc
    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0)

# Define the membership functions for N, Z, and P
N_membership = trimf(temperature_range, [-1, -1, 0])  # Negative
Z_membership = trimf(temperature_range, [-0.25, 0, 0.25])  # Zero
P_membership = trimf(temperature_range, [0, 1, 1])  # Positive

# Define the activation levels based on your rule table:
# These are the maximum activations for each fuzzy set from the rule table
activation_N = np.array([0.5, 0.5, 1, 0, 0, 0, 0, 0, 0])  # Activation of N in rules
activation_Z = np.array([0, 0, 0, 0.5, 0.5, 0, 0, 0, 0])  # Activation of Z in rules
activation_P = np.array([0, 0, 0, 0, 0, 1, 0, 0.3, 1])  # Activation of P in rules

# Apply the activation levels to each membership function
N_activated = activation_N * N_membership
Z_activated = activation_Z * Z_membership
P_activated = activation_P * P_membership

# Aggregate the membership functions (take the max of each membership at each point)
aggregated_membership = np.fmax(N_activated, np.fmax(Z_activated, P_activated))

# Calculate the centroid (center of gravity)
numerator = np.sum(temperature_range * aggregated_membership)
denominator = np.sum(aggregated_membership)
centroid = numerator / denominator

print("The centroid (defuzzified temperature) is:", centroid)
