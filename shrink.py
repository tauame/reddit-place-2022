#!/usr/bin/python3

# @author tauame
# This script will download ALL csv files from https://placedata.reddit.com/data/canvas-history/index.html
# and merge them into a stripped down version.
# The script will also perform the following transformations over the data:
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

#because yes... Just publishing the files in chronological order would be too easy to parse.
read_order = [1,2,3,5,6,10,11,8,13,4,9,15,12,18,14,16,20,17,23,19,21,28,7,29,30,31,32,33,25,35,36,27,22,0,40,41,24,34,44,37,38,39,48,43,26,45,46,47,42,49,50,55,52,57,58,54,61,56,63,53,59,60,62,51,70,64,65,66,72,73,74,75,76,77,67,69,68,71]

for i in read_order:

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
        out[3] = out[3].replace("\"","")

        out.pop(1) #remove user_id, optional if you want to keep user_ids, comment this line

        print(";".join(out))
