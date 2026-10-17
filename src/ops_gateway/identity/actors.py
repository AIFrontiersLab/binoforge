ACTORS = {
    "reader": {"role": "reader", "can_approve": False},
    "operator": {"role": "operator", "can_approve": True},
}

def known(actor: str) -> bool:
    return actor in ACTORS

def role_of(actor: str) -> str:
    record = ACTORS.get(actor)
    if record is None:
        return ""
    return record["role"]
