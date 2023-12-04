__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2022, RGZM, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "florian.thiery@rgzm.de"
__status__ = "beta"
__update__ = "2022-12-09"

# import dependencies
import uuid
import requests
import io
import pandas as pd
import os
import codecs
import datetime
import importlib  # py3
import sys

# set UTF8 as default
importlib.reload(sys)  # py3
# reload(sys) #py2

# uncomment the line below when using Python version <3.0
# sys.setdefaultencoding('UTF8')

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set input csv
csv = "productioncentre.csv"
url = "https://www1.rgzm.de/ips/lod/" + csv

print(url)

# read csv file
data = pd.read_csv(
    url,
    encoding='utf-8',
    sep='|',
    usecols=['id', 'kilnregion', 'wikidata', 'label'],
    na_values=['.', '??']  # take any '.' or '??' values as NA
)
print(data.info())

# create triples from dataframe
lineNo = 2
outStr = ""
lines = []
for index, row in data.iterrows():
    # print(lineNo)
    tmpno = lineNo - 2
    if tmpno % 10 == 0:
        print(tmpno)
    lineNo += 1
    if str(row['kilnregion']) == 'Argonne':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132300" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'British':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132304" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'Central Gaulish':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132311" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'Dacian':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132318" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'East Gaulish':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132326" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'Helvetisch':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132334" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'Italian':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132343" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'Obergermanisch':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132348" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'Raetian':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132358" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'South Gaulish':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q102764958" + " /* " + str(row['id']) + "," + str(row['label']) + " */")
    if str(row['kilnregion']) == 'Spanish':
        lines.append(str(row['wikidata']) + "\t" + "P706" + "\t" + "Q103132368" + " /* " + str(row['id']) + "," + str(row['label']) + " */")

files = (len(lines) / 100000) + 1
print("lines", len(lines), "files", int(files))

# set output path
dir_path = os.path.dirname(os.path.realpath(__file__))

# write output files
print("start writing QS file")

f = 0
step = 100000
fileprefix = "wd_pc_kilnregion_"
for x in range(1, int(files) + 1):
    strX = str(x)
    filename = dir_path.replace("\\py", "\\ttl") + "\\" + fileprefix + strX + ".txt"
    file = codecs.open(filename, "w", "utf-8")
    i = f
    for i, line in enumerate(lines):
        if (i > f - 1 and i < f + step):
            file.write(line)
            file.write("\r\n")
    f = f + step
    print("Yuhu! > " + fileprefix + strX + ".txt")
    file.close()

print("*****************************************")
print("SUCCESS")
print("closing script")
print("*****************************************")
