import urllib.request
import sys
import getopt
import csv
import os

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

            if (check_object_num(row[0], obj_num_list)):
                lines.append(row)
    else:
        for row in tate_csv:
            if (check_artists(row[14], artists)
                    and check_types(row[24], types)):
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
            print('ID: ', line[3].strip())
            # You need to fill the user-agent and cookie [WIP]
            url = urllib.request.Request(
                'http://www.tatemuseum.org/art/collection/search/'
                + line[3].strip()
                # data=None,
                # headers={
                # 'User-Agent': '',
                # 'Cookie': 'visid_incap_1662004=;
                # incap_ses_510_1662004=;' + \
                # 'visid_incap_1661922=;
                # incap_ses_510_1661922=;'
                # }
            )
            try:
                res = urllib.request.urlopen(url)
            except ImportError:
                image_names.append(None)
                # print(line)
                print("URL Page Error")
                continue

            html = BeautifulSoup(res.read(), "lxml")
            # print(html)
            image_link = html.find(id="artwork__image")['src']

            if "noimage" not in image_link:
                print(image_link)
                image_name = image_link.split('/')[-2] + ".jpg"
                image_path = os.path.join(out_dir, image_name)
                try:
                    image_file = urllib.request.urlopen(image_link)
                except ImportError:
                    image_names.append(None)
                    print("URL Link error")
                    continue

                with open(image_path, 'wb') as output:
                    output.write(image_file.read())
                image_names.append(image_path)
                if image_names[-1] is None:
                    continue
            else:
                continue
            im_writer.writerow(line + [image_names[-1]])

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
        print(line[14] + " " + line[24] + " " + line[3])
        lines += 1

    print(lines)
    download_lines(csv_lines, out_dir, tate_csv)


if __name__ == "__main__":
    main(sys.argv[1:])
