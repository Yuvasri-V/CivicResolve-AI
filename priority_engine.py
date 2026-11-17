
def assess_priority(title: str, description: str, category: str) -> dict:
    """
    Transparent prototype rules.
    Potentially dangerous reports are flagged for human review.
    This score is a triage aid, not a validated safety assessment.
    """
    text = f"{title} {description}".lower()

    score = 20
    reasons = []

    # Category-based baseline
    category_scores = {
        "Roads": 15,
        "Water": 15,
        "Electricity": 25,
        "Sanitation": 10,
        "Drainage": 20,
        "Safety": 30,
    }

    score += category_scores.get(category, 10)

    # Urgent risk indicators
    urgent_terms = [
        "sparking", "exposed wire", "electrocut",
        "trapped", "fire", "collapse", "life threatening",
        "gas leak", "serious injury"
    ]

    high_terms = [
        "school", "hospital", "flooding",
        "overflowing", "contaminated", "severe"
    ]

    urgent_flag = any(term in text for term in urgent_terms)

    if urgent_flag:
        score += 40
        reasons.append("Potential immediate hazard detected")
    elif any(term in text for term in high_terms):
        score += 20
        reasons.append("Possible elevated community risk")

    score = min(score, 100)

    if urgent_flag or score >= 80:
        level = "P1 - Urgent"
    elif score >= 60:
        level = "P2 - High"
    elif score >= 40:
        level = "P3 - Medium"
    else:
        level = "P4 - Low"

    return {
        "priority_score": score,
        "priority_level": level,
        "human_review_required": urgent_flag,
        "priority_reason": (
            "; ".join(reasons) if reasons
            else "Assigned using prototype category and keyword rules"
        ),
    }
