def analyze_report(report):
    """
    Rule-based SIF precursor detector.

    Input:
        report (str) - Safety observation/report text

    Output:
        Structured SIF analysis
    """

    # ---------------------------------------------------------
    # Basic validation
    # ---------------------------------------------------------

    if not report or not isinstance(report, str):
        return {
            "sif_potential": "NO",
            "risk_level": "LOW",
            "life_saving_rule": "None",
            "hazard": "No report provided",
            "barrier_failure": "Not identified",
            "confidence": 0.50
        }

    report = report.lower().strip()

    # ---------------------------------------------------------
    # 0. SAFE / NORMAL CONDITIONS
    # ---------------------------------------------------------
    # Check safe statements BEFORE checking hazard keywords.
    # This prevents phrases like "no hazardous gas" from
    # being detected as a gas hazard.

    safe_phrases = [
        "no hazard",
        "no hazards",
        "no hazardous gas",
        "no hazardous gases",
        "no gas detected",
        "no gas leakage",
        "no gas leak",
        "oxygen level is normal",
        "oxygen level normal",
        "normal oxygen",
        "oxygen is normal",
        "safe atmosphere",
        "atmosphere is safe",
        "no dangerous atmosphere",
        "no danger",
        "no risk",
        "risk free",
        "safely completed",
        "safe working condition",
        "working safely",
        "no unsafe condition",
        "no unsafe conditions",
        "outside the confined space",
        "outside confined space",
        "no confined space entry",
        "confined space not entered",
        "no welding",
        "no hot work",
        "no electrical hazard",
        "energy properly isolated",
        "properly isolated",
        "fall protection provided",
        "harness used",
        "safety harness used"
    ]

    if any(phrase in report for phrase in safe_phrases):
        return {
            "sif_potential": "NO",
            "risk_level": "LOW",
            "life_saving_rule": "None",
            "hazard": "No significant SIF precursor detected",
            "barrier_failure": "None identified",
            "confidence": 0.90
        }

    # ---------------------------------------------------------
    # 1. CONFINED SPACE
    # ---------------------------------------------------------

    confined_space_keywords = [
        "confined space",
        "enclosed space",
        "tank entry",
        "vessel entry",
        "manhole entry",
        "entered tank",
        "entered vessel",
        "entered manhole"
    ]

    if any(keyword in report for keyword in confined_space_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Confined Space",
            "hazard": "Dangerous atmosphere / oxygen deficiency",
            "barrier_failure": "Gas testing or confined-space controls not followed",
            "confidence": 0.95
        }

    # ---------------------------------------------------------
    # 2. HOT WORK
    # ---------------------------------------------------------

    hot_work_keywords = [
        "welding",
        "hot work",
        "gas cutting",
        "cutting operation",
        "grinding",
        "flame cutting"
    ]

    if any(keyword in report for keyword in hot_work_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Hot Work",
            "hazard": "Fire / explosion",
            "barrier_failure": "Hot-work controls or fire prevention measures not followed",
            "confidence": 0.90
        }

    # ---------------------------------------------------------
    # 3. ENERGY ISOLATION / LOTO
    # ---------------------------------------------------------

    loto_keywords = [
        "lockout",
        "lock out",
        "tagout",
        "tag out",
        "loto",
        "energy isolation",
        "not isolated",
        "without isolation",
        "isolation not done",
        "isolation failed",
        "equipment not isolated"
    ]

    if any(keyword in report for keyword in loto_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Energy Isolation",
            "hazard": "Uncontrolled energy",
            "barrier_failure": "Energy was not properly isolated",
            "confidence": 0.92
        }

    # ---------------------------------------------------------
    # 4. WORKING AT HEIGHT
    # ---------------------------------------------------------

    height_keywords = [
        "working at height",
        "work at height",
        "working from height",
        "fall from height",
        "scaffold",
        "scaffolding",
        "ladder",
        "without harness",
        "without fall protection",
        "no fall protection",
        "unprotected height",
        "edge without protection"
    ]

    if any(keyword in report for keyword in height_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Working at Height",
            "hazard": "Fall from height",
            "barrier_failure": "Fall protection was not used or was inadequate",
            "confidence": 0.93
        }

    # ---------------------------------------------------------
    # 5. LINE OF FIRE
    # ---------------------------------------------------------

    line_of_fire_keywords = [
        "line of fire",
        "line-of-fire",
        "caught between",
        "crushing hazard",
        "pinch point",
        "struck by",
        "standing below suspended load",
        "in the line of fire",
        "worker in line of fire"
    ]

    if any(keyword in report for keyword in line_of_fire_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Line of Fire",
            "hazard": "Struck-by / caught-between / crushing",
            "barrier_failure": "Worker entered an unsafe line-of-fire zone",
            "confidence": 0.91
        }

    # ---------------------------------------------------------
    # 6. LIFTING OPERATIONS
    # ---------------------------------------------------------

    lifting_keywords = [
        "lifting operation",
        "lifting",
        "crane",
        "suspended load",
        "heavy load",
        "rigging",
        "lifting equipment",
        "load suspended",
        "crane operation"
    ]

    if any(keyword in report for keyword in lifting_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Lifting Operations",
            "hazard": "Dropped or suspended load",
            "barrier_failure": "Lifting-zone controls or exclusion zone not followed",
            "confidence": 0.89
        }

    # ---------------------------------------------------------
    # 7. ELECTRICAL
    # ---------------------------------------------------------

    electrical_keywords = [
        "electrical work",
        "electrical hazard",
        "electric shock",
        "live wire",
        "live electrical",
        "exposed wire",
        "energized equipment",
        "electrical equipment energized",
        "working on live equipment"
    ]

    if any(keyword in report for keyword in electrical_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Electrical Safety",
            "hazard": "Electric shock / arc flash",
            "barrier_failure": "Electrical isolation or protection was inadequate",
            "confidence": 0.91
        }

    # ---------------------------------------------------------
    # 8. EXCAVATION
    # ---------------------------------------------------------

    excavation_keywords = [
        "excavation",
        "excavated area",
        "trench",
        "trenching",
        "open pit",
        "excavation collapse",
        "trench collapse",
        "cave in",
        "cave-in"
    ]

    if any(keyword in report for keyword in excavation_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Excavation",
            "hazard": "Cave-in / collapse",
            "barrier_failure": "Excavation protection or inspection was inadequate",
            "confidence": 0.88
        }

    # ---------------------------------------------------------
    # 9. VEHICLE / DRIVING
    # ---------------------------------------------------------

    vehicle_keywords = [
        "vehicle collision",
        "vehicle accident",
        "unsafe driving",
        "speeding",
        "driving",
        "reversing vehicle",
        "vehicle movement",
        "pedestrian struck",
        "vehicle struck worker",
        "vehicle near miss"
    ]

    if any(keyword in report for keyword in vehicle_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Vehicle Safety",
            "hazard": "Vehicle collision / struck-by",
            "barrier_failure": "Vehicle or pedestrian-control measures were inadequate",
            "confidence": 0.87
        }

    # ---------------------------------------------------------
    # 10. HAZARDOUS ATMOSPHERE
    # ---------------------------------------------------------

    atmosphere_keywords = [
        "toxic gas",
        "gas leak",
        "gas leakage",
        "low oxygen",
        "oxygen deficiency",
        "oxygen level is low",
        "flammable gas",
        "dangerous atmosphere",
        "h2s",
        "hydrogen sulfide",
        "toxic fumes",
        "toxic vapor",
        "toxic vapour",
        "gas detected",
        "hazardous atmosphere"
    ]

    if any(keyword in report for keyword in atmosphere_keywords):

        return {
            "sif_potential": "YES",
            "risk_level": "HIGH",
            "life_saving_rule": "Hazardous Atmosphere",
            "hazard": "Toxic / flammable atmosphere",
            "barrier_failure": "Atmospheric monitoring or gas control was inadequate",
            "confidence": 0.94
        }

    # ---------------------------------------------------------
    # 11. NO SIF PRECURSOR DETECTED
    # ---------------------------------------------------------

    return {
        "sif_potential": "NO",
        "risk_level": "LOW",
        "life_saving_rule": "None",
        "hazard": "General safety hazard",
        "barrier_failure": "Not identified",
        "confidence": 0.70
    }