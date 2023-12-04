__author__ = "Florian Thiery, Dennis Gottwald"
__copyright__ = "MIT Licence 2020, RGZM, Florian Thiery"
__credits__ = ["Florian Thiery, Dennis Gottwald"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "thiery@rgzm.de"
__status__ = "beta"
__update__ = "2020-12-09"

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
csv = "discoverysite.csv"
url = "https://www1.rgzm.de/ips/lod/" + csv

print(url)

# read csv file
data = pd.read_csv(
    url,
    encoding='utf-8',
    sep='|',
    usecols=['id', 'label', 'lat', 'long', 'pleiadesid', 'ancientname', 'wkt', 'wikidata'],
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
    if tmpno % 1000 == 0:
        print(tmpno)
    lineNo += 1
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "rdf:type" + " lado:Location .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "rdf:type" + " lado:DiscoverySite .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "lado:hasType" + " lado:DiscoverySite .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "rdfs:label" + " " + "'" + str(row['label']).replace('\'', '`') + "'@en" + ".")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "dc:identifier" + " " + "" + str(row['id']) + "" + ".")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "lado:exactMatch" + " " + "wd:" + str(row['wikidata']) + " . ")
    if str(row['pleiadesid']).replace('\'', '`') != 'nan':
        if str(row['pleiadesid']).replace('\'', '`') != 'undefined':
            lines.append("samian:loc_ds_" + str(row['id']) + " " + "lado:pleiadesID" + " " + "" + str(row['pleiadesid']) + "" + ".")
            # pleiades modelling (https://github.com/pelagios/pelagios-cookbook/wiki/Joining-Pelagios#minimum-example)
            # An object you want to link to Pelagios
            lines.append("samian:loc_ds_" + str(row['id']) + " " + "rdf:type" + " pelagios:AnnotatedThing .")
            # Title and homepage URL are MANDATORY
            lines.append("samian:loc_ds_" + str(row['id']) + " " + "dcterms:title" + " " + "'" + str(row['label']).replace('\'', '`') + "'" + ".")
            lines.append("samian:loc_ds_" + str(row['id']) + " " + "foaf:homepage" + " " + "'<http://lod.archaeology.link/samian/>'" + ".")
            # Feel free to assign 'tags' to your data
            lines.append("samian:loc_ds_" + str(row['id']) + " dcterms:subject " + "'samian ware discovery site'" + ".")
            # Objects are 'annotated' with any number of gazetteer references
            lines.append("_:" + str(lineNo) + " " + " rdf:type " + "oa:Annotation .")
            # metadata
            lines.append("_:" + str(lineNo) + " " + " dcterms:creator " + "<http://www.wikidata.org/entity/Q90412636> .")
            lines.append("_:" + str(lineNo) + " " + " <http://www.w3.org/ns/activitystreams#generator> " + "<https://orcid.org/0000-0002-3246-3531> .")
            lines.append("_:" + str(lineNo) + " " + " dcterms:contributor " + "<https://orcid.org/0000-0002-7634-5342> .")
            lines.append("_:" + str(lineNo) + " " + " dcterms:contributor " + "<https://orcid.org/0000-0002-8761-4659> .")
            lines.append("_:" + str(lineNo) + " " + " dcterms:contributor " + "<https://orcid.org/0000-0002-3246-3531> .")
            lines.append("_:" + str(lineNo) + " " + " dcterms:issued " + "'" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") + "'^^xsd:dateTime .")
            # MANDATORY: the 'annotation target' is the URI of your object;
            # the 'annotation body' is the gazetteer reference
            lines.append("_:" + str(lineNo) + " " + " oa:hasTarget " + "samian:loc_ds_" + str(row['id']) + " .")
            lines.append("_:" + str(lineNo) + " " + " oa:hasBody " + "<http://pleiades.stoa.org/places/" + str(row['pleiadesid']) + "> .")
            # OPTIONAL: extra metadata about the nature of the place reference
            lines.append("_:" + str(lineNo) + " " + " pelagios:relation " + "relations:foundAt .")
            lines.append("_:" + str(lineNo) + " " + " oa:annotatedAt " + "'" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") + "'^^xsd:date .")
            lines.append("_:" + str(lineNo) + "_1 " + " cnt:chars '" + str(row['wkt']) + "' .")
            lines.append("_:" + str(lineNo) + "_1 " + " dcterms:format '" + "application/wkt" + "' .")

            lines.append("samian:loc_ds_" + str(row['id']) + " " + "lado:pleiadesID" + " " + "pleiades:" + str(row['pleiadesid']) + ".")
    if str(row['ancientname']).replace('\'', '`') != 'nan':
        if str(row['ancientname']).replace('\'', '`') != 'undefined':
            lines.append("samian:loc_ds_" + str(row['id']) + " " + "lado:ancientName" + " " + "'" + str(row['ancientname']).replace('\'', '`') + "'" + ".")
    # geom
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "geosparql:hasGeometry" + " samian:loc_ds_" + str(row['id']) + "_geom .")
    lines.append("samian:loc_ds_" + str(row['id']) + "_geom " + "rdf:type" + " sf:Point .")
    point = "POINT(" + str(float(row['lat'])) + " " + str(float(row['long'])) + ")"
    point = "\"<http://www.opengis.net/def/crs/EPSG/0/4326> " + point + "\"^^geosparql:wktLiteral"
    lines.append("samian:loc_ds_" + str(row['id']) + "_geom " + "geosparql:asWKT " + point + ".")
    # prov-o
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "prov:wasAttributedTo" + " samian:ImportPythonScript_Samian .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "prov:wasDerivedFrom" + " <http://www.wikidata.org/entity/Q90412636> .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "prov:wasGeneratedBy" + " samian:activity_loc_ds_" + str(row['id']) + " .")
    lines.append("samian:activity_loc_ds_" + str(row['id']) + " " + "rdf:type" + " <http://www.w3.org/ns/prov#Activity> .")
    lines.append("samian:activity_loc_ds_" + str(row['id']) + " " + "prov:startedAtTime '" + starttime + "'^^xsd:dateTime .")
    lines.append("samian:activity_loc_ds_" + str(row['id']) + " " + "prov:endedAtTime '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "'^^xsd:dateTime .")
    lines.append("samian:activity_loc_ds_" + str(row['id']) + " " + "prov:wasAssociatedWith" + " samian:ImportPythonScript_Samian .")

files = (len(lines) / 100000) + 1
print("lines", len(lines), "files", int(files))

# set output path
dir_path = os.path.dirname(os.path.realpath(__file__))

# write output files
print("start writing turtle files...")

f = 0
step = 100000
fileprefix = "loc_discoverysite_"
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX geosparql: <http://www.opengis.net/ont/geosparql#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX sf: <http://www.opengis.net/ont/sf#> \r\n"
prefixes += "PREFIX lado: <http://archaeology.link/ontology#> \r\nPREFIX samian: <http://data.archaeology.link/data/samian/> \r\nPREFIX wd: <http://www.wikidata.org/entity/> \r\n PREFIX pelagios: <http://pelagios.github.io/vocab/terms#> \r\nPREFIX oa: <http://www.w3.org/ns/oa#> \r\nPREFIX dcterms: <http://purl.org/dc/terms/> \r\nPREFIX foaf: <http://xmlns.com/foaf/0.1/> \r\nPREFIX relations: <http://pelagios.github.io/vocab/relations#> \r\nPREFIX cnt: <http://www.w3.org/2011/content#> \r\nPREFIX pleiades: <http://pleiades.stoa.org/places/> \r\nPREFIX amt: <http://academic-meta-tool.xyz/vocab#> \r\n"
prefixes += "\r\n"
for x in range(1, int(files) + 1):
    strX = str(x)
    filename = dir_path.replace("\\py", "\\ttl") + "\\" + fileprefix + strX + ".ttl"
    file = codecs.open(filename, "w", "utf-8")
    file.write("# create triples from " + url + " \r\n")
    file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
    file.write(prefixes)
    i = f
    for i, line in enumerate(lines):
        if (i > f - 1 and i < f + step):
            file.write(line)
            file.write("\r\n")
    f = f + step
    print("Yuhu! > " + fileprefix + strX + ".ttl")
    file.close()

print("*****************************************")
print("SUCCESS")
print("closing script")
print("*****************************************")
