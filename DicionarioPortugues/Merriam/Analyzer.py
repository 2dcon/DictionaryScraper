# IN = 'merriam.dict'
# OUT = 'merriam_reformatted.dict'
IN = 'merriam_reformatted.dict'
OUT = 'merriam_reformatted0.dict'

def process_0():
    reformatted = []
    with open(IN, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('src='):
                continue

            if line.startswith('key=') and ',' in line:
                rl = line.split(',')[0] + '\n'
                print(rl)
                reformatted.append(rl)
                continue

            opened = False
            rl = ''
            for char in line:
                if opened:
                    if char == '>':
                        opened = False
                else:
                    if char == '<':
                        opened = True
                    else:
                        rl += char
            reformatted.append(rl)

    with open(OUT, 'w') as f:
        f.writelines(reformatted)


def process_1():
    with open(IN, 'r') as f:
        reformatted = []
        lines = f.read()

        num_defs = []

        for i in range(len(lines)):
            num_defs.append([])
            if lines[i].startswith('#def'):
                num_defs[-1].append(i)

            # print('\r', f'progress: {current}/{total}', end='')
            # current += 1

    with open(OUT, 'w') as f:
        f.writelines(reformatted)


def main():
    process_1()


if __name__ == "__main__":
    main()
