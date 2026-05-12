def predict_threat(report):

    report = report.lower()

    high_keywords = [
        "gun",
        "knife",
        "fight",
        "bomb",
        "attack",
        "terrorist",
        "kidnap",
        "fire",
        "shooting",
        "explosion",
        "blood",
        "suspicious person",
        "weapon",
        "intruder",
        "unauthorized access"
    ]

    medium_keywords = [
        "running",
        "shouting",
        "crowd",
        "unknown person",
        "external person",
        "teacher entered",
        "stranger",
        "panic"
    ]

    low_keywords = [
        "bird",
        "kid",
        "playing",
        "dog",
        "cat",
        "walking",
        "normal",
        "student"
    ]

    for word in high_keywords:
        if word in report:
            return "High"

    for word in medium_keywords:
        if word in report:
            return "Medium"

    for word in low_keywords:
        if word in report:
            return "Low"

    return "Medium"