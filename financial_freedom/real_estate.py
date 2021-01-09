CASA_AMEGUINO = {
    "BUDGET": 65000,
    "HOUSE": 105000
}

CASA_DON_MATEO = {
    "LAND": 45000,
    "BUDGET": 75000
}


def total_allocation():
    projects = {**CASA_AMEGUINO, **CASA_DON_MATEO}
    total = 0
    for key, value in projects.items():
        total += value

    return round(total, 2)


print(total_allocation())
