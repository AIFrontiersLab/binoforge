from ops_gateway.catalog import TOOLS, known_tools

def require(name: str) -> dict:
    if name not in TOOLS:
        raise KeyError(name)
    return TOOLS[name]

def listed() -> list[str]:
    return known_tools()
