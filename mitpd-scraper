#!/usr/bin/env python

import fitz
import tabula
import numpy as np
import argparse
import datetime
import urllib
import os

TEMP_FILENAME =  "/tmp/.mitpd_scraper_temp"

def print_day_entries(day, entries):
    print(day)
    print("------------------------")
    for entry in entries:
        print(entry)

    print()

def download_and_scrape_date(date: datetime.date):
    today_filename = f"{date:%B}_{date.day}_{date.year}.pdf"
    url_prefix = "https://police.mit.edu/sites/default/files/MIT-Police-Files/"
    url = url_prefix + today_filename

    print("Fetching log from url:", url)
    try:
        logfile = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return ["Something went wrong. There is probably no log file for this day."]

    with open(TEMP_FILENAME, 'wb') as f:
        f.write(logfile.read())

    day_entries = scrape_file(TEMP_FILENAME)

    os.remove(TEMP_FILENAME)

    return day_entries

def scrape_today(*args):
    """ gets the log file for today and prints the result """
    today = datetime.date.today()
    entries = download_and_scrape_date(today)
    print_day_entries(today, entries)
    

def scrape_last_week(*args):
    """
        downloads the log files for each day in the last 7 days,
        including today, and scrapes them.
    """
    today = datetime.date.today()
    days = {}
    for days_ago in range(6, -1, -1):
        date = today - datetime.timedelta(days=days_ago)
        day_entries = download_and_scrape_date(date)
        days[date] = day_entries

    for day, entries in days.items():
        print_day_entries(day, entries)


def scrape_file(filename):
    doc = fitz.open(filename)
    page = doc[0]

    # a list of thetext to search for to identify each column
    column_text = [
        "Date & Time Reported",
        "Inc Type",
        "Date & Time Occurred",
        "Address",
        "Comments",
        "Disposition"
    ]

    ############
    ## Find table bounding box
    ############

    col_x_offsets = []
    for _, text in enumerate(column_text):
        col_x_offsets.append(page.searchFor(text)[0].x0 - 3)
    table_left_x = col_x_offsets[0]

    top_left_text = "Date & Time Reported"
    table_top_y = page.searchFor(top_left_text)[0].y0

    bottom_text = "NO REPORTS OF RESIDENTIAL FIRES"
    table_bottom_y = page.searchFor(bottom_text)[0].y0

    table_right_x = page.searchFor(column_text[-1])[0].x1 + 3

    # print("column x offsets", col_x_offsets)

    # print(f"table corners: ({table_left_x}, {table_top_y}), ({table_right_x}, {table_bottom_y})")
    table_bounding_box = (table_top_y, table_left_x, table_bottom_y, table_right_x)

    #########
    ## Parse Table
    #########

    table = tabula.read_pdf(filename, pages = "all", multiple_tables = True, \
            pandas_options={'header': None}, stream=True, guess=False, \
            area=table_bounding_box, columns=col_x_offsets, silent=True)[0]

    # print(table)

    ##############
    ## Convert messy output to entries
    ##############

    entries = []
    current_entry = None
    for _, row in table.iterrows():
        row = list(row)
        if row[-1] == "OPEN":
            if current_entry:
                entries.append(current_entry)
            # start of an entry, next 2-3 rows will be that entry
            # until the next OPEN
            current_entry = {col: "" for col in column_text}
        # once we find the first row, look at each piece
        if current_entry is not None:
            for col_i, val in enumerate(row):
                # skip first column of nothing (?)
                if col_i == 0:
                    continue
                col_name = column_text[col_i-1]

                if val and val is not np.nan:
                    current_entry[col_name] += str(val) + " "

    if current_entry:
        entries.append(current_entry)

    # clean up output
    for entry in entries:
        for key, val in entry.items():
            entry[key] = val.strip()

    # print(entries)

    #############
    ## format to nice strings
    #############

    formatted_entries = []
    for entry in entries:
        formatted_entries.append(f"On {entry['Date & Time Occurred']} near {entry['Address']} - {entry['Inc Type']}: {entry['Comments']}")

    return formatted_entries


parser = argparse.ArgumentParser(description="Get a human-readable text format of an MITPD log file PDF.")

# have subparsers for different modes, each has a function to get the file and call the function. 

subparsers = parser.add_subparsers(required=True)

# "today" command
parser_today = subparsers.add_parser("today")
# don't have any arguments, could add some here with 
# parser_today.add_argument("whatever", type=xxx, default=x)
parser_today.set_defaults(func=scrape_today)

parser_week = subparsers.add_parser("lastweek")
parser_week.set_defaults(func=scrape_last_week)

args = parser.parse_args()
args.func(args)