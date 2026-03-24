def get_allowed_departments(role: str):
    role = role.lower()

    if role == "admin":
        return ["engineering", "finance", "hr", "marketing", "general"]

    elif role == "hr":
        return ["hr", "general"]

    elif role == "finance":
        return ["finance", "general"]

    elif role == "marketing":
        return ["marketing", "general"]

    elif role == "engineering":
        return ["engineering", "general"]

    else:
        return ["general"]