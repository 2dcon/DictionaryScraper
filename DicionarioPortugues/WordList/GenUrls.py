IN = 'filtered_3'
OUT = 'urls'
BASE_URL = 'https://www.infopedia.pt/dicionarios/lingua-portuguesa/'

def gen_urls():
    urls = []
    with open(IN, 'r') as f:
        words = f.readlines()
        for word in words:
            urls.append(BASE_URL + word)

    with open(OUT, 'w') as f:
        f.writelines(urls)


def main():
    gen_urls()


if __name__ == "__main__":
    main()
