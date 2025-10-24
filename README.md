# HorstFX-Robot-Palletizer

## Overview
This repository contains a comprehensive project on designing and implementing a **miniaturized robotic pallet stacking** scenario. The project demonstrates a hybrid approach that leverages **Python’s flexibility** and **HorstFX’s** advanced robotic control capabilities to optimize pallet stacking operations.

- **Control flow:** A JSON file defines the boxes and their target positions → Python sends this plan to the robot and starts the job → a HORST-side JS program performs the actual pick/place moves.
- **Interface:** Optional **Tkinter GUI** (`main.py`) to load a plan, set anchor offsets/speed, and launch.
- **Connectivity:** Python client (`client.py`) communicates with HorstFX over **XML-RPC**.

## Features
- Data-driven stacking: box size, pose, and approach are read from a JSON file.  
- Remote control: Python client uses the **HorstFX XML-RPC API**.  
- Robot-side logic in JS: HORST executes a JS program that consumes the JSON payload.  
- Simple GUI: `main.py` (Tkinter) to load a plan, set anchor offsets/speed, and start.  
- Gripper I/O: vacuum on/off and vacuum-OK check handled in the JS program.

## Installation
```bash
# (optional) create and activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
pip install numpy opencv-python matplotlib
```

> **Notes**
> - Tkinter is part of the standard library on most platforms.  
> - `tensorflow` is imported in `client.py` but not required for the basic flow; remove the import or install if needed.  
> - **Security:** Don’t commit robot IP/user/password. Use environment variables or a local, git-ignored config.

## Repository Layout
```
.
├─ complexPallete.json     # Example pallet + boxes definition (meters)
├─ StackingProgram.js      # HORST-side program (textual script for HorstFX)
├─ client.py               # Python XML-RPC client (commands, I/O, program start)
└─ main.py                 # Tkinter GUI + JSON injection into the JS program
```

## Requirements

**Robot / Controller**
- fruitcore **HORST 900** with **HorstFX** (textual scripting enabled).  
- PC ↔ controller network access (**XML-RPC**).

**PC**
- **Python 3.9+**  
- Packages listed above.

## How It Works
1. **Edit** a JSON plan with your pallet and box list (see schema below).  
2. **Start the GUI** (`python main.py`) or call the client API directly.  
3. The GUI **loads your JSON** and injects it into `StackingProgram.js` by replacing the `PUTHERE` placeholder (variable `Pattern1Create`).  
4. The Python client **uploads/starts** the JS program on HorstFX.  
5. The JS code **parses the JSON**, performs **pick → move → place** for each box using an approach strategy, and controls the **vacuum gripper I/O**.

## Quick Start
1. Configure connection in `client.py` (URL/IP/port and credentials). Prefer environment variables.  
2. Launch:
   ```bash
   python main.py
   ```
   - Select your JSON file (e.g., `complexPallete.json`)  
   - Set **Anchor X/Y** (pallet origin in robot frame) and **Speed** multiplier  
   - Click **START** (or **Start JS file** to run the robot program)  
3. Observe the robot executing the plan.

> **Headless option:** Call methods from `client.py` in your own script to start a plan without GUI.

## JSON Schema (Minimal)
```json
{
  "pallets": [
    {
      "palletNr": "001",
      "palletType": "Euro",
      "width": 0.30,
      "length": 0.20,
      "boxes": [
        {
          "product_code": "servo",
          "dim_x": 0.063, "dim_y": 0.064, "dim_z": 0.037,
          "x": 0.000, "y": 0.115, "z": 0.000,
          "approach": "7"
        }
      ]
    }
  ],
  "articles": { "0": { "description": "SingleItem", "weight": 1, "shippingGroup": "A" } },
  "orderID": ""
}
```

**Units:** meters for all lengths.  
**Approach codes:** `"3"`, `"5"`, `"7"`, `"9"` — numpad-style directions for the final approach vector before placing:
- **3** → from **+X, +Y**  
- **5** → from **+X, −Y**  
- **7** → from **−X, −Y**  
- **9** → from **−X, +Y**  

Choose the approach that avoids neighboring boxes/fixtures.

## Robot-Side Program (`StackingProgram.js`)
- Configures robot, tool, world frame and I/O (`StackingProgram.io`).  
- Expects a string variable **`Pattern1Create`** containing the JSON; parses it via `JSON.parse`.  
- Uses four approach functions (**Approach3/5/7/9**) plus a short **ApproachUp** retract.  

**Key parameters**
- `pat_x` / `pat_y` – pallet anchor in robot frame  
- `bld` / `bor` – blend radii for smooth motion  
- Speed ratios set per motion stage  

**I/O mapping** (adjust to your hardware)
- `TOOL_OUTPUT_1` → vacuum **ON/OFF**  
- `TOOL_OUTPUT_2` → **blow-off / release**  
- `TOOL_INPUT_1`  → vacuum **OK** (object detected)

## Python Components

### `main.py`
- Tkinter UI to:
  - Load a JSON plan  
  - Set **Anchor X / Y** and **Speed** multiplier  
  - Start the stacking cycle (runs the JS on the controller)  
- Injects your JSON into the JS by replacing the **`PUTHERE`** placeholder.

### `client.py`
- Wraps **HorstFX XML-RPC** calls (connect, moves, I/O, program start/stop, etc.).  
- Helper methods for robot motion and controller state.

## Safety Guidelines
- Start with **low speed** and a **single test box**.  
- Verify **TCP/tool data**, **payload**, and **world frame** in HorstFX.  
- **Dry-run** each approach code at safe heights to confirm clearances.  
- Keep an **E-Stop** reachable. Validate **vacuum I/O** mapping before production.

---

### Instruction on all 4 files
- **Main.py**  
- **Client.py**  
- **JavaScript File**  
- **JSON File**  

**HORST 900 Box Stacking (Python + JS)**  
Control and launch a pallet/box stacking routine on a fruitcore HORST 900 robot from your computer.  
A JSON file defines the boxes and their target positions, Python sends this plan to the robot and starts the job, and a HORST-side JS program performs the actual pick/place moves.
