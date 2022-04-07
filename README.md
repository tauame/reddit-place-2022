# reddit-place-2022
Working with Reddit's 2022 r/place public data

shrink.py script will download ALL csv files from https://placedata.reddit.com/data/canvas-history/index.html and merge them into a stripped down version.
The script perform the following transformations:
1. Change the timestamp format to a unixtimestamp integer
2. remove user_id column. You can comment the code if you want to keep this column, but in this case I'd suggest rehashing it with a smaller hash to keep the file small.
3. remove quotation marks from pixel coordinate column
4. change the column separators from commas to semi-colons

The script will write the CSV to the STDOUT. Redirect the output to file or pipe it into another program.

Sample usage:

`./shrink.py > canvas.csv`

Sample line from original files:

`2022-04-01 12:44:10.315 UTC,lEjremCtNoQaJ6KGBSWsatGEMXwjqoQqGZesWxHdyPetpAyFCsyShKzs5vkloRk7IIi1OrpftoO+fGwJ9zoKYA==,#7EED56,"42,42"`

Same line after being processed by shrink.py:

`1648827850315;#7EED56;42,42`
