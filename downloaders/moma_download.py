import urllib.request
import urllib.error
import sys
import getopt
import csv
import os
import time

from bs4 import BeautifulSoup


def check_artists(artist, artists):
    if (len(artists) == 0):
        return True
    else:
        return artist in artists


def check_types(piece_type, types):
    if (len(types) == 0):
        return True
    else:
        return piece_type in types


def check_object_num(object_num, num_list):
    return object_num in num_list


# Returns list of csv lines that the artist matches
def match_lines(tate_csv, artists, types, list_file):
    lines = []

    print(artists)
    if (list_file != ""):
        f = open(list_file, 'r')
        obj_num_list = []
        for line in f:
            obj_num_list.append(line.strip())

        for row in tate_csv:
            if (check_object_num(row[2], obj_num_list)):
                lines.append(row)
    else:
        for row in tate_csv:
            if (check_artists(row[1], artists)
                    and check_types(row[13], types)):
                lines.append(row)

    return lines


def download_lines(lines, out_dir, tate_csv):
    image_names = []

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(os.path.join(out_dir, "piece_info.csv"), 'wb') as csv_file:
        im_writer = csv.writer(csv_file, delimiter=',')

        for row in tate_csv:
            im_writer.writerow(row + ['Image Location'])
            break

        for line in lines:
            print('ID: ', line[17].strip())
            url = urllib.request.Request(
                'http://www.moma.org/collection/works/' + line[17].strip())
            try:
                res = urllib.request.urlopen(url)
                time.sleep(2)
            except urllib.error.URLError:
                image_names.append(None)
                # print(line)
                print(urllib.error.URLError)
                print("URL Page Error")
                continue

            html = BeautifulSoup(res.read(), "lxml")
            # print(html)
            try:
                image_link = 'https://www.moma.org' + html.find(
                        'img', {'class': 'picture__img--focusable'})['src']
            except ImportError:
                continue

            if "noimage" not in image_link:
                print(image_link)

                image_name = line[1].strip() + '__' + line[17].strip() + ".jpg"

                image_path = os.path.join(out_dir, image_name)

                try:
                    image_file = urllib.request.urlopen(image_link)
                except urllib.error.URLError:
                    image_names.append(None)
                    print(urllib.error.URLError)
                    print("URL Link error")
                    continue

                with open(image_path, 'wb') as output:
                    output.write(image_file.read())

                image_names.append(image_path)

                if image_names[-1] is None:
                    continue
            else:
                continue

            # im_writer.writerow(line + [image_names[-1]])

    return image_names


def main(argv):
    opts, args = getopt.getopt(
            argv, "i:o:a:t:l:", ["csv=", "out=", "artist=", "type=", "list="])

    tate_csv_file = ""
    out_dir = ""
    list_file = ""
    artists = []

    types = []

    for opt, arg in opts:
        if opt in ("--csv", "-i"):
            tate_csv_file = arg
        elif opt in ("--out", "-o"):
            out_dir = arg
        elif opt in ("--artist", "-a"):
            artists_file = arg
            # artists = arg.split(':')
        elif opt in ("--type", "-t"):
            types = arg.split(":")
        elif opt in ("--list", "-l"):
            list_file = arg

    tate_csv = csv.reader(
            open(tate_csv_file, 'rt', encoding="utf8"), delimiter=',')

    artist_csv = csv.reader(
            open(artists_file, 'rt', encoding="utf8"), delimiter=':')

    for row in artist_csv:
        artists.append(row[0])
    print(artists)
    csv_lines = match_lines(tate_csv, artists, types, list_file)
    lines = 0

    for line in csv_lines:
        print(line[1] + " " + line[0] + " " + line[17])
        lines += 1
    print(lines)
    download_lines(csv_lines, out_dir, tate_csv)


if __name__ == "__main__":
    main(sys.argv[1:])
