"""
Flood Road Passability Assistant
--------------------------------
A Streamlit web application providing indicative road passability assessments
during flood conditions using user-supplied observations and a transparent,
deterministic rule-based scoring engine.
"""

from typing import Dict, List, Tuple
import streamlit as st


def assess_road(
    water_depth: int,
    road_condition: str,
    blockage: str,
    travel_mode: str
) -> Tuple[str, int, str, List[str], Dict[str, int]]:
    """
    Evaluates flood-related road passability based on observable inputs.

    Parameters:
        water_depth: Estimated water depth in centimeters (0–300).
        road_condition: Condition of road ('Normal', 'Damaged', 'Unknown').
        blockage: Level of obstruction ('None', 'Partial', 'Complete').
        travel_mode: Mode of travel ('Walking', 'Bike', 'Car').

    Returns:
        A tuple containing:
            - risk_level (str): 'PASSABLE', 'CAUTION', or 'AVOID'
            - total_score (int): Cumulative risk score
            - recommendation (str): Contextual safety recommendation
            - contributing_factors (List[str]): List of active adverse factors
            - score_breakdown (Dict[str, int]): Points assigned to each component
    """
    # 1. Water Depth Score
    if water_depth < 20:
        depth_score = 0
    elif water_depth < 50:
        depth_score = 2
    else:
        depth_score = 4

    # 2. Road Condition Score
    road_condition_scores = {
        "Normal": 0,
        "Unknown": 1,
        "Damaged": 2
    }
    road_score = road_condition_scores.get(road_condition, 0)

    # 3. Blockage Score
    blockage_scores = {
        "None": 0,
        "Partial": 2,
        "Complete": 4
    }
    blockage_score = blockage_scores.get(blockage, 0)

    # 4. Travel Mode Adjustment
    travel_mode_adjustment = 0
    if travel_mode == "Bike" and water_depth >= 20:
        travel_mode_adjustment = 1

    # Total Score Calculation
    total_score = depth_score + road_score + blockage_score + travel_mode_adjustment

    # Determine Risk Classification
    if total_score <= 2:
        risk_level = "PASSABLE"
        recommendation = (
            "The supplied conditions indicate relatively lower risk, but local conditions "
            "and official guidance should always be verified before traveling. Exercise standard care."
        )
    elif total_score <= 5:
        risk_level = "CAUTION"
        recommendation = (
            "Proceed with heightened caution. Observed hazards or water levels pose potential "
            "risks to vehicle and personal safety. Consider delaying travel or monitoring official local updates."
        )
    else:
        risk_level = "AVOID"
        recommendation = (
            "Avoid this route if possible and follow official local safety instructions "
            "or use a confirmed alternative."
        )

    # Compile Active Contributing Factors (strictly relevant to inputs)
    contributing_factors: List[str] = []

    if depth_score == 4:
        contributing_factors.append(f"High reported water depth ({water_depth} cm: ≥50 cm threshold)")
    elif depth_score == 2:
        contributing_factors.append(f"Moderate reported water depth ({water_depth} cm: 20–49 cm threshold)")

    if road_condition == "Damaged":
        contributing_factors.append("Damaged road surface reported")
    elif road_condition == "Unknown":
        contributing_factors.append("Uncertain or unverified road condition")

    if blockage == "Complete":
        contributing_factors.append("Complete physical road blockage reported")
    elif blockage == "Partial":
        contributing_factors.append("Partial physical road blockage reported")

    if travel_mode_adjustment > 0:
        contributing_factors.append("Increased exposure and instability for two-wheeler / bike in water depth ≥20 cm")

    if not contributing_factors:
        contributing_factors.append("No significant adverse risk factors detected in supplied inputs")

    score_breakdown = {
        "water_depth": depth_score,
        "road_condition": road_score,
        "blockage": blockage_score,
        "travel_mode": travel_mode_adjustment,
        "total_score": total_score
    }

    return risk_level, total_score, recommendation, contributing_factors, score_breakdown


def main():
    st.set_page_config(
        page_title="Flood Road Passability Assistant",
        page_icon="🌊",
        layout="centered"
    )

    # Application Header
    st.title("🌊 Flood Road Passability Assistant")
    st.subheader("An AI-assisted prototype for interpreting flood-related road conditions.")
    st.caption("Transparent decision-support tool powered by a deterministic, rule-based assessment engine.")

    # Safety Disclaimer
    st.info(
        "⚠️ **Safety Disclaimer:** This is a prototype decision-support tool based on user-provided "
        "information. It does not replace official emergency alerts, road closures, police instructions, "
        "disaster-management authorities, or local safety guidance. Flood conditions can change rapidly. "
        "Never enter moving or unknown floodwater."
    )

    # How It Works Expander
    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown(
            """
            1. **Enter Road Conditions:** Provide observable details including location, water depth, road state, obstruction level, and travel mode.
            2. **System Evaluation:** The deterministic risk engine evaluates individual hazards against standardized flood safety criteria.
            3. **Score Calculation:** Each factor contributes weighted points to an overall cumulative risk score.
            4. **Passability Classification:** The system outputs an indicative passability category (🟢 PASSABLE, 🟡 CAUTION, or 🔴 AVOID) with specific explanations.
            """
        )

    st.markdown("---")

    # User Input Form
    st.markdown("### 📝 Enter Observable Road Details")

    with st.form(key="road_assessment_form"):
        location = st.text_input(
            "Location / Road Name *",
            placeholder="e.g., Main Road, Thiruvallur",
            help="Enter the specific street, intersection, or landmark name. This field is required."
        )

        col1, col2 = st.columns(2)

        with col1:
            water_depth = st.number_input(
                "Estimated Water Depth (cm)",
                min_value=0,
                max_value=300,
                value=10,
                step=5,
                help="Estimated stagnant or observed floodwater depth on the road surface (0 to 300 cm)."
            )

            road_condition = st.selectbox(
                "Road Condition",
                options=["Normal", "Damaged", "Unknown"],
                index=0,
                help="Physical condition of the road surface beneath the water."
            )

        with col2:
            blockage = st.selectbox(
                "Road Blockage",
                options=["None", "Partial", "Complete"],
                index=0,
                help="Physical obstacles, fallen debris, stalled vehicles, or barriers on the route."
            )

            travel_mode = st.selectbox(
                "Travel Mode",
                options=["Walking", "Bike", "Car"],
                index=2,
                help="Intended mode of transport for assessing stability and hazard exposure."
            )

        submit_button = st.form_submit_button(label="Assess Road", type="primary")

    # Assessment Result Presentation
    if submit_button:
        # Input Validation
        if not location or not location.strip():
            st.warning("⚠️ Please enter a valid **Location / Road Name** before running the assessment.")
            return

        cleaned_location = location.strip()

        # Run Assessment Engine
        risk_level, total_score, recommendation, factors, breakdown = assess_road(
            water_depth=water_depth,
            road_condition=road_condition,
            blockage=blockage,
            travel_mode=travel_mode
        )

        st.markdown("---")
        st.markdown("### 📊 Assessment Results")

        # Visual indicator badge based on risk level
        if risk_level == "PASSABLE":
            st.success(f"### 🟢 Passability Status: **PASSABLE**")
        elif risk_level == "CAUTION":
            st.warning(f"### 🟡 Passability Status: **CAUTION**")
        else:
            st.error(f"### 🔴 Passability Status: **AVOID**")

        # Metrics display
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(label="Assessed Location", value=cleaned_location)
        with col_res2:
            st.metric(label="Calculated Risk Score", value=f"{total_score} pts")
        with col_res3:
            st.metric(label="Travel Mode Evaluated", value=travel_mode)

        # Recommendation section
        st.markdown("#### 💡 Recommendation")
        st.write(recommendation)

        # Contributing Factors section
        st.markdown("#### 🔍 Contributing Factors Considered")
        for factor in factors:
            st.markdown(f"- {factor}")

        # Transparent Score Calculation Breakdown
        with st.expander("📐 How was this score calculated?", expanded=True):
            st.markdown(
                f"""
                | Factor | Observed Value | Points Assigned | Rule Description |
                | :--- | :--- | :---: | :--- |
                | **Water Depth** | {water_depth} cm | **+{breakdown['water_depth']}** | 0–19 cm = 0, 20–49 cm = 2, 50–300 cm = 4 |
                | **Road Condition** | {road_condition} | **+{breakdown['road_condition']}** | Normal = 0, Unknown = 1, Damaged = 2 |
                | **Blockage** | {blockage} | **+{breakdown['blockage']}** | None = 0, Partial = 2, Complete = 4 |
                | **Travel Mode** | {travel_mode} | **+{breakdown['travel_mode']}** | Bike: +1 when water depth ≥ 20 cm; Walking/Car: 0 |
                | **Total Score** | — | **{breakdown['total_score']}** | **Sum of all applicable points** |
                """
            )
            st.markdown(
                """
                **Classification Thresholds:**
                - **0 to 2 points:** 🟢 **PASSABLE** (Relatively lower risk under stated conditions)
                - **3 to 5 points:** 🟡 **CAUTION** (Elevated hazard; caution or travel deferral advised)
                - **6 or more points:** 🔴 **AVOID** (High risk; route avoidance strongly recommended)
                """
            )


if __name__ == "__main__":
    main()
