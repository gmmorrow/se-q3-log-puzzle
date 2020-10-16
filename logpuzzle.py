#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    puzzle_urls = []
    pth = "http://" + "".join(filename.replace('animal_', ""))
    print(pth)
    
    with open(filename, 'r') as f:
        for position in f:
            url_result = re.findall(r'GET (\S+) HTTP', position)
            for match in url_result:
                if match not in puzzle_urls and 'puzzle' in match:
                    puzzle_urls.append(match)
    
    puzzle_urls.sort(key=lambda x: x[-9:-4])
    puzzle_urls = list(map(lambda tag: pth + tag, puzzle_urls))
    print(puzzle_urls)
    return puzzle_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # start to write out the new index.html
    index_html = '<html> \n <body> \n'

    for url in img_urls:
        img_dest = dest_dir + '/img' + str(img_urls.index(url))
        download_images(url, img_dest)
        index_html += '<img src="../' + img_dest + '"/>'

    index_html += '\n</body> \n </html>'

    with open(dest_dir + "/index.html", "w") as index_html_file:
        index_html_file.write(index_html)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
