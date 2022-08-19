def main():
    lines = []

    with open('urls_dup_removed', 'r') as urls:
        lines = urls.readlines()

    parts = []
    for i in range(0, len(lines)):
        if i % 50000 == 0:
            parts.append([])
        parts[-1].append(lines[i])

    for i in range(0, len(parts)):
        with open(f'part{i}', 'w') as part:
            part.writelines(parts[i])


if __name__ == "__main__":
    main()
