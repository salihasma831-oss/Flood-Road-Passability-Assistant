# Flood Road Passability Assistant

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive, transparent, decision-support prototype built with Python and Streamlit to evaluate the indicative passability of flood-affected roads based on user-reported observations and deterministic risk scoring.

---

## Overview

During severe weather events and urban inundations, road infrastructure can deteriorate rapidly with standing floodwaters, hidden debris, sinkholes, and stalled traffic. Commuters often lack a straightforward method to contextualize observable road conditions before undertaking potentially dangerous journeys.

The **Flood Road Passability Assistant** allows users to input observable road characteristics (water depth, surface integrity, physical obstructions, and travel modality) and translates them into an intuitive, indicative classification:
- 🟢 **PASSABLE** (Score: 0–2)
- 🟡 **CAUTION** (Score: 3–5)
- 🔴 **AVOID** (Score: 6+)

The application prioritizes transparency: every assessment includes a clear point-by-point breakdown showing exactly which hazards contributed to the final score.

---

## Problem Statement

Flooding is one of the most frequent natural hazards affecting urban mobility. When navigating inundated streets:
- Water depth is deceptive and often masks potholes, dislodged manhole covers, or structural washouts.
- Motorized two-wheelers and passenger vehicles have distinct vulnerability thresholds compared to pedestrians or heavy transports.
- Commuters frequently attempt travel without structured risk interpretation, leading to vehicle stall, stranding, and life-threatening exposure to moving floodwaters.

---

## Proposed Solution

The Flood Road Passability Assistant provides an immediate, rule-based mobility risk evaluation interface:
1. **User-Provided Observation:** Gathers straightforward, qualitative, and quantitative inputs that can be observed on-site or reported via local neighborhood groups.
2. **Deterministic Risk Scoring:** Applies a standardized, reproducible weighting model that isolates distinct physical hazards.
3. **Actionable Recommendations:** Outputs categorized guidance with an itemized breakdown of contributing hazards.
4. **Safety Disclaimer:** Explicitly reinforces that the tool is an indicative decision aid, not an emergency dispatch or official authority feed.

---

## Key Features

- **Intuitive Streamlit Interface:** Modern, clean, and responsive design optimized for mobile and desktop screens.
- **Robust Input Validation:** Safeguards against empty location entries and restricts numeric inputs to realistic bounds (0 to 300 cm).
- **Multi-Factor Risk Assessment:** Accounts for water depth, road damage, blockages, and vehicle vulnerability.
- **Explainable Point Breakdown:** Dedicated calculation audit view showing individual score contributions and thresholds.
- **Strictly Grounded Explanations:** Displays only relevant hazard factors without hallucinating absent risks.
- **Zero Heavy Dependencies:** Built cleanly with Python and Streamlit for lightweight deployment and rapid startup.

---

## How It Works

```
[ User Inputs ]
  ├── Location / Road Name (Required)
  ├── Estimated Water Depth (0–300 cm)
  ├── Road Surface Condition (Normal / Damaged / Unknown)
  ├── Obstruction / Blockage (None / Partial / Complete)
  └── Travel Mode (Walking / Bike / Car)
           │
           ▼
[ Deterministic Scoring Engine: assess_road() ]
  ├── Depth Score (0, 2, or 4 pts)
  ├── Surface Score (0, 1, or 2 pts)
  ├── Blockage Score (0, 2, or 4 pts)
  └── Vehicle Exposure (+1 pt for Bike if depth ≥ 20 cm)
           │
           ▼
[ Total Risk Score Calculation ]
  ├── 0–2 pts ──► 🟢 PASSABLE
  ├── 3–5 pts ──► 🟡 CAUTION
  └── 6+  pts ──► 🔴 AVOID
           │
           ▼
[ Presentation & Detailed Explanation ]
  ├── Status Badge & Metric Display
  ├── Contextual Safety Recommendation
  ├── Itemized Contributing Factors List
  └── Transparent Calculation Breakdown Table
```

---

## Risk Assessment Methodology

The assessment engine uses a transparent, additive point system:

### 1. Water Depth Score
| Depth Range | Risk Weight | Rationale |
| :--- | :---: | :--- |
| **0 – 19 cm** | **0 points** | Generally below typical vehicle floorboards and exhaust pipes. |
| **20 – 49 cm** | **2 points** | Poses risk of water intake, loss of control, and submerged hazards. |
| **50 – 300 cm** | **4 points** | Severe submersion hazard capable of floating light passenger cars. |

### 2. Road Condition Score
| Surface State | Risk Weight | Rationale |
| :--- | :---: | :--- |
| **Normal** | **0 points** | Paved, intact surface without visible structural defects. |
| **Unknown** | **1 point** | Water turbidity obscures surface integrity; caution warranted. |
| **Damaged** | **2 points** | Known potholes, washouts, broken pavement, or missing covers. |

### 3. Blockage Score
| Blockage Level | Risk Weight | Rationale |
| :--- | :---: | :--- |
| **None** | **0 points** | Route is clear of physical obstructions. |
| **Partial** | **2 points** | Debris, fallen branches, or stalled vehicles restrict lane width. |
| **Complete** | **4 points** | Physical barriers completely impede continuous vehicular progress. |

### 4. Travel Mode Adjustment
| Mode | Condition | Adjustment |
| :--- | :--- | :---: |
| **Walking** | Any water depth | 0 points |
| **Bike** | Water depth < 20 cm | 0 points |
| **Bike** | Water depth ≥ 20 cm | **+1 point** (Instability and balance loss in standing water) |
| **Car** | Any water depth | 0 points |

### 5. Final Classification Thresholds
- **🟢 PASSABLE (0–2 points):** Relatively lower risk based on supplied inputs; travel should still be accompanied by vigilance.
- **🟡 CAUTION (3–5 points):** Significant hazard factors present; consider deferring trip or monitoring local updates.
- **🔴 AVOID (6 or more points):** Hazardous conditions present; road traversal poses severe danger.

---

## Technology Stack

- **Core Language:** Python 3.10+
- **Frontend / Application Framework:** Streamlit (v1.30.0+)
- **Standard Library:** `typing` for static typing and structured return signatures
- **Version Control:** Git

---

## Project Structure

```
Flood-Road-Passability-Assistant/
│
├── app.py                     # Streamlit application & assessment engine
├── requirements.txt           # Minimal runtime dependencies
├── README.md                  # Complete project documentation
├── IBM_BOB_USAGE.md           # Documentation of IBM Bob's development role
├── sample_test_cases.md       # Validated test scenarios and mathematical proofs
├── .gitignore                 # Standard Python exclusions
└── assets/
    └── .gitkeep               # Directory placeholder for screenshots and media
```

---

## Installation

### Prerequisites
- Python 3.10 or later installed on your system.
- `pip` package installer.

### Steps
1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-username/Flood-Road-Passability-Assistant.git
   cd Flood-Road-Passability-Assistant
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   - **Windows:**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Launch the Streamlit web server:

```bash
streamlit run app.py
```

The application will launch locally at `http://localhost:8501`.

---

## Example Usage

1. Open the web interface in your browser.
2. Enter the target road: `Lakeview Avenue`.
3. Set the estimated water depth slider/input to `50 cm`.
4. Choose road condition: `Normal`.
5. Choose blockage: `None`.
6. Choose travel mode: `Car`.
7. Click **Assess Road**.
8. View the result:
   - **Status:** 🟡 **CAUTION**
   - **Score:** `4 pts`
   - **Recommendation:** Proceed with heightened caution. Observed hazards or water levels pose potential risks.
   - **Factors:** High reported water depth (50 cm: ≥50 cm threshold).
   - **Calculation:** Detailed audit table showing point distribution.

---

## Testing

Comprehensive test cases validating each threshold and boundary scenario are documented in [`sample_test_cases.md`](sample_test_cases.md).

To run the automated verification script from your terminal:

```bash
python -c "
from app import assess_road

test_cases = [
    (1, 5, 'Normal', 'None', 'Car', 0, 'PASSABLE'),
    (2, 20, 'Normal', 'None', 'Car', 2, 'PASSABLE'),
    (3, 50, 'Normal', 'None', 'Car', 4, 'CAUTION'),
    (4, 50, 'Damaged', 'Partial', 'Bike', 9, 'AVOID'),
    (5, 10, 'Normal', 'Complete', 'Car', 4, 'CAUTION'),
    (6, 30, 'Unknown', 'None', 'Bike', 4, 'CAUTION'),
]

for tid, d, r, b, m, es, ec in test_cases:
    risk, score, _, _, _ = assess_road(d, r, b, m)
    assert score == es and risk == ec, f'Test {tid} failed'
print('All 6 benchmark test cases verified successfully.')
"
```

---

## Limitations

- **Manual Input Dependency:** The current prototype relies entirely on user-observed data and does not have automated real-time sensory confirmation.
- **Static Depth Interpretation:** Does not measure water flow velocity, current, or rate of rise, which critically affect safety.
- **Qualitative Surface State:** Potholes or subsurface washouts may be hidden under turbid floodwaters even when reported as "Normal".
- **Rule-Based Engine:** Operates on deterministic thresholds rather than probabilistic machine learning models.

---

## Future Scope

1. **Hydrological & Weather Integration:** Connect to regional meteorological feeds and river gauge sensors for live depth estimations.
2. **GIS & Map Visualizations:** Integrate OpenStreetMap / Leaflet layers to display color-coded passability directly onto neighborhood maps.
3. **Real-Time Authority Road Closures:** Ingest official police, municipal corporation, and disaster response alerts.
4. **Crowdsourced Validation:** Allow users to submit geo-tagged, timestamped road-condition reports with upvoting / verification.
5. **Vehicle-Specific Calibration:** Expand travel modes with specific car chassis ground clearances and commercial transport profiles.
6. **Machine Learning Model:** Train predictive hazard classification models once a sufficiently validated historical urban flooding dataset is gathered.
7. **Multilingual Emergency Guidance:** Provide translations into regional languages (e.g., Tamil, Hindi, Telugu) for broader accessibility.

---

## Safety Disclaimer

> **IMPORTANT:** This application is a prototype decision-support tool based on user-provided information. It does not replace official emergency alerts, road closures, police instructions, disaster-management authorities, or local safety guidance. Flood conditions can change rapidly. Never enter moving or unknown floodwater.
