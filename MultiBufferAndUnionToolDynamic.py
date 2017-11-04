# use this tool when you need to create multiple buffers for a possible facility...even the analysis after the filter?
# this tool will calculate the demographics in the 1, 2, 3 mile radii


###  Make sure to save edits (when creating the point feature for the possible site), before running the tool


import arcpy
import os
from arcpy import env
env.workspace = r"C:\Users\Kyle\Documents\ArcGIS\Projects\MyProject\MyProject.gdb"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.env.overwriteOutput = True

# VARIABLES
site = "possibleHerriman"
censusOriginal = "SLCoTracts"
tracts = "SLCoTractsSplit"
competition = "SLCoCompetition_GeocodeAddre"
MetroPerCapitaSFMultiplier = 7.93
radiusList = ["3", "2", "1"]
inFeatures = [site, tracts]
# VARIABLES

##I don't know if they InsertCursor isn't working because there are a couple of edit session things going on so the following was to try to do that but I think it really breaks things.....
#edit = arcpy.da.Editor(r"C:\Users\Kyle\Documents\ArcGIS\Projects\MyProject\MyProject.gdb")
#edit.startEditing(False, True)
#edit.startOperation()
##.....................................................................................................................................................

arcpy.management.MakeFeatureLayer(censusOriginal, tracts, None, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;tl_2016_49_tract_STATEFP tl_2016_49_tract_STATEFP VISIBLE NONE;tl_2016_49_tract_COUNTYFP tl_2016_49_tract_COUNTYFP VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_NAMELSAD tl_2016_49_tract_NAMELSAD VISIBLE NONE;tl_2016_49_tract_MTFCC tl_2016_49_tract_MTFCC VISIBLE NONE;tl_2016_49_tract_FUNCSTAT tl_2016_49_tract_FUNCSTAT VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Id why_csv_Id VISIBLE NONE;why_csv_Id2 why_csv_Id2 VISIBLE NONE;why_csv_Geography why_csv_Geography VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE NONE;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE NONE;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE NONE;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE NONE;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE RATIO;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE")

for radiusListIndex in radiusList:
    facilityBufferName = site + radiusListIndex + "M"
    spatialJoinForCompetition = facilityBufferName + "SpatialJoin"
    arcpy.analysis.Buffer(site, facilityBufferName, str(radiusListIndex) + " Miles", "FULL", "ROUND", "NONE", None, "PLANAR")
    #arcpy.Buffer_analysis(site, facilityBufferName, str(radiusListIndex) + " Miles")
    currentBufferUnion = "BufferUnion" + radiusListIndex + "M" #this creates the output feature layer
    arcpy.Union_analysis([inFeatures[0] + radiusListIndex + "M", inFeatures[1]], currentBufferUnion)
    arcpy.analysis.SpatialJoin(competition, facilityBufferName, spatialJoinForCompetition, "JOIN_ONE_TO_MANY", "KEEP_ALL")

    # MakeFeatureLayer_management (in_features, out_layer, {where_clause})
    # This may prove useful in showing a visualization...but I do not think it is necessary
    input_feature = "BufferUnion" + radiusListIndex + "M" #this creates the input feature layer
    facilityCapture = "FacilityCapture" + radiusListIndex + "M"
    arcpy.MakeFeatureLayer_management(input_feature, facilityCapture, "FID_" + site + radiusListIndex + "M = 1")
     
    # sum up the people located in the buffer shown in feature class FacilityCapture
    fc = currentBufferUnion
    fields = ["why_csv_Total_population"]
    expression = "FID_" + site + radiusListIndex + "M = 1"
    summedTotPop = 0
    with arcpy.da.SearchCursor(fc, fields, expression) as cursorPopulation:
        for rowPopulation in cursorPopulation:
            summedTotPop = summedTotPop + rowPopulation[0]

    # sum up the supplied Square Footage from the competition within the buffers
    fc = spatialJoinForCompetition
    fields = ["USER_Gross"]
    expression = "Join_Count = 1"
    competitionWithin = 0
    with arcpy.da.SearchCursor(fc, fields, expression) as cursorCompetition:
        for rowCompetition in cursorCompetition:
            facilityGrossSF = float(rowCompetition[0].replace(",", ""))
            competitionWithin = competitionWithin + facilityGrossSF

    ##I am trying to get this to write to my table but I am not having luck..........................................................
    #table = site
    #fieldsToUpdate = ["totPopInBuffer" + radiusListIndex + "M", "competitionSSSFin" + radiusListIndex + "M", "UnmetSSSFDemand" + radiusListIndex + "M" ]
    #with arcpy.da.InsertCursor(table, fieldsToUpdate) as fieldInsertCursor:
    #    fieldInsertCursor.insertRow((summedTotPop, competitionWithin, ((MetroPerCapitaSFMultiplier*summedTotPop)-competitionWithin)))
    ##End of Insert Cursor............................................................................................................

    print ("Population within a " + radiusListIndex + " Mile Radius = " + str(summedTotPop) + ". Which equals " + str(MetroPerCapitaSFMultiplier*summedTotPop) + " Square Feet of Self-Storage Demand.")
    print ("Supplied Gross Square Feet of Self-Storage within the " + radiusListIndex + " Mile Radius = " + str(competitionWithin) + ". Which when subtracted from Demand leaves " + str((MetroPerCapitaSFMultiplier*summedTotPop)-competitionWithin) + "Square Feet Unmet Demand")
    #arcpy.Statistics_analysis("FacilityCapture" + radiusListIndex + "M", "SumStats" + radiusListIndex, [["Total Population", "SUM"]])

print ("All Done!")

##I don't know if they InsertCursor isn't working because there are a couple of edit session things going on so the following was to try to do that but I think it really breaks things.....
#edit.stopOperation()
#edit.stopEditing(True)
##.....................................................................................................................................................

## to find fields for a table....but it didn't seem to work???........................................
#fieldList = arcpy.ListFields(possible2MSpatialJoin)
#for fields in fieldList:
#    print (fields.name)
##.....................................................................................................................................................

## delete old features so you get a blank slate to work with, but I believe this is obsolete since I am now overwriting results
#for featuretodelete in ["sandyPossible1", "sandyPossible2", "sandyPossible3", "SumStats1", "SumStats2", "SumStats3", "BufferUnion1", "BufferUnion2", "BufferUnion3", "F1Capture1", "F1Capture2", "F1Capture3", "LeftOver1", "LeftOver2", "LeftOver3", "FacilityCapture1M", "FacilityCapture2M", "FacilityCapture3M"]:
#    arcpy.management.Delete(featuretodelete, None)