PERCENT_CODE = {
    '%2F': '/',
    '%3F': '?',
    '%27': "'",
    '%28': '(',
    '%29': ')',
    '%2C': ',',
    '%20': ' '
}


def main():
    scraped = []
    with open('stat/list0612', 'r') as scr:
        for line in scr.readlines():
            reformatted = line.split('.')[0]
            # replace percent code
            for code, value in PERCENT_CODE.items():
                if code in reformatted:
                    reformatted = reformatted.replace(code, value)
            scraped.append(reformatted)

    remainders = []

    # with open('urls_dup_removed') as url_file:
    #     for line in url_file.readlines():
    #         word = line.split('/')[-1]
    #         if word not in scraped:
    #             remainders.append(line)

    with open('scraped.log', 'w') as scr:
        scr.writelines(scraped)

    with open('remainder', 'w') as result:
        result.writelines(remainders)


if __name__ == "__main__":
    main()