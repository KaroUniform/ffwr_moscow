from functools import reduce

def deepgetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    return reduce(lambda o, a: getattr(o, a, None), attr.split('.'), obj)

def del_command(text:str):
    return " ".join(text.split(' ')[1:])