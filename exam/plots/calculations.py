import numpy as np

# e1
print("---------------e1--------------")
val = np.exp(- np.pi / 10)
print(f"e ^ (-pi/10): {val}")
val = np.cos(np.pi * np.sqrt(3) / 10)
print(f"cos(pi * sqrt(3) / 10: {val}")
val = np.sin(np.pi * np.sqrt(3) / 10)
print(f"sin(pi * sqrt(3) / 10: {val}")
# e2
print("---------------e2--------------")
val = np.exp(- np.pi / 5)
print(f"e ^ (-pi/5): {val}")
# e3
print("---------------e3--------------")

val = np.sin(np.pi * np.sqrt(3) / 10)
print(f"sin(pi * sqrt(3) / 10): {val}")

wc = np.pi * 4000
sqr3 = np.sqrt(3)
z1 = np.exp(-np.pi / 10) * (-wc * np.cos((np.pi * sqr3) / 10) + (sqr3 / 3) * wc * np.sin(np.pi * sqr3 / 10)) + np.exp(-np.pi / 5) * wc
print("-------z1----------")
print(f"z1: {z1}")

z2 = wc * np.exp(-np.pi / 5) + np.exp(-3 * np.pi / 10) * (-wc * np.cos(np.pi * sqr3 / 10) - sqr3 / 3 * wc * np.sin(np.pi * sqr3 / 10))
print("-------z2----------")
print(f"z2: {z2}")

print("-------denum-----")
print("-------z1--------")
z1 = np.exp(-np.pi / 10) * 2 * np.cos(np.pi * sqr3 / 10) + np.exp(-np.pi / 5)
print(f"z1: {z1}")

print("-------z2--------")
z2 = np.exp(- 3 * np.pi * 10) * 2 * np.cos(np.pi * sqr3 / 10) + np.exp(-np.pi / 5)
print(f"z2: {z2}")

print("-------z3--------")
z3 = np.exp(- 2 * np.pi / 5)
print(f"z3: {z3}")