# Interactive 3D Cymatic Simulator

A dynamic 3D Interactive Cymatic Wave Simulator built with Python and Matplotlib. It visually replicates the physical phenomena of cymatics (visible sound and vibration) by generating continuously updating, 3D topographical standing waves!

## Features

- **True 3D Visualization:** Maps structural cymatic modes dynamically onto a configurable 3D geometric grid using `matplotlib.mplot3d` surfaces.
- **Real-Time Interactive Controls:** Includes UI widgets to toggle between fluid types, modify base structural sound wave frequencies natively, and configure elevation angles without restarting the application!
- **Physics-Informed Patterning:** The geometry generation engine utilizes physical metrics of simulated fluids:
  - **Water, Alcohol, Glycerin & Mercury:** Adjusts geometric complexity dynamically based on the specific fluid's density ($\rho$) and surface tension ($\sigma$) parameters via an approximation of the geometric dispersion relation ($k \propto (\rho/\sigma)^{1/3} \times f^{2/3}$).
  - **Viscous Damping:** Employs structural gaussian blurring linearly tied to the fluid's mathematical viscosity—realistically damping high-frequency sharp structural edges for thick substances (like Glycerin).
- **Container Shape Architectures:** Simulate modal behaviors using both standard rectangular bounding (orthogonally combined 2D sine waves) or circular topology (Bessel function bounds).
- **Freely Navigable Context:** Supports standard mouse inputs for panning and zooming across the grid. The renderer intelligently respects and preserves manual zoom logic, pans, and user camera rotations natively between frame ticks!

## Quickstart & Installation

The repository includes an automated runtime script that safely constructs its own isolated Virtual Environment (`.venv`) and pulls the latest numerical dependencies.

1. Ensure you are running a Linux/Unix-based environment with `python3` installed natively.
2. Open your terminal inside the root directory and execute the wrapper script:
   ```bash
   ./run.sh
   ```
*(If you encounter permission issues, ensure it is executable via `chmod +x run.sh` first!)*

### Manual Installation
If you prefer not to use the automated runner script, you can install the dependencies conventionally:
```bash
pip install numpy matplotlib scipy
python3 simulator.py
```