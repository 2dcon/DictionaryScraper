import glob
from dataclasses import dataclass
MAX_CON_LEN = 256

CLASS_END = 'widget more_defs'
CLASS_END_LEN = len(CLASS_END)

CLASS_WORD = 'hword'

CLASS_INFO = 'row headword-row'

CLASS_IPA = 'prs'

CLASS_IPA_VAR = 'pr'
CON_IPA_VAR = 'span'

CLASS_INF = 'vg-ins'

CLASS_POS = 'important-blue-link'
CLASS_POS_SUB = 'vd'

CLASS_POS_SUB = 'important-blue-link'

CLASS_DEF_GROUP = 'sb has-num'
CLASS_DEF_COM = 'drp'
CLASS_DEF = 'dtText'

CLASS_PHR = 'ex-sent'

CLASS_ET = 'et'

DIR = '/home/ferris/Documents/dict/html/merriam'
OUT = 'merriam.dict'
# OUT = 'sorting_test'

LOG = 'GenDict.log'

TEST_FILE = "/home/ferris/Documents/dict/html/merriam/apple.html"
# TEST_FILE = 'simple_test'


@dataclass
class dictEntry:
    keys: []
    text: str


def get_type(string: str):
    ctype = ''
    for char in string:
        if char == ' ' or char == '>':
            # print(f'type = {ctype}')
            return ctype
        elif char == '<' or char == '/':
            continue
        else:
            ctype += char


def get_class(container: str):
    label = 'class='
    len_label = len(label)

    i = -1
    while i < len(container) - len_label:
        i += 1
        if container[i: i + len_label] == label:
            clss = ''
            opened = False
            for char in container[i + len_label:]:
                if opened:
                    if char == '"':
                        return clss
                    clss += char
                elif char == '"':
                    opened = True

    return None


def get_container(string: str):
    start = 0
    for i in range(0, len(string)):
        if string[i] == '<':
            start = i
            break
    # print(f'start = {start}')
    # print(f'len(string) = {len(string)}')
    for end in range(start, len(string)):
        if string[end] == '>':
            return string[start + 1: end]


def get_word(string: str):
    word = ''
    opened = False
    for char in string:
        if char == '\n':
            return word
        if opened:
            if char == '>':
                opened = False
        elif char == '<':
            opened = True
        else:
            word += char


@dataclass
class Extracted:
    text: str
    section_length: int


def extract(substring: str, t: str):
    depth = 0

    start = 0
    end = 0

    for i in range(0, len(substring)):
        if substring[i] == '>':
            start = i + 1
            end = i
            break
    # print(f'@extract():\nstart = {start}\nlen(substring) = {len(substring)}')
    while end < len(substring) - 1:
        end += 1
        if substring[end] == '<' and substring[end + 1] != '!':
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


def extract_all(string: str, t: str, c: str):
    depth = 0

    extracted = []

    i = -1
    while i < len(string) - 1:
        i += 1

        if string[i] == '<' and string[i + 1] != '!':
            con = get_container(string[i: len(string)])
            tp = get_type(con)
            cl = get_class(con)
            i += len(con)
            if tp == t and cl == c:
                text = extract(string[i: len(string)], t).text
                extracted.append(text.strip())
    # print(extracted)
    return extracted


def em_2_i(string: str):
    new_string = ''
    ignoring = False
    i = 0
    while i < len(string):
        if string[i: i + 3] == '<em':
            ignoring = True
        if string[i: i + 5] == '</em>':
            ignoring = False

def read_file(file: str):
    with open(file, 'r') as f:
        html = f.read()

        entry = dictEntry(keys=[], text=f'src={file}\n')

        i = -1
        while i < len(html) - 1:
            i += 1

            if html[i] == '<' and html[i + 1] != '!':  # ignore comments
                con = get_container(html[i: i + MAX_CON_LEN])

                if not con:
                    # print('container not found!')
                    continue

                # print(f'con = {con}')
                tp = get_type(con)
                # print(f'type = {tp}')
                cl = get_class(con)

                # print(f"con={con}")
                i += len(con)

                if cl:
                    if cl == CLASS_END:
                        break
                    elif cl == CLASS_WORD:
                        word = get_word(html[i + 2:])
                        # print(f'word = {word}')
                        entry.keys.append(word.lower())

                        entry.text += f'word={word}\n'

                    elif cl == CLASS_IPA:
                        extracted = extract(html[i:], tp)
                        i += extracted.section_length

                        ipa = extracted.text
                        ipas = extract_all(ipa, CON_IPA_VAR, CLASS_IPA_VAR)

                        if ipa:
                            p = ''
                            for ip in ipas:
                                p += ip + ', '
                            entry.text += f'ipa={p[0: -2]}\n'
                        else:
                            print(f'{con}\nipa is empty')

                    elif cl == CLASS_POS:
                        extracted = extract(html[i:], tp)
                        i += extracted.section_length
                        pos = extracted.text

                        entry.text += f'pos={pos}\n'

                    elif cl.startswith(CLASS_POS_SUB):
                        text = extract(html[i:], tp)
                        sub = extract(text, 'a')
                        entry.text += f'spos={sub}'

                    elif cl.startswith(CLASS_DEF_GROUP):
                        entry.text += '#def\n'

                    elif cl == CLASS_DEF_COM:
                        extracted = extract(html[i:], tp)
                        i += extracted.section_length
                        combo = extracted.text

                        entry.text += f'#def\ncom={combo}\n'

                    elif cl == CLASS_DEF:
                        extracted = extract(html[i:], tp)
                        i += extracted.section_length
                        definition = extracted.text

                        if definition:
                            entry.text += f'def={definition}\n'

                    elif cl == CLASS_PHR:
                        extracted = extract(html[i:], tp)
                        i += extracted.section_length
                        phr = extracted.text

                        if phr:
                            entry.text += f'phr={phr}\n'
                    elif cl == CLASS_ET:
                        extracted = extract(html[i:], tp)
                        et = extracted.text
                        entry.text += f'ety={et}\n'
                        i += extracted.section_length

        entry.text += '#eoe\n\n'

        if not entry.keys:
            message = f'empty key at {file}\n'
            with open(LOG, 'a') as log:
                log.write(message)

        return entry


def gen_dict():
    entries = []

    file_list = glob.glob(f'{DIR}/*.html')

    total = len(file_list)

    for i in range(total):
        print('\r', f'progress: {i}/{total}', end='')

        entry = read_file(file_list[i])

        if entry.keys and entry.text:
            entries.append(entry)

    entries.sort(key=lambda x: x.key[0])
    print(f'Found {len(entries)} entries.')

    # print('\n\n' + len(entries))
    with open(OUT, 'w') as out:
        for entry in entries:
            key_line = 'key=' + ','.join(entry.keys) + '\n'
            out.write(key_line)
            out.write(entry.text)


def test():
    e = read_file(TEST_FILE)
    print(e.text)


def main():
    test()


if __name__ == "__main__":
    main()
