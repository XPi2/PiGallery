import urllib.request
import csv
# import getopt
# import os

from bs4 import BeautifulSoup


def main():

    # TODO: Make easy category get than put manual url
    url = "https://en.wikipedia.org/w/index.php?title=Category:Abstract_expressionist_artists&pagefrom=Poliakoff%2C+Serge%0ASerge+Poliakoff#mw-pages"
    output_name = "AbsImp_painters2.csv"

    output_file = csv.writer(
            open(output_name, 'a', newline='', encoding="utf8"), delimiter=':')

    res = urllib.request.urlopen(url)
    html = BeautifulSoup(res, "lxml")

    scope = html.findAll("div", {"class": "mw-category-group"})
    for lists in scope:
        elements = lists.findAll('a')
        for element in elements:
            try:
                print(element['title'])
            except ImportWarning:
                continue
            output_file.writerow([element['title']])


if __name__ == "__main__":
    main()
