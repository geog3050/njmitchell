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
# Problem 1: 20 Points
#
# Given a csv file import it into the database passed as in the second parameter
# Each parameter is described below:

# csvFile: The absolute path of the file should be included (e.g., C:/users/ckoylu/test.csv)
# geodatabase: The workspace geodatabase
###################################################################### 
def importCSVIntoGeodatabase(csvFile, geodatabase):
    import arcpy
    arcpy.env.workspace = geodatabase
    outTable = "importTable"
    arcpy.TableToTable_conversion(csvFile, arcpy.env.workspace, outTable)

##################################################################################################### 
# Problem 2: 80 Points Total
#
# Given a csv table with point coordinates, this function should create an interpolated
# raster surface, clip it by a polygon shapefile boundary, and generate an isarithmic map

# You can organize your code using multiple functions. For example,
# you can first do the interpolation, then clip then equal interval classification
# to generate an isarithmic map

# Each parameter is described below:

# inTable: The name of the table that contain point observations for interpolation       
# valueField: The name of the field to be used in interpolation
# xField: The field that contains the longitude values
# yField: The field that contains the latitude values
# inClipFc: The input feature class for clipping the interpolated raster
# workspace: The geodatabase workspace

# Below are suggested steps for your program. More code may be needed for exception handling
#    and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. For example,
#    interpolated raster can be named after the field value field name 
# 2- You can assume the input table should have the coordinates in latitude and longitude (WGS84)
# 3- Generate an input feature later using inTable
# 4- Convert the projection of the input feature layer
#    to match the coordinate system of the clip feature class. Do not clip the features yet.
# 5- Check and enable the spatial analyst extension for kriging
# 6- Use KrigingModelOrdinary function and interpolate the projected feature class
#    that was created from the point feature layer.
# 7- Clip the interpolated kriging raster, and delete the original kriging result
#    after successful clipping. 
#################################################################################################################### 
def krigingFromPointCSV(inTable, valueField, xField, yField, inClipFc, workspace = "assignment3.gdb"):
    import arcpy
    from arcpy.sa import *
    arcpy.env.workspace=workspace
    #create input point feature from xy data in inTable
    outputPoints = inTable+"_Points"
    arcpy.management.XYTableToPoint(inTable, outputPoints, xField, yField)
    #check coordinate system of input feature layer and set point feature to match
    Desc = arcpy.Describe(outputPoints)
    SR = Desc.spatialReference
    arcpy.management.DefineProjection(outputPoints, SR)
    #check and enable the spatial analyst extension
    try:
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise LicenseError
    except LicenseError:
        print("Spatial Analyst license is unavailable")
    #find cellSize for Kriging
    descOP = arcpy.Describe(outputPoints)
    cellSize = 0
    width = descOP.extent.width
    height = descOP.extent.height
    if width < height:
        cellSize = width / 1000
    else:
        cellSize = height / 1000
    #using kriging and interpolating the projected feature class that was created from the point feature layer
    KrigModelOrd = KrigingModelOrdinary ("SPHERICAL")
    KrigModelOrd2 = Kriging(outputPoints, valueField, '#', cellSize)
    KrigModelOrd2.save(valueField+"_Krig")
    #clip the interpolated kriging raster using bounds established from inClipFC
    descICFC = arcpy.Describe(inClipFC)
    bounds = str(descICFC.extent.XMin) + " " + str(descICFC.extent.YMin) + " " + str(descICFC.extent.XMax) + " " + str(descICFC.extent.YMax)
    arcpy.Clip_management(valueField+"_Krig", bounds, valueField+"_Krig_Clip", inClipFC, "#", "ClippingGeometry", "MAINTAIN_EXTENT")
    #delete the original kriging result
    arcpy.management.Delete(valueField+"_Krig")
    

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
