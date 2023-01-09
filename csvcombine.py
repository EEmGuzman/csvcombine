#!/usr/bin env python3

import os
import sys
import csv
import ntpath


def get_csv_paths(li_args):
    """
    Parameters
    ----------
    li_args :
        list that has file names/paths as elements or a single element with
        a directory.

    Returns
    -------
    fnames :
        list containing all csv file names
    """
    if len(li_args) == 1 and not(li_args[0].endswith('.csv')):
        fnames = [os.path.join(li_args[0], item) for item in os.listdir(li_args[0]) if item.endswith(".csv")]
    elif len(li_args) > 1:
        # If there are multiple args, they should all be the file names
        fnames = [item for item in li_args if item.endswith(".csv")]
    else:
        raise TypeError("Script args must either be a single directory or all file paths.")
    return fnames


def get_csv_header(full_fpath):
    """
    Parameters
    ----------
    full_fpath :
        path to a single csv file

    Returns
    -------
    row :
        list of csv field names (header)
    """

    with open(full_fpath) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            return row


def combine_csv_headers(all_fpaths):
    """
    Parameters
    ----------
    all_fpaths :
        list containing all of the csv files to be combined

    Returns
    -------
    unique_headers :
        list containing all unique field names from all csv files
    """
    unique_headers = []
    seen = set()

    for f in all_fpaths:  # make this more efficient?
        single_header = get_csv_header(f)
        for h in single_header:
            if h not in seen:
                seen.add(h)
                unique_headers.append(h)
    return unique_headers


def read_one_csv(p, h, wheader=True):
    """
    Parameters
    ----------
    p :
        path to single csv file
    h :
        list of field names for the csv file
    wheader :
        Write header to stdout

    Returns
    -------
    Writes each row of the csv file to stdout with a new column
    called 'filename'
    """
    with open(p) as f:
        final_h = h.copy()
        final_h.append('filename')  # Add column to show row origin file

        origin_filename = ntpath.basename(p)
        dreader = csv.DictReader(f, lineterminator='\n')
        dwriter = csv.DictWriter(sys.stdout, fieldnames=final_h,
                                 quoting=csv.QUOTE_NONNUMERIC,
                                 lineterminator='\n', escapechar='\\',
                                 doublequote=False)

        if wheader:
            dwriter.writeheader()

        for row in dreader:
            row["filename"] = origin_filename  # add val to final column
            dwriter.writerow(row)


def main(larg):
    """
    Parameters
    ----------
    larg: list of input arguments. Either a list with a directory or a list of files

    Returns
    -------
    Writes the combined CSV to stdout row by row
    """
    all_abs_paths = [os.path.abspath(n) for n in larg]
    fnames = get_csv_paths(all_abs_paths)
    hnames = combine_csv_headers(fnames)

    all_h = hnames.copy()
    all_h.append('filename')
    writer = csv.DictWriter(sys.stdout, fieldnames=all_h,
                            quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    writer.writeheader()
    del all_h

    for f in fnames:
        read_one_csv(f, hnames, wheader=False)


if __name__ == "__main__":
    main(sys.argv[1:])
