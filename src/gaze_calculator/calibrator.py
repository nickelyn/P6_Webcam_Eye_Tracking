def handle_input(key: str, ver_ratio: float, hor_ratio: float):
    if key == "q" or key == "w":
        return ver_ratio
    elif key == "e" or key == "r":
        return hor_ratio
    else:
        return False
