import numpy as np
from sympy import Matrix

P = np.array([[5, 7, 10], [13, 17, 7], [0, 5, 4]])  # Plain Text
C = np.array([[3, 6, 0], [14, 16, 9], [3, 17, 11]])  # Cipher Text

P_inv = Matrix(P).inv_mod(26)  #c=pkmod26
K = (Matrix(C)*P_inv) % 26     #k=c* p inverse mod 26

print("Key Matrix:")
print(K)