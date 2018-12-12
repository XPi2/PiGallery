import urllib.request
import sys
import getopt
import csv
import os

# from bs4 import BeautifulSoup
# from fuzzywuzzy import fuzz


def check_artists(artist, artists):
    if (len(artists) == 0):
        return True
    else:
        return artist in artists


def check_object_num(object_num, num_list):
    return object_num in num_list


# Returns list of csv lines that the artist matches
def match_lines(met_csv, artists, list_file):
    lines = []

    print(artists)
    if (list_file != ""):
        f = open(list_file, 'r')
        obj_num_list = []
        for line in f:
            obj_num_list.append(line.strip())

        for row in met_csv:
            if (check_object_num(row[0], obj_num_list)):
                lines.append(row)
    else:
        for row in met_csv:
            if (check_artists(row[2], artists)):
                lines.append(row)
    return lines


def download_lines(lines, out_dir, met_csv):
    image_names = []

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(os.path.join(out_dir, "piece_info.csv"), 'wb') as csv_file:
        im_writer = csv.writer(csv_file, delimiter=',')

        for row in met_csv:
            im_writer.writerow(row + ['Image Location'])
            break

        for line in lines:
            print(line[-2].strip())
            url = line[-2].strip()

            try:
                image_link = urllib.request.urlopen(url)
            except ImportError:
                image_names.append(None)
                print(line[-2].strip())
                print("URL Error")
                continue

            image_name = line[4].strip() + '-' + line[0].strip() + '.jpg'
            image_path = os.path.join(out_dir, image_name)

            with open(image_path, 'wb') as output:
                output.write(image_link.read())

            image_names.append(image_path)

            if image_names[-1] is None:
                continue
            # im_writer.writerow(line + [image_names[-1]])
    return image_names


def main(argv):
    opts, args = getopt.getopt(
            argv, "i:o:a:t:l:", ["csv=", "out=", "artist=", "type=", "list="])

    met_csv_file = ""
    out_dir = "gallery"
    list_file = "paintersDB"
    artists = []

    # types = []

    for opt, arg in opts:
        if opt in ("--csv", "-i"):
            met_csv_file = arg
        elif opt in ("--out", "-o"):
            out_dir = arg
        elif opt in ("--artist", "-a"):
            artists_file = arg
            # artists = arg.split(':')
        elif opt in ("--list", "-l"):
            list_file = arg

    met_csv = csv.reader(
            open(met_csv_file, 'rt', encoding="utf8"), delimiter=',')

    artist_csv = csv.reader(
            open(artists_file, 'rt', encoding="utf8"), delimiter=':')

    for row in artist_csv:
        artists.append(row[0])

    print(artists)

    csv_lines = match_lines(met_csv, artists, list_file)

    lines = 0
    for line in csv_lines:
        print(line[2] + ":" + line[5] + ":" + line[0])
        lines += 1
    print(lines)
    download_lines(csv_lines, out_dir, met_csv)


if __name__ == "__main__":
    main(sys.argv[1:])
