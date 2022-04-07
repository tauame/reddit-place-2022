#!/usr/bin/python3

# This script will download ALL csv files from https://placedata.reddit.com/data/canvas-history/index.html
# and merge them into a stripped down version. 
# The script perform the following transformations:
#  1. Change the timestamp format to a unixtimestamp integer
#  2. remove user_id column (you can comment the code if you want to keep this column)
#  3. remove quotation marks from pixel coordinate column
#  4. change the column separators from commas to semi-colons
#
# The script will write the CSV to the STDOUT. Redirect the output to file or pipe it into another program.

import datetime
import fileinput
import requests
import gzip
import io

#timestamp format
ts_format_with_millis = '%Y-%m-%d %H:%M:%S.%f UTC'

#sometimes the milliseconds are missing
ts_format_without_millis = '%Y-%m-%d %H:%M:%S UTC'

for i in range(0,78):

    r = requests.get('https://placedata.reddit.com/data/canvas-history/2022_place_canvas_history-0000000000{:02d}.csv.gzip'.format(i), stream=True)
    lines = io.StringIO(gzip.decompress(r.content).decode('utf-8'))

    next(lines, None) # skip header line
    for line in lines:
        out = line.rstrip().split(",", 3)

        #if milliseconds are present
        if "." in out[0]:
            out[0] = str(int(datetime.datetime.strptime(out[0], ts_format_with_millis).timestamp()*1000))
        else:
            out[0] = str(int(datetime.datetime.strptime(out[0], ts_format_without_millis).timestamp()*1000))
        out[2] = out[2].replace("\"","")[:-1]

        out.pop(1) #remove user_id, optional if you want to keep user_ids, comment this line

        print(";".join(out))
