# use this tool when you need to create multiple buffers for a possible facility...even the analysis after the filter?
# this tool will calculate the demographics in the 1, 2, 3 mile radii


###  Make sure to save edits (when creating the point feature for the possible parcel), before running the tool


import arcpy
import os
from arcpy import env
env.workspace = r"C:\Users\Kyle\Desktop\SS GIS-Zoning-Competition\SS GIS-Zoning-Competition\Projects\dynamicIterate2\dynamicIterate2.gdb"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.env.overwriteOutput = True

# VARIABLES

censusOriginal = "SLCoTracts"
tracts = "SLCoTractsSplitable0"
#####       get a cleaned up competition data set to get the calcs to process faster
competition = "SLCoCompetition_GeocodeAddre"





MetroPerCapitaSFMultiplier = 7.93
radiusList = ["3", "2", "1"]
inTableParcels = "SandySSParcelsFew"
parcelField = "OBJECTID_1"

# VARIABLES

def splitableTool (censusNonSplitable, censusSplitable):
    arcpy.management.MakeFeatureLayer(censusNonSplitable, censusSplitable, None, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE NONE;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE NONE;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE NONE;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE NONE;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE RATIO;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE")

    return;

def performLoop():
    #VARIABLES
    i = 1

    with arcpy.da.SearchCursor(inTableParcels, parcelField) as cursor:
        for row in cursor:
            parcel = "parcel" + str(i)
            inFeatures = [parcel, tracts]
            parcelFeatureClassesForDeletion = [parcel]

            arcpy.management.MakeFeatureLayer(inTableParcels, parcel, "OBJECTID_1 = " + str(row[0]))

            for radiusListIndex in radiusList:
                parcelBufferName = parcel + "Mile" + radiusListIndex + "Buffer"
                spatialJoinForCompetition = parcelBufferName + "SpatialJoin"
                currentBufferUnion = parcelBufferName + "Union" #this creates the output feature layer
                radiusLoopFeatureClassesForDeletion = [parcelBufferName, spatialJoinForCompetition, currentBufferUnion]
                
                arcpy.analysis.Buffer(parcel, parcelBufferName, str(radiusListIndex) + " Miles", "FULL", "ROUND", "NONE", None, "PLANAR")
                arcpy.Buffer_analysis(parcel, parcelBufferName, str(radiusListIndex) + " Miles")
                
                arcpy.Union_analysis([inFeatures[0] + "Mile" + radiusListIndex + "Buffer", inFeatures[1]], currentBufferUnion)
                arcpy.analysis.SpatialJoin(competition, parcelBufferName, spatialJoinForCompetition, "JOIN_ONE_TO_MANY", "KEEP_ALL")

                
                ## MakeFeatureLayer_management (in_features, out_layer, {where_clause})
                ## This may prove useful in showing a visualization...but I do not think it is necessary
                #input_feature = "BufferUnion" + radiusListIndex + "M" #this creates the input feature layer
                #facilityCapture = "FacilityCapture" + radiusListIndex + "M"
                #arcpy.MakeFeatureLayer_management(input_feature, facilityCapture, "FID_" + parcel + radiusListIndex + "M = 1")
     
                # sum up the people located in the buffer shown in feature class FacilityCapture
                fc = currentBufferUnion
                fields = ["why_csv_Total_population"]
                expression = "FID_" + parcel + "Mile" + radiusListIndex + "Buffer = 1"
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

              

                print ("Population within a " + radiusListIndex + " Mile Radius = " + str(summedTotPop) + ". Which equals " + str(MetroPerCapitaSFMultiplier*summedTotPop) + " Square Feet of Self-Storage Demand.")
                print ("Supplied Gross Square Feet of Self-Storage within the " + radiusListIndex + " Mile Radius = " + str(competitionWithin) + ". Which when subtracted from Demand leaves " + str((MetroPerCapitaSFMultiplier*summedTotPop)-competitionWithin) + "Square Feet Unmet Demand")
                #arcpy.Statistics_analysis("FacilityCapture" + radiusListIndex + "M", "SumStats" + radiusListIndex, [["Total Population", "SUM"]])

                #Need to write to the table before things are deleted
                fc = "SandySSParcelsFew"
                parcelNumber = 
                fieldsToUpdate = ["OBJECTID_1", "totPop3M", "CompetitionSF", "totPop2M", "2MCompetitionSF", "totPop1M", "1MCompetitionSF"]
                newValue = summedTotPop

                # Create update cursor for feature class 
                with arcpy.da.UpdateCursor(fc, fieldsToUpdate) as cursor:
                    for row in cursor:
                        if (row[0] == 15):
                            row[1] = newValue

                        # Update the cursor with the updated list
                        cursor.updateRow(row)



                #summedTotPop = 60000
                #competitionWithin = 80000
                #inTableParcels = "SandySSParcelsFew"               
                #MetroPerCapitaSFMultiplier = 7.93                
                #fieldsToUpdate = ["totPopInBuffer" + "M", "competitionSSSFin" + "M", "UnmetSSSFDemand" + "M" ]                
                ##fieldsToUpdate = ["totPopInBuffer" + radiusListIndex + "M", "competitionSSSFin" + radiusListIndex + "M", "UnmetSSSFDemand" + radiusListIndex + "M" ]
                #with arcpy.da.InsertCursor(inTableParcels, fieldsToUpdate) as fieldInsertCursor:
                #    fieldInsertCursor.insertRow((summedTotPop, competitionWithin, ((MetroPerCapitaSFMultiplier*summedTotPop)-competitionWithin)))
                #                #End of Insert Cursor............................................................................................................



                print (parcel + "Mile" + radiusListIndex + " - All Done!")
                #to delete the feature classes created when loop runs
                for radiusLoopFeatureClass in radiusLoopFeatureClassesForDeletion:
                    arcpy.management.Delete(radiusLoopFeatureClass, None)

            #to delete the parcel
            for parcelFeatureClass in parcelFeatureClassesForDeletion:
                arcpy.management.Delete(parcelFeatureClass, None)

            i += 1

def executeProgram():
    splitableTool("SLCoTracts", "SLCoTractsSplitable0")
    
    fieldsToAdd = ["SFDemandRemaining3M", "totPop2M", "CompSF2M", "SFDemandRemaining2M", "totPop1M", "CompSF1M", "SFDemandRemaining1M"]
    arcpy.management.AddField("SandySSParcelsFew", "CompSF3M", "LONG", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    
    performLoop()

    return;


#FUNCTIONS

#todo  scrpit to clean up competition data ....less fields


executeProgram()

print ("Script has finished running!")



#parcels = "SandySSParcelsFew"
#fieldList = arcpy.ListFields(parcels)
#for fields in fieldList:
#    print (fields.name)

#import arcpy

#fc = "SandySSParcelsFew"
#fieldsToUpdate = ["OBJECTID_1", "totPop3M"]
#newValue = 60000

## Create update cursor for feature class 
#with arcpy.da.UpdateCursor(fc, fieldsToUpdate) as cursor:
#    # For each row, evaluate the WELL_YIELD value (index position 
#    # of 0), and update WELL_CLASS (index position of 1)
#    for row in cursor:
#        if (row[0] == 15):
#            row[1] = newValue

#        # Update the cursor with the updated list
#        cursor.updateRow(row)




##Simple search and replace script
#import arcpy
 
## Retrieve input parameters: the feature class, the field affected by
##  the search and replace, the search term, and the replace term.
#fc = "SandySSParcelsFew"
#affectedField = "totPop3M"
#oldValue = 1
#newValue = 60000
 
## Create the SQL expression for the update cursor. Here this is
##  done on a separate line for readability.
#queryString = "OBJECTID_1 = 15"
#arcpy.management.SelectLayerByAttribute("SandySSParcelsFew", "NEW_SELECTION", "OBJECTID_1 = 15", None)
## Create the update cursor and update each row returned by the SQL expression
#with arcpy.da.UpdateCursor(fc, (affectedField,), queryString) as cursor:
#    for row in cursor:
#        row[0] = newValue
#        cursor.updateRow(row)



## Adds a point and an accompanying description
#import arcpy 
## Retrieve input parameters
#inX = arcpy.GetParameterAsText(0)
#inY = arcpy.GetParameterAsText(1)
#inDescription = arcpy.GetParameterAsText(2)
 
## These parameters are hard-coded. User can't change them.
#incidentsFC = "C:/Data/Yakima/Incidents.shp"
#descriptionField = "DESCR"
 
## Make a tuple of fields to update
#fieldsToUpdate = ("SHAPE@XY", descriptionField)
## Create the insert cursor
#with arcpy.da.InsertCursor(incidentsFC, fieldsToUpdate) as cursor:
#    # Insert the row providing a tuple of affected attributes
#    cursor.insertRow(((float(inX),float(inY)), inDescription)