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
filteredTractsOrig = "SLCoAntiMatterTracts"
filteredTractsSplitable = "SLCoAntiMatterTractsSplitable"
#####       get a cleaned up competition data set to get the calcs to process faster
competition = "SLCoCompetition_GeocodeAddre"
MetroPerCapitaSFMultiplier = 7.93
radiusList = ["3", "2", "1"]
inTableParcels = "SandySSParcelsFew"
parcelField = "OBJECTID_1"
# VARIABLES

#FUNCTIONS
def splitableTool (censusNonSplitable, censusSplitable):
    arcpy.management.MakeFeatureLayer(censusNonSplitable, censusSplitable, None, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE NONE;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE NONE;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE NONE;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE NONE;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE RATIO;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE")

    return;

def filteredSplitableTool (filteredTractsOrig, filteredTractsSplitable):
    arcpy.management.MakeFeatureLayer(filteredTractsOrig, filteredTractsSplitable, None, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_facility155Buffer FID_facility155Buffer VISIBLE NONE;FID_SLCoTracts FID_SLCoTracts VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE RATIO;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE NONE;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE RATIO;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE RATIO;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Area Area VISIBLE NONE;popDensity popDensity VISIBLE NONE;ownerOccupiedHousingUnits ownerOccupiedHousingUnits VISIBLE RATIO;renterOccupiedHousingUnits renterOccupiedHousingUnits VISIBLE RATIO")

    return;

def performLoop():
    
    i = 1

    with arcpy.da.SearchCursor(inTableParcels, parcelField) as cursor:
        for row in cursor:
            #PARCEL LOOP VARIABLES
            parcel = "parcel" + str(i)
            inFeatures = [parcel, tracts]
            filteredInFeatures = [parcel, filteredTractsSplitable]
            parcelFeatureClassesForDeletion = [parcel]
            #PARCEL LOOP VARIABLES

            arcpy.management.MakeFeatureLayer(inTableParcels, parcel, "OBJECTID_1 = " + str(row[0]))

            #Get the Parcel OBJECTID # for writing to the master parcel table later...
            fc = parcel
            fields = ["OBJECTID_1"]
            with arcpy.da.SearchCursor(fc, fields) as cursorObjectID:
                for rowObjectID in cursorObjectID:
                    objectID = row[0]

            for radiusListIndex in radiusList:
                #RADIUS LOOP VARIABLES
                parcelBufferName = parcel + "Mile" + radiusListIndex + "Buffer"
                spatialJoinForCompetition = parcelBufferName + "SpatialJoin"
                currentBufferUnion = parcelBufferName + "Union" #this creates the output feature layer
                filteredCurrentBufferUnion = currentBufferUnion + "Filtered"
                radiusLoopFeatureClassesForDeletion = [parcelBufferName, spatialJoinForCompetition, currentBufferUnion, filteredCurrentBufferUnion]
                #RADIUS LOOP VARIABLES
                
                #arcpy.analysis.Buffer(parcel, parcelBufferName, str(radiusListIndex) + " Miles", "FULL", "ROUND", "NONE", None, "PLANAR")
                arcpy.Buffer_analysis(parcel, parcelBufferName, str(radiusListIndex) + " Miles")
                
                #Union for traditional demographic analysis 
                arcpy.Union_analysis([inFeatures[0] + "Mile" + radiusListIndex + "Buffer", inFeatures[1]], currentBufferUnion)

                #Union for FILTERED demographic analysis
                arcpy.Union_analysis([filteredInFeatures[0] + "Mile" + radiusListIndex + "Buffer", filteredInFeatures[1]], filteredCurrentBufferUnion)
                
                #Spatial Join to see how much competion is in the radius/buffer
                arcpy.analysis.SpatialJoin(competition, parcelBufferName, spatialJoinForCompetition, "JOIN_ONE_TO_MANY", "KEEP_ALL")
                
                ## MakeFeatureLayer_management (in_features, out_layer, {where_clause})
                ## This may prove useful in showing a visualization...but I do not think it is necessary
                #input_feature = "BufferUnion" + radiusListIndex + "M" #this creates the input feature layer
                #facilityCapture = "FacilityCapture" + radiusListIndex + "M"
                #arcpy.MakeFeatureLayer_management(input_feature, facilityCapture, "FID_" + parcel + radiusListIndex + "M = 1")
     
                # sum up the people located in the buffer shown in feature class FacilityCapture
                fc = currentBufferUnion
                fields = ["why_csv_Total_population", "why_csv_TotalHouseholds", "why_csv_Owner_Occupied_Housing_Units", "why_csv_Renter_Occupied_Housing_Units"]
                expression = "FID_" + parcel + "Mile" + radiusListIndex + "Buffer = 1"
                summedTotPop = 0
                summedTotHouseholds = 0
                summedOwnerHousingUnits = 0.00
                summedRenterHousingUnits = 0.00
                with arcpy.da.SearchCursor(fc, fields, expression) as cursorPopulation:
                    for rowPopulation in cursorPopulation:
                        summedTotPop = summedTotPop + rowPopulation[0]
                        summedTotHouseholds = summedTotHouseholds + rowPopulation[1]
                        summedOwnerHousingUnits = summedOwnerHousingUnits + float(rowPopulation[2])
                        summedRenterHousingUnits = summedRenterHousingUnits + float(rowPopulation[3])

                # sum up the FILTERED people located in the buffer shown in feature class FacilityCapture
                fc = filteredCurrentBufferUnion
                fields = ["why_csv_Total_population", "why_csv_TotalHouseholds", "ownerOccupiedHousingUnits", "renterOccupiedHousingUnits"]
                expression = "FID_" + parcel + "Mile" + radiusListIndex + "Buffer = 1"
                summedtotPopFiltered = 0
                summedTotHouseholdsFiltered = 0
                summedOwnerHousingUnitsFiltered = 0
                summedRenterHousingUnitsFiltered = 0
                with arcpy.da.SearchCursor(fc, fields, expression) as cursorPopulationFiltered:
                    for rowPopulationFiltered in cursorPopulationFiltered:
                        summedtotPopFiltered = summedtotPopFiltered + rowPopulationFiltered[0]
                        summedTotHouseholdsFiltered = summedTotHouseholdsFiltered + rowPopulationFiltered[1]
                        summedOwnerHousingUnitsFiltered = summedOwnerHousingUnitsFiltered + float(rowPopulationFiltered[2])
                        summedRenterHousingUnitsFiltered = summedRenterHousingUnitsFiltered + float(rowPopulationFiltered[3])

                # sum up the Median Income located in the buffer shown in feature class FacilityCapture
                fc = currentBufferUnion
                fields = ["why_csv_Median_Household_income", "why_csv_Total_population"]
                expression = "FID_" + parcel + "Mile" + radiusListIndex + "Buffer = 1"
                medianHHIncome = 0
                summedTotPop = 0
                with arcpy.da.SearchCursor(fc, fields, expression) as cursorIncome:
                    for rowIncome in cursorIncome:
                        medianHHIncomePass = float(rowIncome[0]) * rowIncome[1]
                        summedTotPop = summedTotPop + rowIncome[1]
                        medianHHIncome = medianHHIncome + medianHHIncomePass
                        medianHHIncomeFinal = medianHHIncome / summedTotPop

                # sum up the FILTERED Median Income located in the buffer shown in feature class FacilityCapture
                fc = filteredCurrentBufferUnion
                fields = ["MedianHHIncome", "why_csv_Total_population"]
                expression = "FID_" + parcel + "Mile" + radiusListIndex + "Buffer = 1"
                medianHHIncomeFiltered = 0
                summedTotPopFiltered = 1
                with arcpy.da.SearchCursor(fc, fields, expression) as cursorIncomeFiltered:
                    for rowIncomeFiltered in cursorIncomeFiltered:
                        medianHHIncomeFilteredPass = float(rowIncomeFiltered[0]) * rowIncomeFiltered[1]
                        summedTotPopFiltered = summedTotPopFiltered + rowIncomeFiltered[1]
                        medianHHIncomeFiltered = medianHHIncomeFiltered + medianHHIncomeFilteredPass
                        medianHHIncomeFilteredFinal = medianHHIncomeFiltered / summedTotPopFiltered

                # sum up the supplied Square Footage from the competition within the buffers
                fc = spatialJoinForCompetition
                fields = ["USER_Gross"]
                expression = "Join_Count = 1"
                competitionWithin = 0
                with arcpy.da.SearchCursor(fc, fields, expression) as cursorCompetition:
                    for rowCompetition in cursorCompetition:
                        facilityGrossSF = float(rowCompetition[0].replace(",", ""))
                        competitionWithin = competitionWithin + facilityGrossSF

                #Calculate the buffers for the roads




                #print ("Population within a " + radiusListIndex + " Mile Radius = " + str(summedTotPop) + ". Which equals " + str(MetroPerCapitaSFMultiplier*summedTotPop) + " Square Feet of Self-Storage Demand.")
                #print ("Supplied Gross Square Feet of Self-Storage within the " + radiusListIndex + " Mile Radius = " + str(competitionWithin) + ". Which when subtracted from Demand leaves " + str((MetroPerCapitaSFMultiplier*summedTotPop)-competitionWithin) + "Square Feet Unmet Demand")
                #arcpy.Statistics_analysis("FacilityCapture" + radiusListIndex + "M", "SumStats" + radiusListIndex, [["Total Population", "SUM"]])

                #Need to write to the table before things are deleted
                tableToUpdate = "SandySSParcelsFew"
                fieldsToUpdate = ["OBJECTID_1", 
                                  "totPop" + radiusListIndex + "M", 
                                  "totPopFiltered" + radiusListIndex + "M",
                                  "totalHouseholds" + radiusListIndex + "M",
                                  "totalHouseholdsFiltered" + radiusListIndex + "M",
                                  "totalOwnerHousingUnits" + radiusListIndex + "M",
                                  "totalOwnerHousingUnitsFiltered" + radiusListIndex + "M",
                                  "totalRenterHousingUnits" + radiusListIndex + "M",
                                  "totalRenterHousingUnitsFiltered" + radiusListIndex + "M",
                                  "rentersPerc" + radiusListIndex + "M",
                                  "rentersPercFiltered" + radiusListIndex + "M",
                                  "CompSF" + radiusListIndex + "M", 
                                  "SFDemandRemaining" + radiusListIndex + "M", 
                                  "SFDemandFiltered" + radiusListIndex + "M",
                                  "MedianHHIncome" + radiusListIndex + "M",
                                  "MedianHHIncomeFiltered" + radiusListIndex + "M"]

                with arcpy.da.UpdateCursor(tableToUpdate, fieldsToUpdate) as cursor:
                    for row in cursor:
                        if (row[0] == objectID):
                            row[1] = summedTotPop
                            row[2] = summedtotPopFiltered
                            row[3] = summedTotHouseholds
                            row[4] = summedTotHouseholdsFiltered
                            row[5] = summedOwnerHousingUnits
                            row[6] = summedOwnerHousingUnitsFiltered
                            row[7] = summedRenterHousingUnits
                            row[8] = summedRenterHousingUnitsFiltered
                            row[9] = (summedRenterHousingUnits / (summedOwnerHousingUnits + summedRenterHousingUnits))
                            row[10] = (summedRenterHousingUnitsFiltered / (summedOwnerHousingUnitsFiltered + summedRenterHousingUnitsFiltered))
                            row[11] = competitionWithin
                            row[12] = ((MetroPerCapitaSFMultiplier*summedTotPop)-competitionWithin)
                            row[13] = (MetroPerCapitaSFMultiplier*summedtotPopFiltered)
                            row[14] = medianHHIncomeFinal
                            row[15] = medianHHIncomeFilteredFinal
                            row[16] = 
                            #TODO: ADD traffic Counts and Incomes
                       
                        # Update the cursor with the updated list
                        cursor.updateRow(row)

                print (parcel + "Mile" + radiusListIndex + " - All Done!")

                #next 2 lines only works in IDE or IDLE.  Have to press enter to continue
                #print("press enter to continue...")
                #input()

                #to delete the feature classes created when loop runs
                for radiusLoopFeatureClass in radiusLoopFeatureClassesForDeletion:
                    arcpy.management.Delete(radiusLoopFeatureClass, None)

            #to delete the parcel
            for parcelFeatureClass in parcelFeatureClassesForDeletion:
                arcpy.management.Delete(parcelFeatureClass, None)

            i += 1

def executeProgram():
   
    fieldsToAddToDemographics = ["ownerOccupiedHousingUnits", "renterOccupiedHousingUnits", "MedianHHIncome"]

    for fieldsToAddDemo in fieldsToAddToDemographics:
        arcpy.management.AddField(filteredTractsOrig, fieldsToAddDemo, "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
        arcpy.management.AddField(censusOriginal, fieldsToAddDemo, "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    
    splitableTool("SLCoTracts", "SLCoTractsSplitable0")
    
    filteredSplitableTool (filteredTractsOrig, filteredTractsSplitable)
   
    fieldsToAddToParcels = ["totPop3M", 
                            "totPopFiltered3M",
                            "totalHouseholds3M",
                            "totalHouseholdsFiltered3M",
                            "totalOwnerHousingUnits3M",
                            "totalOwnerHousingUnitsFiltered3M",
                            "totalRenterHousingUnits3M",
                            "totalRenterHousingUnitsFiltered3M",
                            "rentersPerc3M",
                            "rentersPercFiltered3M",
                            "CompSF3M", 
                            "SFDemandRemaining3M", 
                            "SFDemandFiltered3M",
                            "totPop2M", 
                            "totPopFiltered2M",
                            "totalHouseholds2M",
                            "totalHouseholdsFiltered2M",
                            "totalOwnerHousingUnits2M",
                            "totalOwnerHousingUnitsFiltered2M",
                            "totalRenterHousingUnits2M",
                            "totalRenterHousingUnitsFiltered2M",
                            "rentersPerc2M",
                            "rentersPercFiltered2M",
                            "CompSF2M", 
                            "SFDemandRemaining2M", 
                            "SFDemandFiltered2M", 
                            "totPop1M", 
                            "totPopFiltered1M",
                            "totalHouseholds1M",
                            "totalHouseholdsFiltered1M",
                            "totalOwnerHousingUnits1M",
                            "totalOwnerHousingUnitsFiltered1M",
                            "totalRenterHousingUnits1M",
                            "totalRenterHousingUnitsFiltered1M",
                            "rentersPerc1M",
                            "rentersPercFiltered1M",
                            "CompSF1M", 
                            "SFDemandRemaining1M", 
                            "SFDemandFiltered1M", 
                            "streetADT",
                            "MedianHHIncome3M",
                            "MedianHHIncome2M",
                            "MedianHHIncome1M",
                            "MedianHHIncomeFiltered3M",
                            "MedianHHIncomeFiltered2M",
                            "MedianHHIncomeFiltered1M",
                            "Score",
                            "filteredScore"]
    for fieldsToAdd in fieldsToAddToParcels:
        arcpy.management.AddField("SandySSParcelsFew", fieldsToAdd, "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    
    #get road data ready for parcels
    #create buffers based upon AADT


roads = "SLCoODOTRoadsFew"
roadBufferName = roads + "Buffer"
AADTField = ["AADT2015"]
with arcpy.da.SearchCursor(roads, AADTField) as cursorRoadBuffer:
    for rowRoadBuffer in cursorRoadBuffer:
        if float(row[0]) >= 65000:
            roadBufferDistance = 200
        elif 35000 <= float(row[0]) < 65000:
            roadBufferDistance = 100
        elif 15000 <= float(row[0]) < 35000:
            roadBufferDistance = 50
        else:
            roadBufferDistance = 30
        arcpy.Buffer_analysis(roads, roadBufferName, str(roadBufferDistance) + " Meters")





    performLoop()

    return;
#FUNCTIONS

#TODO : Add roads, Get the ranking to happen



executeProgram()

print ("Script has finished running!")



##Used to get a field to update...null values were being problematic
#tableToUpdate = "SLCoAntiMatterTracts"
#fieldsToUpdate = ["why_csv_Median_Household_income", "medianHHIncome"]

#with arcpy.da.UpdateCursor(tableToUpdate, fieldsToUpdate) as cursor:
#    for row in cursor:
#        if (float(row[0]) > 1 ):
#            row[1] = row[0]
            
#        # Update the cursor with the updated list
#        cursor.updateRow(row)