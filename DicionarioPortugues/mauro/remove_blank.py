IN = 'mauro_blank_removed.dict'
OUT = ''

props = ["key=", "word", "ipa=", "pos=", "ety=", "#def", "def=", "phr=", "com=", "des=", "#eoe"]


def remove_blank():
    blank_removed = []

    with open(IN, 'r') as ifile:
        lines = ifile.readlines()
        for line in lines:
            if not line.endswith('=\n'):
                blank_removed.append(line)

    with open(OUT, 'w') as ofile:
        ofile.writelines(blank_removed)


def find_irregulars():
    with open(IN, 'r') as ifile:
        lines = ifile.readlines()
        for line in lines:
            if line != '\n' and line[: 4] not in props:
                print(line)


if __name__ == "__main__":
    find_irregulars()
