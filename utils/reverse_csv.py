import csv


def main():
    input_file = "AbsImp_painters2.csv"
    output_file = "painters_AbsImp2.csv"

    input_csv = csv.reader(
            open(input_file, 'rt', encoding="utf8"), delimiter=':')
    output_csv = csv.writer(
            open(output_file, 'w', newline='', encoding="utf8"), delimiter=':')

    for line in input_csv:
        workLine = line[0].split()
        workLine.reverse()
        revList = ', '.join(workLine)
        output_csv.writerow([revList])


if __name__ == "__main__":
    main()
