IN = 'filtered_2'
OUT = 'filtered_3'
VERB_ENDING_FILE = 'ending0'
VERB_ENDINGS = []

def remove_plurals():
    words = []
    filtered = []
    with open(IN, 'r') as wl:
        words = wl.readlines()

    i = -1
    total = len(words)
    while i < total - 3:
        i += 1
        word = words[i]

        if '-' in word:
            continue

        if word.strip().endswith('a') and words[1 + i].strip().endswith('as') and words[i + 2].strip().endswith('o') and words[i + 3].strip().endswith('os'):
            word = words[i + 2]
            i += 3
        if words[i + 1].strip() == word.strip() + 's':
            i += 1

        filtered.append(word)
        print('\r', f'read {i}/{total} lines', end='')

    with open(OUT, 'w') as ofile:
        ofile.writelines(filtered)


def remove_oes():
    words = []
    filtered = []

    with open(IN, 'r') as ifile:
        words = ifile.readlines()

    for word in words:
        if not word.strip().endswith('ões'):
            filtered.append(word)

    with open(OUT, 'w') as ofile:
        ofile.writelines(filtered)


def gen_verb_ending_list():
    endings = []
    stripped_endings = []

    with open(VERB_ENDING_FILE, 'r') as vfile:
        endings = vfile.readlines()

    for ending in endings:
        stripped_endings.append(ending.strip())

    # print(f'len(endings) = {len(stripped_endings)}')
    return stripped_endings


def remove_conjugations():
    endings = gen_verb_ending_list()
    words = []
    filtered = []

    with open(IN, 'r') as ifile:
        words = ifile.readlines()

    i = 0
    total = len(words)
    len_endings = len(endings)
    conj = 0
    while i < total - len_endings:
        # print('\r', f'progress: {i}/{total}', end='')
        filtered += words[i]

        if words[i].strip().endswith(endings[0]):
            is_conj = True

            for j in range(1, len_endings):
                if not words[i + j].strip().endswith(endings[j]):
                    is_conj = False
                    break

            if is_conj:
                conj += 1
                i += len_endings
                continue

        i += 1

    print(f'found {conj} conjugations!')
    with open(OUT, 'w') as ofile:
        ofile.writelines(filtered)


def main():
    remove_conjugations()


if __name__ == "__main__":
    main()

