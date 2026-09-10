import re


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize(text):
    text = str(text).lower().strip()
    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


# =========================================================
# RESULT HELPER
# =========================================================

def result(rule, hazard, barrier, confidence):
    return {
        "sif_potential": "YES",
        "risk_level": "HIGH",
        "life_saving_rule": rule,
        "hazard": hazard,
        "barrier_failure": barrier,
        "confidence": confidence
    }


def safe_result():
    return {
        "sif_potential": "NO",
        "risk_level": "LOW",
        "life_saving_rule": "None",
        "hazard": "No significant SIF precursor detected",
        "barrier_failure": "None identified",
        "confidence": 0.90
    }


def default_result():
    return {
        "sif_potential": "NO",
        "risk_level": "LOW",
        "life_saving_rule": "None",
        "hazard": "General safety hazard",
        "barrier_failure": "Not identified",
        "confidence": 0.70
    }


def contains(text, phrases):
    return any(phrase in text for phrase in phrases)


# =========================================================
# MAIN ANALYZER
# =========================================================

def analyze_report(report):

    if not report or not isinstance(report, str):
        return {
            "sif_potential": "NO",
            "risk_level": "LOW",
            "life_saving_rule": "None",
            "hazard": "No report provided",
            "barrier_failure": "Not identified",
            "confidence": 0.50
        }

    text = normalize(report)

    # =====================================================
    # EXPLICITLY SAFE OBSERVATIONS
    # =====================================================

    safe_statements = [
        "no hazard",
        "no hazards",
        "no gas leak",
        "no gas leakage",
        "no gas detected",
        "no toxic gas",
        "no dangerous atmosphere",
        "oxygen level is normal",
        "oxygen level normal",
        "normal oxygen",
        "safe atmosphere",
        "atmosphere is safe",
        "no danger",
        "no significant risk",
        "no risk",
        "working safely",
        "worked safely",
        "work completed safely",
        "safely completed",
        "safe working condition",
        "no unsafe condition",
        "no unsafe conditions",
        "no confined space entry",
        "confined space not entered",
        "outside confined space",
        "outside the confined space",
        "no welding",
        "no hot work",
        "no electrical hazard",
        "energy properly isolated",
        "equipment properly isolated",
        "properly isolated",
        "fall protection provided",
        "harness used",
        "safety harness used",
        "proper pedestrian control",
        "pedestrian control was provided",
        "trench properly protected",
        "excavation properly protected"
    ]

    # Explicit safe sentence should normally override
    # simple mentions such as "welding", "ladder", etc.
    if contains(text, safe_statements):
        # Exception:
        # If the same report contains an explicit unsafe
        # condition, continue checking the hazard rules.
        unsafe_markers = [
            "without",
            "not properly",
            "not provided",
            "not followed",
            "failed",
            "failure",
            "unsafe",
            "exposed",
            "leak",
            "deficiency",
            "deficient",
            "collapsed",
            "collapse",
            "struck",
            "caught between",
            "near miss"
        ]

        if not contains(text, unsafe_markers):
            return safe_result()

    # =====================================================
    # 1. CONFINED SPACE
    # =====================================================

    confined = [
        "confined space",
        "enclosed space",
        "tank entry",
        "vessel entry",
        "manhole entry",
        "entered tank",
        "entered vessel",
        "entered manhole"
    ]

    confined_safe = [
        "no confined space entry",
        "confined space not entered",
        "outside confined space",
        "outside the confined space"
    ]

    confined_unsafe = [
        "without gas testing",
        "without gas test",
        "no gas testing",
        "no gas test",
        "without atmospheric testing",
        "without atmosphere testing",
        "without ventilation",
        "without permit",
        "without confined space permit",
        "low oxygen",
        "oxygen deficiency",
        "toxic gas",
        "dangerous atmosphere",
        "hazardous atmosphere",
        "gas detected"
    ]

    if contains(text, confined) and not contains(text, confined_safe):

        if contains(text, confined_unsafe) or contains(text, [
            "entered confined space",
            "entered a confined space",
            "inside confined space",
            "inside a confined space",
            "working in confined space",
            "working inside confined space",
            "worker entered"
        ]):
            return result(
                "Confined Space",
                "Dangerous atmosphere / oxygen deficiency",
                "Gas testing or confined-space controls not followed",
                0.95
            )

    # =====================================================
    # 2. HOT WORK
    # =====================================================

    hot_work = [
        "welding",
        "hot work",
        "gas cutting",
        "flame cutting",
        "cutting operation",
        "grinding"
    ]

    hot_work_unsafe = [
        "without fire protection",
        "without proper fire protection",
        "without fire watch",
        "without hot work permit",
        "without permit",
        "without proper precautions",
        "without precautions",
        "near flammable material",
        "near flammable materials",
        "flammable material nearby",
        "fire protection not provided",
        "fire watch not provided",
        "hot work controls not followed",
        "hot work precautions not followed",
        "unsafe welding",
        "unsafe hot work",
        "unsafe grinding"
    ]

    if contains(text, hot_work):

        if contains(text, hot_work_unsafe):
            return result(
                "Hot Work",
                "Fire / explosion",
                "Hot-work controls or fire prevention measures not followed",
                0.90
            )

    # =====================================================
    # 3. ENERGY ISOLATION / LOTO
    # =====================================================

    loto = [
        "lockout",
        "lock out",
        "tagout",
        "tag out",
        "loto",
        "energy isolation",
        "equipment isolation",
        "equipment isolated"
    ]

    loto_unsafe = [
        "not properly isolated",
        "not isolated",
        "without isolation",
        "isolation not done",
        "isolation failed",
        "equipment was not isolated",
        "equipment was not properly isolated",
        "equipment not isolated",
        "energy was not isolated",
        "energy not isolated",
        "lockout not completed",
        "lockout was not completed",
        "tagout not completed",
        "tagout was not completed"
    ]

    if contains(text, loto):

        if contains(text, loto_unsafe):
            return result(
                "Energy Isolation",
                "Uncontrolled energy",
                "Energy was not properly isolated",
                0.92
            )

    # =====================================================
    # 4. WORKING AT HEIGHT
    # =====================================================

    height = [
        "working at height",
        "work at height",
        "working from height",
        "fall from height",
        "scaffold",
        "scaffolding",
        "ladder"
    ]

    height_unsafe = [
        "without harness",
        "without safety harness",
        "without fall protection",
        "no fall protection",
        "fall protection not provided",
        "harness not used",
        "safety harness not used",
        "unprotected height",
        "edge without protection",
        "unsafe work at height",
        "working at height without"
    ]

    if contains(text, height):

        if contains(text, height_unsafe):
            return result(
                "Working at Height",
                "Fall from height",
                "Fall protection was not used or was inadequate",
                0.93
            )

    # =====================================================
    # 5. LINE OF FIRE
    # =====================================================

    line_of_fire = [
        "line of fire",
        "caught between",
        "crushing hazard",
        "pinch point",
        "struck by",
        "standing below suspended load",
        "worker in line of fire",
        "in the line of fire"
    ]

    line_safe = [
        "no line of fire",
        "not in the line of fire",
        "outside the line of fire"
    ]

    if contains(text, line_of_fire) and not contains(text, line_safe):
        return result(
            "Line of Fire",
            "Struck-by / caught-between / crushing",
            "Worker entered an unsafe line-of-fire zone",
            0.91
        )

    # =====================================================
    # 6. LIFTING OPERATIONS
    # =====================================================

    lifting_unsafe = [
        "standing below suspended load",
        "worker below suspended load",
        "without exclusion zone",
        "no exclusion zone",
        "exclusion zone not maintained",
        "unsafe lifting",
        "load dropped",
        "dropped load",
        "lifting controls not followed",
        "suspended load over workers",
        "load suspended over worker"
    ]

    lifting_general = [
        "lifting operation",
        "crane operation",
        "suspended load",
        "lifting equipment",
        "rigging",
        "crane"
    ]

    if contains(text, lifting_unsafe):
        return result(
            "Lifting Operations",
            "Dropped or suspended load",
            "Lifting-zone controls or exclusion zone not followed",
            0.89
        )

    # A simple "lifting" statement is not automatically SIF.
    if contains(text, lifting_general):
        if contains(text, [
            "unsafe",
            "without",
            "not followed",
            "not maintained",
            "not provided",
            "failed"
        ]):
            return result(
                "Lifting Operations",
                "Dropped or suspended load",
                "Lifting-zone controls or exclusion zone not followed",
                0.89
            )

    # =====================================================
    # 7. ELECTRICAL SAFETY
    # =====================================================

    electrical_unsafe = [
        "exposed live wire",
        "live wire exposed",
        "electric shock",
        "electric shock risk",
        "without electrical isolation",
        "electrical isolation not done",
        "working on live equipment",
        "working on live electrical equipment",
        "energized equipment",
        "live electrical equipment",
        "exposed electrical wire"
    ]

    if contains(text, electrical_unsafe):
        return result(
            "Electrical Safety",
            "Electric shock / arc flash",
            "Electrical isolation or protection was inadequate",
            0.91
        )

    # =====================================================
    # 8. EXCAVATION
    # =====================================================

    excavation_unsafe = [
        "without trench protection",
        "without excavation protection",
        "without shoring",
        "without proper shoring",
        "no trench protection",
        "no excavation protection",
        "trench protection not provided",
        "excavation protection not provided",
        "excavation collapse",
        "trench collapse",
        "cave in",
        "cave in",
        "unsafe excavation"
    ]

    if contains(text, excavation_unsafe):
        return result(
            "Excavation",
            "Cave-in / collapse",
            "Excavation protection or inspection was inadequate",
            0.88
        )

    # =====================================================
    # 9. VEHICLE SAFETY
    # =====================================================

    vehicle_words = [
        "vehicle",
        "truck",
        "forklift",
        "heavy vehicle",
        "mobile equipment"
    ]

    vehicle_unsafe = [
        "vehicle collision",
        "vehicle accident",
        "vehicle was reversing",
        "vehicle is reversing",
        "vehicle reversing",
        "reversing vehicle",
        "vehicle was moving",
        "vehicle movement",
        "reversing in the work area",
        "unsafe reversing",
        "reversing without",
        "without pedestrian control",
        "without proper pedestrian control",
        "no pedestrian control",
        "pedestrian struck",
        "vehicle struck worker",
        "vehicle near miss",
        "unsafe vehicle movement",
        "unsafe driving",
        "speeding",
        "driving without"
    ]

    # IMPORTANT:
    # This catches both:
    # "reversing vehicle"
    # and
    # "vehicle was reversing"

    if contains(text, vehicle_words) and contains(text, vehicle_unsafe):
        return result(
            "Vehicle Safety",
            "Vehicle collision / struck-by",
            "Vehicle or pedestrian-control measures were inadequate",
            0.87
        )

    # =====================================================
    # 10. HAZARDOUS ATMOSPHERE
    # =====================================================

    atmosphere_unsafe = [
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

    atmosphere_safe = [
        "no gas detected",
        "no gas leak",
        "no gas leakage",
        "no toxic gas",
        "oxygen level is normal",
        "oxygen level normal",
        "normal oxygen",
        "safe atmosphere",
        "atmosphere is safe"
    ]

    if contains(text, atmosphere_unsafe):

        if not contains(text, atmosphere_safe):
            return result(
                "Hazardous Atmosphere",
                "Toxic / flammable atmosphere",
                "Atmospheric monitoring or gas control was inadequate",
                0.94
            )

    # =====================================================
    # 11. OTHER CLEARLY UNSAFE CONDITIONS
    # =====================================================

    generic_high_risk = [
        "serious injury",
        "potential fatality",
        "fatality risk",
        "life threatening",
        "life-threatening",
        "major incident",
        "critical safety violation"
    ]

    if contains(text, generic_high_risk):
        return result(
            "General Critical Safety",
            "Potential serious injury / fatality",
            "Critical safety control failure identified",
            0.80
        )

    # =====================================================
    # 12. SAFE OBSERVATION
    # =====================================================

    if contains(text, safe_statements):
        return safe_result()

    # =====================================================
    # 13. DEFAULT
    # =====================================================

    return default_result()