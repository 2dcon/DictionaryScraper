import glob
import re
from dataclasses import dataclass
import string

from DicionarioPortugues.DictGenerator import dictEntry
from DicionarioPortugues.Merriam.GenDict import Extracted

MAX_CON_LEN = 256

CLASS_WORD = 'ch_wd'
ID_WORD = 'class="ch_wd">'
END_WORD = '</h1>'
END_WORD_LEN = len(END_WORD)
ID_WORD_LEN = len(ID_WORD)

CON_IPA = 'span'
CLASS_IPA = 'pron'
ID_IPA = 'class="pron">'
ID_IPA_LEN = len(ID_IPA)

START_SUBPOS = '<ul><li><span'
CLASS_POS = 'grl'
CON_POS = 'span'
ID_POS0 = 'class="grl">'
ID_POS0_LEN = len(ID_POS0)
ID_POS1 = '<ul><li><span class="grl">'
CLASS_SUBPOS = 'grl'

CLASS_DEF_COM = ''

CLASS_PARA = 'class="chapter-paragraph"'
CON_DEF_GROUP = '<p><strong>'
CON_DEF0 = '<strong>'
CON_DEF0_LEN = len(CON_DEF0)
CON_DEF1 = '<ul><li><strong>'
CON_DEF2 = '<ul><li>['

CLASS_PHR = 'em'

CON_LI = '<li>'
CON_LI_LEN = len(CON_LI)

DIR = '/home/ferris/Documents/dict/html/corriere/'
OUT = 'corriere.dict'
# OUT = 'test.dict'

TEST_FILE = '/home/ferris/Documents/dict/html/corriere/andare_1.shtml.html'
# TEST_FILE = 'simple_test'


def get_type(string: str):
    ctype = ''
    for char in string:
        if char == ' ' or char == '>':
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
    for end in range(start, len(string)):
        if string[end] == '>':
            return string[start + 1: end]


@dataclass
class WordInfo:
    word: str
    ipa: str
    pos: str
    info: str

    def __str__(self):
        s = f'word={self.word}\nipa={self.ipa}\npos={self.pos}\n'
        if self.info:
            s += f'info={self.info}\n'
        return s


def get_info(line: str):
    word = ''
    ipa = ''
    pos = ''
    info = ''

    i = 0
    while i < len(line) - END_WORD_LEN:
        if line[i: i + END_WORD_LEN] == END_WORD:
            i = i + END_WORD_LEN
            word_raw = line[: i].replace('<sup>', '(').replace('</sup>', ')')
            word = re.sub(r'<.*?>', '', word_raw)
        i += 1

    # while i < len(line) - ID_WORD_LEN:
    #     if line[i: i + ID_WORD_LEN] == ID_WORD:
    #         for j in range(i + ID_WORD_LEN, len(line)):
    #             if line[j] == '<':
    #                 i = j
    #
    #                 break
    #             else:
    #                 word += line[j]
    #         break
    #     i += 1

    while i < len(line) - ID_IPA_LEN:
        if line[i: i + ID_IPA_LEN] == ID_IPA:
            for j in range(i + ID_IPA_LEN, len(line)):
                if line[j] == '<':
                    i = j
                    break
                else:
                    ipa += line[j]
            break
        i += 1

    while i < len(line) - ID_POS0_LEN:
        if line[i: i + ID_POS0_LEN] == ID_POS0:
            for j in range(i + ID_POS0_LEN, len(line)):
                if line[j] == '<':
                    # len('</span>') = 6
                    i = j + 7
                    break
                else:
                    pos += line[j]
            break
        i += 1

    # there rest of the line to info
    while i < len(line):
        info += line[i]
        i += 1

    return WordInfo(word, ipa, pos, info)


def extract_all_text(substring: str):
    text = ''
    ignore = False
    for char in substring:
        if ignore:
            if char == '>':
                ignore = False
            continue
        elif char == '<':
            ignore = True
        else:
            text += char

    return text


def extract(substring: str, t: str):
    depth = 0

    start = 0
    end = 0

    for i in range(0, len(substring)):
        if substring[i] == '>':
            start = i + 1
            end = i
            break
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
            if tp == t and (not c or cl == c):
                text = extract(string[i: len(string)], t).text
                extracted.append(text.strip())
    return extracted


def get_numbered_def(line: str):
    # <em> -> <i>
    leading_text = ''
    strong = extract(line[7:], 'strong').text
    if not strong.isnumeric():
        leading_text = '#def\n' + re.sub(r'<.*?>', '', strong)

    # skip numbering
    following_text = re.sub(r'<strong>.*?</strong>', '', line)

    result = leading_text + following_text.replace('<em>', '<i>').replace('</em>', '</i>')

    return result

# def get_unnumbered_def(line: str):


def read_file(html_file: str):
    key = ''
    entry = ''

    with open(html_file) as f:
        lines = f.readlines()

        i = 0
        lines_len = len(lines)
        while i < lines_len - 1:
            if CLASS_WORD in lines[i]:
                first_line = get_info(lines[i].strip())
                entry += first_line.__str__()
                key = first_line.word

                break
            i += 1

        while i < lines_len - 1:
            line = lines[i].strip()
            # get definitions
            if CLASS_PARA in line:
                next_line = lines[i + 1].strip()
                if next_line.startswith(START_SUBPOS):
                    subpos = extract_all_text(next_line)
                    entry += f'#def\nsubpos={subpos}\n'
                elif next_line.startswith(CON_DEF0):
                    d = get_numbered_def(next_line).strip()
                    entry += f'def={d}\n'
                elif next_line.startswith(CON_DEF1):
                    d = extract(next_line[CON_DEF0_LEN:], 'strong').text
                    entry += f'#def\ndef={d}\n'
                elif next_line.startswith(CON_DEF2):
                    d = extract(next_line[6:], 'li').text
                    entry += f'#def\ndef={d}\n'

            i += 1

    entry += '#eoe\n\n'
    return dictEntry(key, entry)


def gen_dict():
    entries = []

    file_list = glob.glob(f'{DIR}/*.html')

    total = len(file_list)

    for i in range(total):
        print('\r', f'progress: {i}/{total}', end='')

        entry = read_file(file_list[i])

        if entry.key and entry.text:
            entries.append(entry)

    entries.sort(key=lambda x: x.key)
    print(f'\nFound {len(entries)} entries.')

    with open(OUT, 'w') as out:
        out.write('dict=Corriere\n\n')
        for entry in entries:
            key_line = f'key={entry.key}\n'
            out.write(key_line)
            out.write(entry.text)


def main():
    gen_dict()
    # read_file(TEST_FILE)


if __name__ == "__main__":
    main()
