from bs4 import BeautifulSoup
from lxml import etree

TEST_FILE = '/home/ferris/Documents/dict/html/test.html'


def et_test():
    with open(TEST_FILE) as f:
        html = etree.HTML(f.read())
        section = html.xpath('//section')
        for child in section:
            print(child.tag)
            print(child.text)


def bs_test():
    with open(TEST_FILE) as f:
        soup = BeautifulSoup(f, 'html.parser')
        section = soup.findAll('section')
        for child in section[0].children:
            print(child.name)
            print(child.text)
            print('=============================================================')


def get_numbers(string: str):
    num_str = ''
    for char in string:
        if char.isnumeric():
            num_str += char
        else:
            break

    num_int = int(num_str)
    return num_int


def pointer_test(lst: []):
    lst.append('appended!')


def string_test(s: []):
    s[0] += 'added!'


def main():
    s = ['something ']
    string_test(s)
    print(s[0])


if __name__ == "__main__":
    main()
