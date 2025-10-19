# HorstFX-Robot-Palletizer
This repository contains a comprehensive project on designing and implementing a miniaturized robotic pallet stacking scenario. The project demonstrates a hybrid approach that leverages Python’s flexibility and HorstFX’s advanced robotic control capabilities to optimize pallet stacking operations. 

Instruction on all 4 files.

Main.py

Client.py

JavaScript File

JSON File



HORST 900 Box Stacking (Python + JS)

Control and launch a pallet/box stacking routine on a fruitcore HORST 900 robot from your computer.
A JSON file defines the boxes and their target positions, Python sends this plan to the robot and starts the job, and a HORST-side JS program performs the actual pick/place moves.

Bachelor project (Mechatronics) — first public version.

⸻

Features
	•	Data-driven stacking: Box size, pose, and approach are read from a JSON file.
	•	Remote control: Python client uses the HorstFX XML-RPC API.
	•	Robot-side logic in JS: HORST executes a JS program that consumes the JSON payload.
	•	Simple GUI: main.py (Tkinter) to load a plan, set anchor offsets/speed, and start.
	•	Gripper I/O: Vacuum on/off and vacuum-OK check handled in the JS program.

⸻

Repository layout

.
├─ complexPallete.json     # Example pallet + boxes definition (meters)
├─ StackingProgram.js      # HORST-side program (textual script for HorstFX)
├─ client.py               # Python XML-RPC client (commands, I/O, program start)
└─ main.py                 # Tkinter GUI + JSON injection into the JS program


⸻

Requirements

Robot / Controller
	•	fruitcore HORST 900 with HorstFX (textual scripting enabled).
	•	PC ↔ controller network access (XML-RPC).

PC
	•	Python 3.9+
	•	Python packages (as used in the code):

pip install numpy opencv-python matplotlib

(Tkinter is part of the standard library on most platforms. tensorflow is imported in client.py but not required for the basic flow; remove the import or install if needed.)

Security: Don’t commit robot IP/user/password. Use environment variables or a local, git-ignored config.

⸻

How it works
	1.	Edit a JSON plan with your pallet and box list (see schema below).
	2.	Start the GUI (python main.py) or call the client API directly.
	3.	The GUI loads your JSON and injects it into StackingProgram.js by replacing the PUTHERE placeholder (variable Pattern1Create).
	4.	The Python client uploads/starts the JS program on HorstFX.
	5.	The JS code parses the JSON, performs pick → move → place for each box using an approach strategy, and controls the vacuum gripper I/O.

⸻

Quick start
	1.	Configure connection in client.py (URL/IP/port and credentials). Prefer environment variables.
	2.	Load the program:

python main.py

	•	Select your JSON file (e.g., complexPallete.json)
	•	Set Anchor X/Y (pallet origin on the table) and Speed multiplier
	•	Click START (or “Start JS file” to run the robot program)

	3.	Observe the robot executing the plan.

Headless option: Call methods from client.py in your own script to start a plan without GUI.

⸻

JSON schema (minimal)

{
  "pallets": [
    {
      "palletNr": "001",
      "palletType": "Euro",
      "width": 0.30,               // pallet width  (m)
      "length": 0.20,              // pallet length (m)
      "boxes": [
        {
          "product_code": "servo",
          "dim_x": 0.063, "dim_y": 0.064, "dim_z": 0.037,  // box size (m)
          "x": 0.000,  "y": 0.115,  "z": 0.000,            // target offset from pallet anchor (m)
          "approach": "7"                                  // placement approach: "3"|"5"|"7"|"9"
        }
        // ... more boxes
      ]
    }
  ],
  "articles": { "0": { "description": "SingleItem", "weight": 1, "shippingGroup": "A" } },
  "orderID": ""
}

Units: meters for all lengths.
Approach codes: "3", "5", "7", "9" — numpad-style directions for the final approach vector before placing:
	•	3 → from +X, +Y
	•	5 → from +X, −Y
	•	7 → from −X, −Y
	•	9 → from −X, +Y

Choose the approach that avoids neighboring boxes/fixtures.

⸻

Robot-side program (StackingProgram.js)
	•	Configures robot, tool, world frame and I/O (StackingProgram.io).
	•	Expects a string variable Pattern1Create containing the JSON; parses it via JSON.parse.
	•	Uses four approach functions (Approach3/5/7/9) plus a short ApproachUp retract.
	•	Key parameters:
	•	pat_x / pat_y – pallet anchor in robot frame
	•	bld / bor – blend radii for smooth motion
	•	Speed ratios set per motion stage
	•	I/O mapping (adjust to your hardware):
	•	TOOL_OUTPUT_1 → vacuum ON/OFF
	•	TOOL_OUTPUT_2 → blow-off / release
	•	TOOL_INPUT_1  → vacuum OK (object detected)

⸻

Python components

client.py
	•	Wraps HorstFX XML-RPC calls (connect, moves, I/O, start/stop program, etc.).
	•	Contains many helper methods for robot motion and controller state.

main.py (GUI)
	•	Tkinter UI to:
	•	Load a JSON plan
	•	Set Anchor X / Y and Speed multiplier
	•	Start the stacking cycle (and run the JS on the controller)
	•	Injects your JSON into the JS by replacing the PUTHERE placeholder.

⸻

Safety
	•	Start with low speed and a single test box.
	•	Verify TCP/tool data, payload, and world frame in HorstFX.
	•	Dry-run each approach code at safe heights to confirm clearances.
	•	Keep an E-Stop reachable. Validate vacuum I/O mapping before production.

⸻

Known issues / TODO
	•	In StackingProgram.js, one line uses shape_z for height; JSON uses dim_z. Change to dim_z to avoid mismatches.
	•	Only four corner approaches (3/5/7/9). Add more strategies if needed.
	•	Several constants (anchor, blend radii, pick grid) are hard-coded in the JS; consider parameterizing.
	•	Improve error handling and vacuum retry logic.
	•	Move credentials (IP/user/password) to environment variables and remove from source.

⸻

License

Add a license (e.g., MIT).

⸻

Acknowledgments
	•	fruitcore robotics — HORST 900 / HorstFX
	•	Supervisors/mentors for guidance and lab access