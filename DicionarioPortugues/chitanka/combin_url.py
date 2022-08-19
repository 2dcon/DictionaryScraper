import os

DIR = 'word_list'
OUT = 'urls'

urls = []

for fileName in os.listdir(DIR):
    with open(f'{DIR}/{fileName}', 'r') as f:
        urls += f.readlines()

with open(OUT, 'w') as o:
    o.writelines(urls)

