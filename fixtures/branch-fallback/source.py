def resolve(value, fallback=None):
    if value is None:
        return fallback
    if value == "":
        return ""
    try:
        number = int(value)
    except ValueError:
        return fallback
    if number < 0:
        return 0
    return number
