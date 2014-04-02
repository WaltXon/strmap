'''-------------------------------------------------------------------------------------------
 Tool Name:   Section Township Range Plot
 Source Name: strmap.py
 Version:     ArcGIS 10.1
 Author:      Walt Nixon
 Required Arguments:
              PLSS Grid (Feature Layer)
              Legal Description (id, Meridian, Section, Township, TownshipDirection, Range, RangeDirection, Legal)
              Output Feature Class (Feature Class)
 Optional Arguments:

 Description: Takes a PLSS descritiption and maps the resultant polygon
----------------------------------------------------------------------------------------------'''

import arcpy
import os
import sys
import math
import json

TEST = True

arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False
arcpy.env.workspace = r"K:\COLORADO\LWN\WeldCoLeases.gdb"

in_plss = arcpy.GetParameterAsText(0) or r"IHS_CO_Section_proj"

def UnpackGeoObj(geoObj):
    pass

def GetPlssSectionPoints(plss, meridian, sec, twp, twpdir, rng, rngdir):
    expression = """{0} = {1} AND {2} = {3} AND {4} = {5} AND {6} LIKE '{7}' AND {8} = {9} AND {10} LIKE '{11}'""".format(
        arcpy.AddFieldDelimiters(plss,"MER"), meridian,
        arcpy.AddFieldDelimiters(plss,"SEC"), sec,
        arcpy.AddFieldDelimiters(plss,"TWP"), twp,
        arcpy.AddFieldDelimiters(plss,"TDIR"), twpdir,
        arcpy.AddFieldDelimiters(plss,"RNG"), rng,
        arcpy.AddFieldDelimiters(plss,"RDIR"), rngdir)

    shape = [row[0] for row in arcpy.da.SearchCursor(plss, ["SHAPE@JSON"], where_clause=expression)]
    #print shape
    return json.loads(shape[0])


def ParseJsonGeom(json):
    for vals in json['rings']:
        return vals

def GetMaxMinPoints(coords):
    mm = {"maxx": float("-inf"), "maxy": float("-inf"), "minx": float("inf"), "miny": float("inf")}
    for pnt in coords:
        # print("pnt = {0}".format(pnt))
        mm["minx"] = pnt[0] if pnt[0] < mm["minx"] else mm["minx"]
        mm["miny"] = pnt[1] if pnt[1] < mm["miny"] else mm["miny"]
        mm["maxx"] = pnt[0] if pnt[0] > mm["maxx"] else mm["maxx"]
        mm["maxy"] = pnt[1] if pnt[1] > mm["maxy"] else mm["maxy"]
    return mm

def SouthHalf():
    pass

def NorthHalf():
    pass

def EastHalf():
    pass

def WestHalf():
    pass

def NEQuarter():
    pass

def NWQuarter():
    pass

def SEQuarter():
    pass

def SWQuarter():
    pass

#TEST
if TEST == True:
    #secpoints = GetPlssSectionPoints(in_plss, 6, 12, 2, 'N', 102, 'W')
    jsongeom = dict({u'rings': [[[2082748.664897889, 1314559.3098360598], [2077510.7967647165, 1314775.8576313108], [2077710.6139503866, 1320030.2677261382], [2082961.046034798, 1319835.479073733], [2082748.664897889, 1314559.3098360598]]], u'spatialReference': {u'wkid': 102653}})
    print("secpoints = {0}".format(jsongeom))
    parsedjson= ParseJsonGeom(secpoints)
    print("parsedlegal = {0}".format(parsedjson))
    print GetMaxMinPoints(parsedjson)
