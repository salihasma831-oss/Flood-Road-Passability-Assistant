# Sample Test Cases: Flood Road Passability Assistant

This document specifies the benchmark test cases used to validate the deterministic risk-scoring engine of the **Flood Road Passability Assistant**.

In accordance with system design principles, all classifications are derived strictly from the mathematical scoring rules without hidden overrides or ad-hoc adjustments.

---

## Scoring System Reference

### 1. Water Depth Score
| Range | Points |
| :--- | :---: |
| 0–19 cm | 0 |
| 20–49 cm | 2 |
| 50–300 cm | 4 |

### 2. Road Condition Score
| Option | Points |
| :--- | :---: |
| Normal | 0 |
| Unknown | 1 |
| Damaged | 2 |

### 3. Road Blockage Score
| Option | Points |
| :--- | :---: |
| None | 0 |
| Partial | 2 |
| Complete | 4 |

### 4. Travel Mode Adjustment
| Mode | Condition | Points |
| :--- | :--- | :---: |
| Walking | Any depth | 0 |
| Bike | Water depth ≥ 20 cm | +1 |
| Bike | Water depth < 20 cm | 0 |
| Car | Any depth | 0 |

### 5. Final Classification Thresholds
| Total Score | Status Indicator | Indicative Passability |
| :---: | :---: | :--- |
| **0 – 2** | 🟢 | **PASSABLE** |
| **3 – 5** | 🟡 | **CAUTION** |
| **6 or above** | 🔴 | **AVOID** |

---

## Test Scenarios

### TEST 1: Baseline Low-Water Scenario
- **Location:** Main Road, Thiruvallur
- **Inputs:**
  - Water Depth: `5 cm`
  - Road Condition: `Normal`
  - Blockage: `None`
  - Travel Mode: `Car`
- **Point Breakdown:**
  - Water depth (5 cm): 0 pts
  - Road condition (Normal): 0 pts
  - Blockage (None): 0 pts
  - Travel mode (Car): 0 pts
- **Total Calculated Score:** `0`
- **Expected Classification:** 🟢 **PASSABLE** (Score range: 0–2)
- **Contributing Factors Displayed:**
  - "No significant adverse risk factors detected in supplied inputs"
- **Recommendation:**
  - The supplied conditions indicate relatively lower risk, but local conditions and official guidance should always be verified before traveling. Exercise standard care.
- **Verification Status:** Passed (Validated via automated test runner)

---

### TEST 2: Threshold Boundary Scenario (Moderate Water)
- **Location:** Gandhi Road Junction
- **Inputs:**
  - Water Depth: `20 cm`
  - Road Condition: `Normal`
  - Blockage: `None`
  - Travel Mode: `Car`
- **Point Breakdown:**
  - Water depth (20 cm): 2 pts (reaches the 20–49 cm bracket)
  - Road condition (Normal): 0 pts
  - Blockage (None): 0 pts
  - Travel mode (Car): 0 pts
- **Total Calculated Score:** `2`
- **Expected Classification:** 🟢 **PASSABLE** (Score range: 0–2, upper boundary)
- **Contributing Factors Displayed:**
  - Moderate reported water depth (20 cm: 20–49 cm threshold)
- **Recommendation:**
  - The supplied conditions indicate relatively lower risk, but local conditions and official guidance should always be verified before traveling. Exercise standard care.
- **Note on Threshold:**
  - At exactly 20 cm, the water depth contributes 2 points. With all other hazards at baseline (0 pts), the total score remains at 2, representing the upper bound of the PASSABLE tier. If any secondary risk factor is present (such as an unknown road surface +1 pt or bike travel +1 pt), the cumulative score transitions directly into CAUTION (3 pts).
- **Verification Status:** Passed (Validated via automated test runner)

---

### TEST 3: Substantial Water on Normal Road
- **Location:** Lakeview Avenue
- **Inputs:**
  - Water Depth: `50 cm`
  - Road Condition: `Normal`
  - Blockage: `None`
  - Travel Mode: `Car`
- **Point Breakdown:**
  - Water depth (50 cm): 4 pts (reaches the 50–300 cm bracket)
  - Road condition (Normal): 0 pts
  - Blockage (None): 0 pts
  - Travel mode (Car): 0 pts
- **Total Calculated Score:** `4`
- **Expected Classification:** 🟡 **CAUTION** (Score range: 3–5)
- **Contributing Factors Displayed:**
  - High reported water depth (50 cm: ≥50 cm threshold)
- **Recommendation:**
  - Proceed with heightened caution. Observed hazards or water levels pose potential risks to vehicle and personal safety. Consider delaying travel or monitoring official local updates.
- **Verification Status:** Passed (Validated via automated test runner)

---

### TEST 4: Severe Multi-Hazard Road (High Water + Damage + Partial Blockage + Bike)
- **Location:** Riverbank Link Road
- **Inputs:**
  - Water Depth: `50 cm`
  - Road Condition: `Damaged`
  - Blockage: `Partial`
  - Travel Mode: `Bike`
- **Point Breakdown:**
  - Water depth (50 cm): 4 pts
  - Road condition (Damaged): 2 pts
  - Blockage (Partial): 2 pts
  - Travel mode (Bike with depth ≥ 20 cm): 1 pt
- **Total Calculated Score:** `4 + 2 + 2 + 1 = 9`
- **Expected Classification:** 🔴 **AVOID** (Score range: 6+)
- **Contributing Factors Displayed:**
  - High reported water depth (50 cm: ≥50 cm threshold)
  - Damaged road surface reported
  - Partial physical road blockage reported
  - Increased exposure and instability for two-wheeler / bike in water depth ≥20 cm
- **Recommendation:**
  - Avoid this route if possible and follow official local safety instructions or use a confirmed alternative.
- **Verification Status:** Passed (Validated via automated test runner)

---

### TEST 5: Complete Blockage on Shallow Water
- **Location:** North Overbridge Road
- **Inputs:**
  - Water Depth: `10 cm`
  - Road Condition: `Normal`
  - Blockage: `Complete`
  - Travel Mode: `Car`
- **Point Breakdown:**
  - Water depth (10 cm): 0 pts
  - Road condition (Normal): 0 pts
  - Blockage (Complete): 4 pts
  - Travel mode (Car): 0 pts
- **Total Calculated Score:** `0 + 0 + 4 + 0 = 4`
- **Expected Classification:** 🟡 **CAUTION** (Score range: 3–5)
- **Contributing Factors Displayed:**
  - Complete physical road blockage reported
- **Recommendation:**
  - Proceed with heightened caution. Observed hazards or water levels pose potential risks to vehicle and personal safety. Consider delaying travel or monitoring official local updates.
- **Architectural Design Note:**
  - In the current deterministic additive model, a complete blockage assigns 4 points, placing the route in the CAUTION band if water depth is negligible and road surface is normal. A planned future enhancement under evaluation is an explicit override rule whereby `Complete` blockage independently elevates any route to `AVOID`, regardless of water depth.
- **Verification Status:** Passed (Validated via automated test runner)

---

### TEST 6: Moderate Water, Uncertain Surface on Two-Wheeler
- **Location:** Old Bazaar Street
- **Inputs:**
  - Water Depth: `30 cm`
  - Road Condition: `Unknown`
  - Blockage: `None`
  - Travel Mode: `Bike`
- **Point Breakdown:**
  - Water depth (30 cm): 2 pts
  - Road condition (Unknown): 1 pt
  - Blockage (None): 0 pts
  - Travel mode (Bike with depth ≥ 20 cm): 1 pt
- **Total Calculated Score:** `2 + 1 + 0 + 1 = 4`
- **Expected Classification:** 🟡 **CAUTION** (Score range: 3–5)
- **Contributing Factors Displayed:**
  - Moderate reported water depth (30 cm: 20–49 cm threshold)
  - Uncertain or unverified road condition
  - Increased exposure and instability for two-wheeler / bike in water depth ≥20 cm
- **Recommendation:**
  - Proceed with heightened caution. Observed hazards or water levels pose potential risks to vehicle and personal safety. Consider delaying travel or monitoring official local updates.
- **Verification Status:** Passed (Validated via automated test runner)

---

## Test Execution Summary Table

| Test ID | Depth (cm) | Road Condition | Blockage | Travel Mode | Mathematical Score | Calculated Risk Level | Result |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TEST 1** | 5 | Normal | None | Car | **0** | 🟢 PASSABLE | PASS |
| **TEST 2** | 20 | Normal | None | Car | **2** | 🟢 PASSABLE | PASS |
| **TEST 3** | 50 | Normal | None | Car | **4** | 🟡 CAUTION | PASS |
| **TEST 4** | 50 | Damaged | Partial | Bike | **9** | 🔴 AVOID | PASS |
| **TEST 5** | 10 | Normal | Complete | Car | **4** | 🟡 CAUTION | PASS |
| **TEST 6** | 30 | Unknown | None | Bike | **4** | 🟡 CAUTION | PASS |
