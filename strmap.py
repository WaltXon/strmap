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
import cProfile

TEST = True

arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False
arcpy.env.workspace = r"K:\COLORADO\LWN\WeldCoLeases.gdb"

in_plss = arcpy.GetParameterAsText(0) or r"IHS_CO_Section_proj"

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

def MaxMinPoints(coords):
    mm = {"maxx": float("-inf"), "maxy": float("-inf"), "minx": float("inf"), "miny": float("inf")}
    for pnt in coords:
        # print("pnt = {0}".format(pnt))
        mm["minx"] = pnt[0] if pnt[0] < mm["minx"] else mm["minx"]
        mm["miny"] = pnt[1] if pnt[1] < mm["miny"] else mm["miny"]
        mm["maxx"] = pnt[0] if pnt[0] > mm["maxx"] else mm["maxx"]
        mm["maxy"] = pnt[1] if pnt[1] > mm["maxy"] else mm["maxy"]
    shp = [(mm['minx'],mm['miny']),(mm['minx'],mm['maxy']),(mm['maxx'],mm['maxy']),(mm['maxx'],mm['miny'])]    
    return shp

##|(minx, maxy)----(maxx, maxy)|
##|                                               |
##|                                               |
##|(minx, miny)----(maxx, miny) |
## lower left corner = ll = shp[0]
## upper left corner = ul = shp[1]
## upper right corner = ur = shp[2]
## lower right corner = lr = shp[3]

def Angle(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    a = math.atan2(dy,dx)
    return a

def Distance(x1,y1,x2,y2):
    a = (x2-x1)**2
    b = (y2-y1)**2
    return math.sqrt(a+b)

def NewPoint(x,y,angle, dist):
    cos = math.cos((angle))
    sin = math.sin((angle))
    xn = x + cos * dist
    yn = y + sin * dist
    return (xn,yn)

def SouthHalf(shp):
    ll = shp[0]
    ul = NewPoint(shp[0][0], shp[0][1], Angle(shp[0][0], shp[0][1],shp[1][0], shp[1][1]),  Distance(shp[0][0],shp[0][1],shp[1][0],shp[1][1])*0.5)
    lr =  shp[3]
    ur = NewPoint(shp[3][0], shp[3][1], Angle(shp[3][0], shp[3][1],shp[2][0], shp[2][1]),  Distance(shp[3][0],shp[3][1],shp[2][0],shp[2][1])*0.5)
    return([ll, ul, ur, lr, ll])

def NorthHalf(shp):
    ll = NewPoint(shp[1][0], shp[1][1], Angle(shp[1][0], shp[1][1],shp[0][0], shp[0][1]),  Distance(shp[1][0],shp[1][1],shp[0][0],shp[0][1])*0.5)
    ul = shp[1]
    lr =  NewPoint(shp[2][0], shp[2][1], Angle(shp[2][0], shp[2][1],shp[3][0], shp[3][1]),  Distance(shp[2][0],shp[2][1],shp[3][0],shp[3][1])*0.5)
    ur = shp[2]
    return([ll, ul, ur, lr, ll])

def EastHalf(shp):
    ll = NewPoint(shp[3][0], shp[3][1], Angle(shp[3][0], shp[3][1],shp[0][0], shp[0][1]),  Distance(shp[3][0],shp[3][1],shp[0][0],shp[0][1])*0.5)
    ul = NewPoint(shp[2][0], shp[2][1], Angle(shp[2][0], shp[2][1],shp[1][0], shp[1][1]),  Distance(shp[2][0],shp[2][1],shp[1][0],shp[1][1])*0.5)
    lr =  shp[3]
    ur = shp[2]
    return([ll, ul, ur, lr, ll])

def WestHalf(shp):
    ll = shp[0]
    ul = shp[1]
    lr = NewPoint(shp[0][0], shp[0][1], Angle(shp[0][0], shp[0][1],shp[3][0], shp[3][1]),  Distance(shp[0][0],shp[0][1],shp[3][0],shp[3][1])*0.5)
    ur = NewPoint(shp[1][0], shp[1][1], Angle(shp[1][0], shp[1][1],shp[2][0], shp[2][1]),  Distance(shp[1][0],shp[1][1],shp[2][0],shp[2][1])*0.5)
    return([ll, ul, ur, lr, ll])

def NEQuarter(shp):
    ul = NewPoint(shp[2][0], shp[2][1], Angle(shp[2][0], shp[2][1],shp[1][0], shp[1][1]), Distance(shp[2][0],shp[2][1],shp[1][0],shp[1][1])*0.5)
    lr = NewPoint(shp[2][0], shp[2][1], Angle(shp[2][0], shp[2][1],shp[3][0], shp[3][1]), Distance(shp[2][0],shp[2][1],shp[3][0],shp[3][1])*0.5)
    ur = shp[2] 
    ll = NewPoint(ul[0], ul[1], Angle(shp[2][0], shp[2][1],shp[3][0], shp[3][1]), Distance(shp[2][0],shp[2][1],shp[3][0],shp[3][1])*0.5)
    return([ll, ul, ur, lr, ll])

def NWQuarter(shp):
    ul = shp[1]
    ur = NewPoint(shp[1][0], shp[1][1], Angle(shp[1][0], shp[1][1],shp[2][0], shp[2][1]), Distance(shp[1][0],shp[1][1],shp[2][0],shp[2][1])*0.5) 
    ll = NewPoint(shp[1][0], shp[1][1], Angle(shp[1][0], shp[1][1],shp[0][0], shp[0][1]),  Distance(shp[1][0],shp[1][1],shp[0][0],shp[0][1])*0.5)
    lr = NewPoint(ur[0], ur[1], Angle(shp[1][0], shp[1][1],shp[0][0], shp[0][1]), Distance(shp[1][0],shp[1][1],shp[0][0],shp[0][1])*0.5)
    return([ll, ul, ur, lr, ll])

def SEQuarter(shp):
    lr = shp[3]
    ur = NewPoint(shp[3][0], shp[3][1], Angle(shp[3][0], shp[3][1],shp[2][0], shp[2][1]), Distance(shp[3][0],shp[3][1],shp[2][0],shp[2][1])*0.5) 
    ll = NewPoint(shp[3][0], shp[3][1], Angle(shp[3][0], shp[3][1],shp[0][0], shp[0][1]),  Distance(shp[3][0],shp[3][1],shp[0][0],shp[0][1])*0.5)
    ul = NewPoint(ll[0], ll[1], Angle(shp[3][0], shp[3][1],shp[2][0], shp[2][1]),  Distance(shp[3][0],shp[3][1],shp[2][0],shp[2][1])*0.5)
    return([ll, ul, ur, lr, ll])

def SWQuarter(shp):
    ll = shp[0]
    ul = NewPoint(shp[0][0], shp[0][1], Angle(shp[0][0], shp[0][1],shp[1][0], shp[1][1]), Distance(shp[0][0],shp[0][1],shp[1][0],shp[1][1])*0.5) 
    lr = NewPoint(shp[0][0], shp[0][1], Angle(shp[0][0], shp[0][1],shp[3][0], shp[3][1]),  Distance(shp[0][0],shp[0][1],shp[3][0],shp[3][1])*0.5)
    ur = NewPoint(lr[0], lr[1], Angle(shp[0][0], shp[0][1],shp[1][0], shp[1][1]),  Distance(shp[0][0],shp[0][1],shp[1][0],shp[1][1])*0.5)
    return([ll, ul, ur, lr, ll])

#TEST
def test():
    #jsongeom = GetPlssSectionPoints(in_plss, 6, 12, 2, 'N', 102, 'W')
    jsongeom = dict({u'rings': [[[2082748.664897889, 1314559.3098360598], [2077510.7967647165, 1314775.8576313108], [2077710.6139503866, 1320030.2677261382], [2082961.046034798, 1319835.479073733], [2082748.664897889, 1314559.3098360598]]], u'spatialReference': {u'wkid': 102653}})
    print("jsongeom = {0}".format(jsongeom))
    parsedjson= ParseJsonGeom(jsongeom)
    print("parsedjson = {0}".format(parsedjson))
    maxmin = MaxMinPoints(parsedjson)
    print("maxmin = {0}".format(maxmin))
    print("SouthHalf = {0}".format(SouthHalf(maxmin)))
    print("NorthHalf = {0}".format(NorthHalf(maxmin)))
    print("EastHalf = {0}".format(EastHalf(maxmin)))
    print("WestHalf = {0}".format(WestHalf(maxmin)))
    print("SWQuarter = {0}".format(SWQuarter(maxmin)))
    print("SEQuarter = {0}".format(SEQuarter(maxmin)))
    print("NWQuarter = {0}".format(NWQuarter(maxmin)))
    print("NEQuarter = {0}".format(NEQuarter(maxmin)))

if TEST == True:
    cProfile.run('test()')


