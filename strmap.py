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

in_plss = arcpy.GetParameterAsText(0) or r"IHS_CO_Section"

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
    print shape
    return json.loads(shape[0])


def ParseLegalDesc():
    pass

def CreateBisector():
    pass



#TEST
if TEST == True:
    print GetPlssSectionPoints(in_plss, 6, 12, 2, 'N', 102, 'W')