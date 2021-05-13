import arcpy
calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygon1, fcPolygon2)
#setup workspace
    arcpy.env.workspace=input_geodatabase
#create intersect fc from the two input polygons
    arcpy.analysis.Intersect([fcPolygon1, fcPolygon2], myOutput)
#add field 'OmyArea' onto intersect output
    arcpy.AddField_management(myOutput, 'OmyArea', 'DOUBLE')
#populate field 'OmyArea' of intersect
    arcpy.management.CalculateGeometryAttributes(myOutput, [["OmyArea","AREA_GEODESIC"]])
    arcpy.AddField_management(fcPolygon1, 'PmyArea', 'DOUBLE')
    arcpy.management.CalculateGeometryAttributes(fcPolygon1, [["PmyArea","AREA_GEODESIC"]])
#initialize empty dictionary 'myDict'
    myDict = {}
#iterate through 'myOutput' using 'FIPS' and 'OmyArea' 
    with arcpy.da.SearchCursor(myOutput, ["FIPS","OmyArea"]) as cursor:
        for row in cursor:
            fips = row[0]
#create dictionary key for each unique fips code
            if fips in myDict.keys():
                myDict[fips] += row[1]
            else:
                myDict[fips] = row[1]
#add field 'BGmyArea' onto fcPolygon2
    arcpy.AddField_management(fcPolygon2, 'BGmyArea', 'DOUBLE')
#iterate through fcPolygon2 using 'FIPS' and 'BGmyArea' 
    with arcpy.da.UpdateCursor(fcPolygon2, ["FIPS","BGmyArea"]) as cursor:
        for row in cursor:
#if the fips aligns, the row for 'BGmyArea' is set
            if row[0] in myDict.keys():
                row[1] = myDict[row[0]]
            else:
                row[1]=0
            cursor.updateRow(row)
#add field 'pct' onto fcPolygon2
    arcpy.AddField_management(fcPolygon2, 'pct', 'DOUBLE')
#calculate field 'pct' by dividing 'BGmyArea' by 'OmyArea'
    arcpy.CalculateField_management(fcPolygon2, 'pct', "!BGmyArea!/!OmyArea!", "PYTHON3")
