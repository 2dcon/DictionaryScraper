DICT_URL = 'https://www.merriam-webster.com/dictionary/'


def main():
    word_urls = []
    with open('urls') as url_file:
        for line in url_file.readlines():
            word = DICT_URL + line.split('/')[-1]
            word_urls.append(word)

    urls_sorted = sorted(word_urls)

    with open('urls', 'w') as file:
        for word in urls_sorted:
            file.write(word)


if __name__ == "__main__":
    main()