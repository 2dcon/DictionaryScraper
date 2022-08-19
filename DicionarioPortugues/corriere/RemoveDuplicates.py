def main():
    missing_lines = 0
    with open('urls', 'r') as url_file:
        lines = url_file.readlines()

    dup_removed = list(set(lines))

    with open('urls_sorted', 'w') as f:
        f.writelines(dup_removed)


if __name__ == "__main__":
    main()
