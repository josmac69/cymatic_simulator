import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.colors import LightSource
from scipy.special import jv # Bessel function for circular patterns
from scipy.ndimage import gaussian_filter

# --- Fluid Properties ---
# rho: density (kg/m^3), sigma: surface tension (N/m), viscosity: blur radius
FLUIDS = {
    'Water': {'rho': 997, 'sigma': 0.072, 'viscosity': 0.0},
    'Alcohol': {'rho': 789, 'sigma': 0.022, 'viscosity': 0.2},
    'Glycerin': {'rho': 1260, 'sigma': 0.063, 'viscosity': 2.0},
    'Mercury': {'rho': 13500, 'sigma': 0.485, 'viscosity': 0.1} # High density, high surface tension
}

# --- Initial Parameters ---
INITIAL_SHAPE = 'circle'
INITIAL_FREQ = 50.0        # Initial sound frequency in Hz
INITIAL_FLUID = 'Water'
INITIAL_STYLE = 'Magma'
RESOLUTION = 80           # Grid density (reduced for 3D performance)
ANIMATION_SPEED = 0.5

# --- Light Source ---
ls = LightSource(azdeg=315, altdeg=45)

# Create the Coordinate System
x = np.linspace(-1, 1, RESOLUTION)
y = np.linspace(-1, 1, RESOLUTION)
X, Y = np.meshgrid(x, y)

def get_z(t, shape, freq, fluid_name):
    """Calculates surface displacement based on physics approximations."""
    # Retrieve fluid properties
    props = FLUIDS[fluid_name]
    rho = props['rho']
    sigma = props['sigma']
    viscosity = props['viscosity']
    
    # Physics approximation: k ~ (rho/sigma)^(1/3) * f^(2/3)
    k = (rho / sigma)**(1/3) * (freq/10.0)**(2/3)
    
    # Map wavenumber k to mode numbers M and N
    M = max(1, int(k / 2))
    N = max(1, int(k))

    if shape == 'square':
        Z = np.sin(M * np.pi * X) * np.sin(N * np.pi * Y)
    else:
        R = np.sqrt(X**2 + Y**2)
        Theta = np.arctan2(Y, X)
        Z = jv(N, M * np.pi * R) * np.cos(N * Theta)
        Z[R > 1] = 0

    # Apply viscosity dampening (blur) to simulate viscous fluids
    if viscosity > 0:
        Z = gaussian_filter(Z, sigma=viscosity)

    # Time evolution (standing wave formula)
    return Z * np.cos(t * ANIMATION_SPEED * freq / 50.0)

# --- Visualization Setup ---
fig = plt.figure(figsize=(10, 8), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
plt.subplots_adjust(left=0.3, bottom=0.35) # Make room for UI

# Use the modified get_z signature
Z_init = get_z(0, INITIAL_SHAPE, INITIAL_FREQ, INITIAL_FLUID)
if INITIAL_STYLE == 'B&W Shadows':
    surf = ax.plot_surface(X, Y, Z_init, cmap='gray', lightsource=ls, rstride=2, cstride=2, antialiased=False)
else:
    surf = ax.plot_surface(X, Y, Z_init, cmap='magma', rstride=2, cstride=2, antialiased=False)
ax.axis('off')
ax.set_zlim(-1.5, 1.5)
ax.view_init(elev=45, azim=45)
title = plt.suptitle(f"Cymatic Pattern", color='white', fontsize=16)

# --- UI Elements ---
# Frequency Slider
ax_freq = plt.axes([0.3, 0.15, 0.5, 0.03], facecolor='lightgoldenrodyellow')
slider_freq = Slider(ax=ax_freq, label='Frequency (Hz)', 
                     valmin=10.0, valmax=300.0, valinit=INITIAL_FREQ)

# Elevation Angle Slider
ax_angle = plt.axes([0.3, 0.08, 0.5, 0.03], facecolor='lightgoldenrodyellow')
slider_angle = Slider(ax=ax_angle, label='Elevation Angle', 
                      valmin=0.0, valmax=90.0, valinit=45.0)

# Fluid Radio Buttons
ax_fluid = plt.axes([0.05, 0.5, 0.15, 0.25], facecolor='lightgoldenrodyellow')
fluid_radio = RadioButtons(ax_fluid, list(FLUIDS.keys()), 
                           active=list(FLUIDS.keys()).index(INITIAL_FLUID))

# Style Radio Buttons
ax_style = plt.axes([0.05, 0.8, 0.15, 0.15], facecolor='lightgoldenrodyellow')
style_radio = RadioButtons(ax_style, ['Magma', 'B&W Shadows'], 
                           active=0 if INITIAL_STYLE == 'Magma' else 1)

# Container Shape Radio Buttons
ax_shape = plt.axes([0.05, 0.2, 0.15, 0.15], facecolor='lightgoldenrodyellow')
shape_radio = RadioButtons(ax_shape, ['circle', 'square'], 
                           active=0 if INITIAL_SHAPE == 'circle' else 1)

def update_angle(val):
    ax.view_init(elev=val, azim=ax.azim)

slider_angle.on_changed(update_angle)

def update(frame):
    global surf
    t = frame * 0.1
    # Read current state from UI
    current_freq = slider_freq.val
    current_fluid = fluid_radio.value_selected
    current_shape = shape_radio.value_selected
    current_style = style_radio.value_selected
    
    # Generate new frame
    new_z = get_z(t, current_shape, current_freq, current_fluid)
    
    # Save current view limits to preserve user zoom/pan/rotation
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    zlim = ax.get_zlim()
    elev = ax.elev
    azim = ax.azim
    
    surf.remove()
    if current_style == 'B&W Shadows':
        surf = ax.plot_surface(X, Y, new_z, cmap='gray', lightsource=ls, rstride=2, cstride=2, antialiased=False)
    else:
        surf = ax.plot_surface(X, Y, new_z, cmap='magma', rstride=2, cstride=2, antialiased=False)
    
    # Restore view limits
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)
    ax.axis('off')
    ax.view_init(elev=elev, azim=azim)
    
    title.set_text(f"({current_shape.capitalize()}) Frequency: {int(current_freq)}Hz | Fluid: {current_fluid}")
    return surf, title

# Run Animation
ani = FuncAnimation(fig, update, frames=np.linspace(0, 1000, 200),
                    interval=50, blit=False) # blit=False handles dynamic title updates better

plt.show()