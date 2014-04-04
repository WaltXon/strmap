import strmap as sm
import strparse as sp
import strimport as im
import strwritegeom as wr




testlegal = ['NE4', 'SE4', 'NENE', 'S2S2', 'S2',
    'N2S2+W2NW4', 'ALL','SW4NE4','S2NW4+SW4','E2', 'W2W2']

jsongeom = dict({u'rings': [[[2082748.664897889, 1314559.3098360598], [2077510.7967647165, 1314775.8576313108],
                [2077710.6139503866, 1320030.2677261382], [2082961.046034798, 1319835.479073733], [2082748.664897889, 1314559.3098360598]]], u'spatialReference': {u'wkid': 102653}})

##1) Get Legal Descriptions from Spreadsheet (strimport)
##2) Parse and format the spreadsheet descriptions (strimport)
##3) Step though each description (strmain)
###3a) pull  nad parse section geometry
###3b)

def main():
    rawdata = ''
    guiddata = ''
    grid = ''
    out_fc = ''

    data = im.ImportDIData(rawdata, guiddata)
    filtereddata = sp.LegalDesc(data)

    for lgl in filtereddata:
        section = sp. GetPlssSectionPoints(grid, '6', sec = lgl[1], twp = lgl[2], twpdir = lgl[3], rng = lgl[4], rngdir= lgl[5])
        for lglpart in lgl[?]:
            for lglsubpart in lglpart.reverse():
                if lglsubpart == 'ALL':
                    shape = section
                elif lglsubpart == 'S':
                    shape = sm.SouthHalf(section)
                elif lglsubpart == 'E'






main()


