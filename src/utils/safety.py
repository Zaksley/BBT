def safetyWeight(edge):
    weight = 1

    if edge.getSafety() == "safe":  weight = 0.1
    elif edge.getSafety() == "normal": weight = 1
    elif edge.getSafety() == "unsafe": weight = 1.5
    elif edge.getSafety() == "very_unsafe": weight = 2

    return weight
