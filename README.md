# MITPD Log Scraper

## Overview

This is mostly a for-fun project to scrape the logs that the MIT police department posts online semi-daily. It grabs the PDF from the url using todays date, then finds the borders of the table and columns they report incidents in (because it's not the same every day, apparently) using `PyMuPDF`, and finally passes the table with the column splits into `tabula-py`, which does a *decent* of finding the text within each row. I do a bit more processing on that due to some funkiness in the way it turns out, and finally format it into a nice human-readable string. 

## Dependencies

There are a few dependencies to process the PDFs:

* Python 3
* `tabula-py` and its dependency `numpy`
* `PyMuPDF`

## Usage

There are currently two modes for the script---it will either show you the log file for today, or all the log files for the past 7 days. After navigating to the folder with the script inside, these can be executed as follows:

* `./mitpd-scraper today` to scrape today's log
* `./mitpd-scraper lastweek` to scrape the last week's worth of logs.
* `./mitpd-scraper -h` for some very basic help in case you forget.

You could also add the containing folder to your `$PATH` and just use it as `mitpd-scraper`, of course.