

def strip_name_of_underscores_begin_end(name: str) -> str:
    # Remove underscores only at the beginning and end, not inside the string
    return name.lstrip('_').rstrip('_')

def add_underscored_to_name_begin_end(name: str) -> str:
    # adds 2 underscored before and 2 after the name
    return f"__{name}__"