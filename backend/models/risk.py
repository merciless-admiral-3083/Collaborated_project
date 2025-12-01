# backend/models/risk.py

def analyze_country_risk(country_data):
    """Compute a realistic, dynamic country risk score."""

    political = country_data.get("political_stability", 5)
    economic = country_data.get("economic_health", 5)
    corruption = country_data.get("corruption_index", 5)
    conflict = country_data.get("conflict_level", 5)
    sanctions = country_data.get("sanctions_risk", 5)

    weights = {
        "political": 0.25,
        "economic": 0.25,
        "corruption": 0.20,
        "conflict": 0.20,
        "sanctions": 0.10,
    }

    score = (
        political * weights["political"] +
        economic * weights["economic"] +
        (10 - corruption) * weights["corruption"] +
        (10 - conflict) * weights["conflict"] +
        (10 - sanctions) * weights["sanctions"]
    )

    score_100 = round(score * 10, 2)

    if score_100 >= 75:
        risk = "Low Risk"
    elif score_100 >= 50:
        risk = "Moderate Risk"
    elif score_100 >= 30:
        risk = "High Risk"
    else:
        risk = "Severe Risk"

    return {
        "score": score_100,
        "risk_level": risk,
        "details": {
            "political": political,
            "economic": economic,
            "corruption": corruption,
            "conflict": conflict,
            "sanctions": sanctions
        }
    }
