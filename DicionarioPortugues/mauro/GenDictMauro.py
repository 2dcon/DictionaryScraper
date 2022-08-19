import glob
import multiprocessing
import sys
import timeit
import tqdm

from bs4 import BeautifulSoup, PageElement

from DicionarioPortugues.tools import EnoLex as enolex

ID_WORD = 'data-toggle-header'

CLASS_POS = 'qualifica'

DIR = '/home/ferris/Documents/dict/html/mauro'
HEADER = 'dict=De Mauro\n'
OUT = 'mauro.dict'
OUT_MP = 'mauro_mp.dict'
LOG = 'GenDict.log'

TEST_FILE = '/home/ferris/Documents/dict/html/mauro/aficionado'
# TEST_FILE = '/home/ferris/Documents/dict/html/test.html'

manager = multiprocessing.Manager()
shared_list = manager.list()
char_list = manager.list()


def remove_new_line(string: str):
    return string.replace('\n', '')


def add_log(message: str):
    with open(LOG, 'a') as log_file:
        log_file.write(message + '\n')


def read_html(html_file: str):
    with open(html_file, 'r') as f:
        key = ''
        entry_text = ''
        soup = BeautifulSoup(f, features="lxml")
        # word
        word_container = soup.find('h1', attrs={'data-toggle-header': ''})
        word_numbering = ''
        word_text = ''
        word = ''

        try:
            for child in word_container.children:
                if child.name == 'sup':
                    word_numbering = f' ({child.text.strip()})'
                elif not child.text.isspace():
                    word_text = remove_new_line(child.text.strip())
        except AttributeError:
            add_log(f'word_container not found in {html_file}')

        key = word_text
        word = word_text + word_numbering
        # except AttributeError:
        #     message = f'word_container not found in {html_file}\n'
        #     add_log(message)

        entry_text += enolex.new_prop('key', key)
        entry_text += enolex.new_prop('word', word)

        # pos
        pos = soup.find('span', attrs={'class': 'qualifica'})
        if pos:
            entry_text += enolex.new_prop('pos', pos.text.strip())

        ipa_and_ety = soup.findAll('section', attrs={'id': 'lemma_lemma'})
        if ipa_and_ety:
            # ipa
            ipa = ipa_and_ety[0].text.strip()
            entry_text += enolex.new_prop('ipa', ipa)

            # etymology
            if len(ipa_and_ety) >= 2:
                ety = remove_new_line(ipa_and_ety[1].text.strip())
                if ety:
                    entry_text += enolex.new_prop('ety', ety)

        # definitions
        section = soup.find('section', attrs={'id': 'descrizione'})
        current_number = 0
        try:
            def_not_numbered = True
            for child in section.children:
                print(f'child.name = {child.name}')
                print(f'child.text = {child.text}')
                if child.name == 'span' and child.has_attr('class'):
                    if child['class'][0] == 'ac':
                        def_not_numbered = False
                        found_number = enolex.get_numbers(child.text)
                        if current_number < found_number:
                            entry_text += enolex.DEFINITION_GROUP
                            current_number = found_number
                        entry_text += '\ndef='
                    elif child['class'][0] == 'mu':
                        continue
                elif child.name == 'i':
                    entry_text += child.__str__()
                elif child.text and not child.text.isspace():
                    def_text = remove_new_line(child.text)
                    if def_not_numbered:
                        entry_text += enolex.new_prop('def', def_text)
                        def_not_numbered = False
                    else:
                        entry_text += def_text

        except AttributeError:
            message = f'<section class="descrizione"> not found in {html_file}\n'
            add_log(message)

        # Polirematiche
        poli = soup.find('section', attrs={'id': 'polirematiche'})

        if poli:
            com = ''

            for child in poli.children:
                # skip the subtitle
                if child.name == 'h4':
                    continue
                elif child.name == 'strong':
                    com += f'\ncom={child.text}\ndes='
                elif child.name == 'br' and com[-1] != '=':
                    com += enolex.NEW_LINE
                else:
                    com += child.text

            entry_text += com.strip()

        # end of entry
        entry_text += enolex.END_OF_ENTRY

        return enolex.Entry(key, entry_text)


def process_all_files():
    file_list = glob.glob(f'{DIR}/*')
    entries = []

    for file in tqdm.tqdm(file_list):
        entries.append(read_html(file))

    entries.sort(key=lambda x: x.key)

    with open(OUT, 'w') as f:
        f.write(HEADER)
        for entry in entries:
            f.write(entry.text)


def process_file(file_name: str):
    shared_list.append(read_html(file_name))


def multiprocess_files():
    file_list = glob.glob(f'{DIR}/*')
    sample_list = []

    for i in range(64):
        sample_list.append(file_list[i])

    pl = multiprocessing.Pool(16)

    for _ in tqdm.tqdm(pl.imap(process_file, file_list), total=len(file_list)):
        pass

    entries = list(shared_list)
    entries.sort(key=lambda x: x.key)

    with open(OUT_MP, 'w') as out_mp:
        out_mp.write(HEADER)
        for entry in entries:
            out_mp.write(entry.text)


def get_sp_chars(file_name):

    with open(file_name, 'r') as f:
        all_text = f.read()
        length = len(all_text)
        i = 0
        while i < length - 10:
            if all_text[i] == '&':
                for j in range(i, i + 9):
                    if all_text[j] == ';':
                        char_code = all_text[i: j + 1]
                        if char_code not in char_list:
                            char_list.append(char_code)
                        i = j + 1
                        break

            i += 1


def multiprocess_chars():
    file_list = glob.glob(f'{DIR}/*')
    char_file = "char_code"

    pl = multiprocessing.Pool(16)

    for _ in tqdm.tqdm(pl.imap(get_sp_chars, file_list), total=len(file_list)):
        pass

    with open(char_file, 'w') as out_mp:
        for char in char_list:
            line = char + '\n'
            out_mp.write(line)


def gen_cpp_map():
    char_code = 'char_code'
    char_converted = 'char_converted'

    code = []
    converted = []

    with open(char_code, 'r') as f0:
        code_lines = f0.readlines()
        for line in code_lines:
            code.append(line.strip())

    with open(char_converted, 'r') as f1:
        converted_lines = f1.readlines()
        for line in converted_lines:
            converted.append(line.strip())

    print(len(code))
    print(len(converted))

    i = 0
    while i < len(code):
        print('{"' + code[i] + '", ' + converted[i] + "},")
        i += 1


def test():
    entry = read_html(TEST_FILE)
    print(entry.text)


def main():
    # multiprocess_files()
    # process_all_files()
    # multiprocess_chars()
    gen_cpp_map()

if __name__ == "__main__":
    main()
    # main()

