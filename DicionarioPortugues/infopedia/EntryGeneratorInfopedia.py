import glob
import os
path = "def"

wordIdentifier = "class=\"dolEntrinfoEntrada\">"
wordEnd = "</h1>"

ipaIdentifier = "class=\"dolRegfonFonet\">"
ipaEnd = "</span>"

posIdentifier = "class=\"dolCatgramTbcat\">"
posEnd = "</span>"

etymIdentifier = "class=\"dolVverbeteEtim-corpo\">"
etymEnd = "</div>"

catIdentifier = "class=\"dolSubacepTbdom\">"
catEnd = "</span>"

defIdentifier = "class=\"dolAcepsRightCell\""
subDefIdentifier = "class=\"dolTraduzTrad\">"
subDefEnd = "</span>"

allText = ''


def getContent(start: int, end_mark: str, eof: int):
    len_mark = len(end_mark)
    limit = eof - len_mark

    global allText
    for end in range(start, limit):
        if allText[end: end + len_mark] == end_mark:
            return allText[start: end]

    return "content not found!"


def checkIdentifier(index: int, identifier: str):
    global allText
    return allText[index: index + len(identifier)] == identifier

def main():

    with open("infopedia.dict", 'w') as dict:
        for filename in sorted(glob.glob('def/*.html')):
            with open(filename) as file:
                entry = ''

                word = ''
                ipa = ''
                etym = ''
                category = ''

                definitions = []
                sub_definition = False

                global allText
                allText = file.read()
                eof = len(allText)

                found_word = False
                found_ipa = False
                found_etym = False

                i = 0
                while i < eof - 30:
                    if not found_word and checkIdentifier(i, wordIdentifier):
                        i += len(wordIdentifier)
                        word = getContent(i, wordEnd, eof)
                        entry += f'\nword={word}'
                        i += len(word)
                        found_word = True

                    elif not found_ipa and checkIdentifier(i, ipaIdentifier):
                        i += len(ipaIdentifier)
                        ipa = getContent(i, ipaEnd, eof)
                        entry += f'\nipa={ipa}'
                        i += len(ipa)
                        found_ipa = True

                    elif not found_etym and checkIdentifier(i, etymIdentifier):
                        i += len(etymIdentifier)
                        etym = getContent(i, etymEnd, eof)
                        entry += f'\nety={etym}'
                        i += len(etym)
                        found_etym = True

                    elif checkIdentifier(i, posIdentifier):
                        i += len(posIdentifier)
                        pos = getContent(i, posEnd, eof)
                        entry += f'\npos={pos}'
                        i += len(pos)

                    elif checkIdentifier(i, defIdentifier):
                        i += len(defIdentifier)
                        sub_definition = False

                    elif checkIdentifier(i, catIdentifier):
                        i += len(catIdentifier)
                        category = f"({getContent(i, catEnd, eof).strip()}) "

                    elif checkIdentifier(i, subDefIdentifier):
                        i += len(subDefIdentifier)
                        definition = getContent(i, subDefEnd, eof).strip()

                        if category:
                            definition = category + definition
                            category = ''

                        if sub_definition:
                            entry += '; ' + definition
                        else:
                            entry += f"\ndef={definition}"
                            sub_definition = True


                        i += len(definition)

                    i += 1
            entry += '\n<eoe>\n'
            dict.write(entry)

if __name__ == "__main__":
    main()