words = []
verbs = []
non_verbs = []

with open('filtered', 'r') as wordlist:
    for line in wordlist:
        words.append(line)

non_verbs = words
i = 1
while i < len(non_verbs) - 1:
    word = non_verbs[i].strip()
    if len(word) >= 3:
        suffix = word[-2:]
        if suffix == 'ar' or suffix == 'er' or suffix == 'ir':
            # print(suffix)
            root = word[:-2]
            if root in non_verbs[i - 1] and root in non_verbs[i + 1]:
                verbs.append(word + '\n')
                while i > 1:
                    if non_verbs[i - 1].startswith(root):
                        non_verbs.pop(i - 1)
                        i -= 1
                    else:
                        break

                while i < len(non_verbs) - 1:
                    if non_verbs[i + 1].startswith(root):
                        non_verbs.pop(i + 1)
                    else:
                        break

    i += 1

# remove plurals
n = 1
while n < len(non_verbs):
    current = non_verbs[n].strip()
    previous = non_verbs[n - 1].strip()

    if current.endswith('s') and current[:-1] == previous:
        non_verbs.pop(n)
    else:
        n += 1

with open('verbs', 'w') as verbFile:
    verbFile.writelines(verbs)

with open('non_verbs', 'w') as nonVerbs:
    nonVerbs.writelines(non_verbs)
