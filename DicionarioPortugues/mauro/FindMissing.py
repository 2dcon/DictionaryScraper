URLS = 'urls'
SCRAPED = 'scrapy_output'
MISSING = 'missing'

LOG = 'GenDict.log'
OUT = 'incomplete'
BASE_URL = 'https://dizionario.internazionale.it/parola/'


def find_not_scraped():
    urls = []
    scraped = []
    missing = []

    with open(URLS, 'r') as ufile:
        urls = list(set(ufile.readlines()))

    with open(SCRAPED, 'r') as sfile:
        scraped = sfile.readlines()

    i = 0
    missing = 0
    while i < len(urls):
        print('\r', f'progress: {i}/{len(urls)}, found {missing} missing urls', end='')
        j = 0
        found = False
        while j < len(scraped):
            if urls[i].strip() in scraped[j]:
                urls.pop(i)
                scraped.pop(j)
                found = True
                break
            j += 1

        if not found:
            missing += 1
            i += 1

    with open(MISSING, 'w') as mfile:
        mfile.writelines(urls)


def find_incomplete():
    missing = []
    with open(LOG, 'r') as log:
        lines = log.readlines()
        for line in lines:
            if line.startswith('<section class='):
                missing.append(line.split('/')[-1])

    srtd = sorted(set(missing))

    with open(OUT, 'w') as out:
        for line in srtd:
            out.write(BASE_URL + line)


if __name__ == "__main__":
    find_incomplete()
