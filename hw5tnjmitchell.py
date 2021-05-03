###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Nathan Mitchell", "njmitchell"])

###################################################################### 
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population) 
# 
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems. 
# 
###################################################################### 
def calculateDensity(fcpolygon, attribute,geodatabase = "assignment2.gdb"):
    arcpy.env.workspace=geodatabase
    #checking input variables
    describe1=arcpy.Describe(fcpolygon)
    if describe1.shapeType != "Polygon":
        print ("Check inputs")
    #identify coordinate system and give warning if geographic
    describe3=arcpy.Describe(fcpolygon)
    coord0=describe3.spatialReference
    if coord0=="WGS84" or "NAD83":
        print (fcpolygon+" is a geographic projection(e.g., WGS84, NAD83)")
    #calculating the area of each polygon by given attribute in US miles^2, coordinate system is equal to that of input
    arcpy.management.CalculateGeometryAttributes(fcpolygon, attribute, "", "SQUARE_MILES_US",coord0)
    #add new field "myDensity" onto polygon fc
    arcpy.env.overwriteOutput = True
    arcpy.management.AddField(fcpolygon, "myDensity", "DOUBLE")
    #populate new field with with values equal to the quotient of the attribute/area
    arcpy.management.CalculateField(fcpolygon, "myDensity", "!"+attribute+"! / !"+POLY_AREA+"!")

###################################################################### 
# Problem 2 (40 Points)
# 
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase, 
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
# 
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#        
###################################################################### 
def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase = "assignment2.gdb"):
    arcpy.env.workspace=geodatabase
    #checking inputs
    describeA=arcpy.Describe(fcLine)
    describeB=arcpy.Describe(fcClipPolygon)
    if describeA.shapeType != "Line" or
    describeB.shapeType != "Polygon":
        print ("Check input shape type")
    #check to see if the coordinate systems are the same
    dsc1=arcpy.Describe(fcPoint)
    coord1=dsc1.spatialReference
    dsc2=arcpy.Describe(fcClipPolygon)
    coord2=dsc2.spatialReference
    #if they are the same, set fcClipPolygon to the projection of fcLine
    if coord1==coord2:
        arcpy.management.DefineProjection(fcClipPolygon, coord1)
    #create a smaller fc by copying only the polygons with the desired clipPolygonID to the new fc "StateFC" 
    #in this case clipPolygonID is a name field containing states, "Iowa" for example
    arcpy.conversion.FeatureClassToFeatureClass(fcClipPolygon, geodatabase, "StateFC", "STATE_NAME="+clipPolygonID+"")
    #creating a new fc "Clip1" by removing (clipping) any lines from fcLine not within StateFC
    arcpy.analysis.Clip(fcLine, "StateFC", "Clip1")
    #calculating the length of the lines within Clip1
    arcpy.management.AddGeometryAttributes("Clip1", "LENGTH_GEODESIC")
    #calculating the combined length of the lines to field "myOut"
    arcpy.geoanalytics.SummarizeAttributes("Clip1", 'myOut', 'LENGTH_GEO','SUM')
######################################################################
# Problem 3 (30 points)
# 
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################
def countObservationsWithinDistance(fcPoint, distance, distanceUnit, geodatabase = "assignment2.gdb"):
    arcpy.env.workspace=geodatabase  
    arcpy.analysis.Buffer(fcPoint, "myBuff", distance)
    #count quantity of fcPoint points within each myBuff polygon created around the fcPoints
    #"Count of Points" field added to outputFC
    arcpy.analysis.SummarizeWithin("myBuff", fcPoint, "outputFC")
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')
