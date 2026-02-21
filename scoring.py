def calculate_score(signals):
    score = 0
    
    if signals.get("industry_match"):
        score += 20
    if signals.get("recent_funding"):
        score += 30
    if signals.get("ai_hiring"):
        score += 25
    if signals.get("automation_mentions"):
        score += 15
    if signals.get("expansion"):
        score += 10

    return score