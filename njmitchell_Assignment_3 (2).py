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
import arcpy
import os

def hawkid():
    return(["Nathan Mitchell", "njmitchell"])

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'


###################################################################### 
def printFeatureClassNames(workspace):
    #create workspace
    arcpy.env.workspace=workspace
    #create list of feature classes from workspace
    fcList = arcpy.ListFeatureClasses()
    #iterate through the list, using Describe to get name and shapeType
    for fc in fcList:
        desc = arcpy.Describe(fc)
        print(desc.name+" is a "+desc.shapeType+" feature class")    
###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    #iterate through a created list of fields taken from the input feature class
    for f in arcpy.ListFields(inputFc):
        #conditional to check: "only if it is a numerical type"
        #printing name of each attribute and its type
        if f.type=="Double":
            print(f.name,f.type)
        elif f.type=="Float":
            print(f.name,f.type)
        elif f.type=="Integer":
            print(f.name,f.type)
        elif f.type=="SmallInteger":
            print(f.name,f.type)

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    arcpy.env.workspace = input_geodatabase
    #Creating list of feature classes of type: shapeType
    FClist = arcpy.ListFeatureClasses(feature_type=shapeType)
    #Creating the output geodatabase path
    arcpy.CreateFileGDB_management(out_folder_path, output_geodatabase)
    #Iterating through the desired feature classes only
    for s in FClist:
        #Creating an output feature class in the output gdb
        out_featureclass = os.path.join(output_geodatabase, os.path.splitext(s)[0])
        #Copying features from desired feature classes into the output fc
        arcpy.CopyFeatures_management(s, out_featureclass)
        
###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    arcpy.env.workspace=workspace
    #Creating a new table populated with values from the inputTable that were joined to the inputFC
    joinedTable=arcpy.AddJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable)
    #Creating a new feature class 
    newFeature=arcpy.management.CreateFeatureclass(workspace,"newFeature.shp")
    #Copying data from the joined table to the new feature class
    output = arcpy.CopyFeatures_management(joinedTable, newFeature)
    print(output)

#Printing results of how many records matched
    count1=0
    count2=0
    #Iterating through the input table to check if the values made it into the joined table
    #Counter created to track every item from the imput table
    #Second counter will not count items that are not within the joined table
    for e in inputTable:
        if e not in joinedTable:
            count1=count1+1
        count2=count2+1
    #Printing total number of matched records over total number of items in the input table
    print(count1+" records matched of "+count2+" total.")
    
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
