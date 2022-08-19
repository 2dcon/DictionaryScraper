def main():
    dup_removed = []
    missing_lines = 0
    with open('urls', 'r') as url_file:
        lines = url_file.readlines()

        i = 0
        while i < len(lines) - 1:
            print(f"Comparing line {i}/{len(lines)}")

            j = i + 1
            while j < len(lines):
                if lines[i].split('/')[-1] == lines[j].split('/')[-1]:
                    j += 1
                else:
                    dup_removed.append(lines[i])
                    i = j
                    break

        checked = 0
        length = len(lines)
        while checked < length:
            print(f'Checking missing lines ({checked}/{length})')
            if lines[checked] not in dup_removed:
                missing_lines += 1
                print(f'missing line:\n{lines[checked]}')
            checked += 1

    if missing_lines == 0:
        # with open('urls_dup_removed', 'w') as url_refined:
        #     url_refined.writelines(dup_removed)
        print("Task finished without error.")
    else:
        print(f"{missing_lines} lines are missing!")


if __name__ == "__main__":
    main()
