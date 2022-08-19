IN = 'urls'
OUT = 'urls_filtered'


def main():
    # print(IN)
    with open(IN, 'r') as ifile:
        all_lines = ifile.readlines()
        print(f'read {len(all_lines)} lines')
        with open(OUT, 'w') as ofile:
            srtd = sorted(set(all_lines))
            ofile.writelines(srtd)
            print(f'{len(srtd)} lines after sorting')


if __name__ == "__main__":
    main()
