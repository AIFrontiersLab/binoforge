TERMINAL = {"completed", "failed"}

def is_terminal(state: str | None) -> bool:
    return state in TERMINAL
