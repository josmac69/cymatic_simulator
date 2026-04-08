import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ls = LightSource(azdeg=0, altdeg=65)
try:
    ax.plot_surface(X, Y, Z, cmap='gray', lightsource=ls)
    print("LIGHTSOURCE KWARG SUCCESS")
except Exception as e:
    print("FAILED:", e)
