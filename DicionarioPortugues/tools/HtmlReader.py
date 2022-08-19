from dataclasses import dataclass


@dataclass
def tagged_teext:
    text: str
    tag: str
    class_: str
    id_: str


def find_closing_index(string: str, tag: str):
    closing_index = 0

    string_len = len(string)
    tag_opening = f'<{tag}'
    tag_closing = f'</{tag}>'
    tag_len = len(tag_closing)

    depth = 0

    end = -1

    while end < string_len - 1:
        end += 1


        if string[end] == '<' and substring[end + 1] != '!':
            tp = get_type(substring[end: end + MAX_CON_LEN])
            if tp == t:
                if substring[end + 1] == '/':
                    if depth == 0:
                        return Extracted(substring[start: end].strip(), end - start)
                    else:
                        depth -= 1
                else:
                    depth += 1
            else:
                continue
    return None

    return closing_index



def get_tag(string: str):
    ctype = ''
    for char in string:
        if char == ' ' or char == '>':
            # print(f'type = {ctype}')
            return ctype
        elif char == '<' or char == '/':
            continue
        else:
            ctype += char


def get_tagged_texts(html: str):
    html_len = len(html)

    tagged_texts = []

    i = -1

    while i < html_len - 1:
        i += 1
        if html[i] == '<':
            tag_code = ''
            for j in range(i + 1, html_len):
                if html[j] == '>':
                    tag_code = html[i: j + 1]
                    break


    return tagged_texts
