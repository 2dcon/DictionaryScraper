from dataclasses import dataclass

DEFINITION_GROUP = '\n#def'
END_OF_ENTRY = '\n#eoe\n\n'
NEW_LINE = '$^'


@dataclass
class Entry:
    key: str
    text: str

def get_numbers(string: str):
    num_str = ''
    for char in string:
        if char.isnumeric():
            num_str += char
        else:
            break

    if num_str:
        num_int = int(num_str)
        return num_int
    else:
        return 0


def new_prop(prop: str, value: str):
    return f'\n{prop}={value}'


