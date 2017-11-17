#1st thing when establishing new map...go into the map and set up the projection
#import competition and Tracts (but add them to the geodatabase as well
#set up new work environment
import arcpy
from arcpy import env
import os
env.workspace = r"C:\Users\Kyle\Desktop\SS GIS-Zoning-Competition\SS GIS-Zoning-Competition\Projects\dynamicIterate2\dynamicIterate2.gdb"

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.env.overwriteOutput = True
clear = lambda: os.system('cls')

# FUNCTIONS
#Retrieve the Square Footage supplied for the Facility
 #The following gives a list of fields to pick from:**********
    #fieldList = arcpy.ListFields(facility)
    #for fields in fieldList:
    #    print (fields.name)
    #************************************************************

def getValueFromCompetitionTable(facility, fieldNetSF):
    expression = None
    facilityNetSF = 0
    with arcpy.da.SearchCursor(facility, fieldNetSF, expression) as cursor:
        for row in cursor:
            facilityNetSF = float(row[0].replace(",", ""))
    #print (facility, 'has a Net Square Footage of:', facilityNetSF)

    return facilityNetSF;

def facilitySupplyIsGreaterThanbufferPopulationDemand(bufferPopulationDemand, netSquareFeet, radius, radiusIncrement):
    if bufferPopulationDemand == 0:
        return True;

    if netSquareFeet < bufferPopulationDemand:
        print("netSquareFeet:", netSquareFeet, ", bufferPopulationDemand:", bufferPopulationDemand, " Equilibrium Found!!!")
    else :
        print("Facility Net Square Feet: is ", netSquareFeet, ", which is larger than Buffer Population's Square Footage Demanded of ", bufferPopulationDemand, ". Continue Script to increase the Radius...")

    return netSquareFeet > bufferPopulationDemand;

#To make a feature class "Divisible" or "Splitable"
def splitableTool (censusNonSplitable, censusSplitable):
    arcpy.management.MakeFeatureLayer(censusNonSplitable, censusSplitable, None, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE NONE;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE NONE;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE NONE;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE NONE;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE RATIO;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE")

    return;

def splitableToolEndOfLoop (unionName, censusSplitableOutput, expressionLO):
    arcpy.management.MakeFeatureLayer(unionName, censusSplitableOutput, expressionLO, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_facility3Buffer FID_facility3Buffer VISIBLE NONE;FID_SLCoTracts FID_SLCoTracts VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE RATIO;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE RATIO;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE RATIO;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE RATIO;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")

    return;

#Buffer Creation
def bufferTool (facility, bufferName, radius):
    arcpy.analysis.Buffer(facility, bufferName, str(radius) + " Miles", "FULL", "ROUND", "NONE", None, "PLANAR")

    return;

#union between buffer and census tracts (divisible)
def unionTool (unionInputs, unionName):
    arcpy.analysis.Union(unionInputs, unionName, "ALL", None, "GAPS")

    return;

def leftOverTool (unionName, leftOverLayer, expressionLO):
    arcpy.MakeFeatureLayer_management (unionName, leftOverLayer, expressionLO)

    return;


def clearConsole():
    clear()

def performLoop():
    #VARIABLES
    i = 1
    MetroPerCapitaSFMultiplier = 7.93
    radius = .1
    radiusIncrement = .02
    fieldNetSF = "USER_Net"
    bufferPopulationDemand = None
    netSquareFeet = None
    inTable = "SLCoCompetition_GeocodeAddre"
    fields = ["OBJECTID", "USER_Name_of_Store", "USER_Net"]


     #VARIABLES

    #  [{
    #   "OBJECTID": 0,
    #   "USER_Name_of_Store": "Storage Plus",
    #   "USER_Net": 1234
    #  },
    #  {
    #   "OBJECTID": 1,
    #   "USER_Name_of_Store": "Storage Plus Plus",
    #   "USER_Net": 12345
    #  }]

    # with arcpy.da.SearchCursor(inTable, fields) as cursor:
    # for row.USER_Name_of_Store in cursor:


    with arcpy.da.SearchCursor(inTable, fields) as cursor:
        for row in cursor:
            clearConsole()
            facility = "facility" + str(i)
            censusNonSplitable = "SLCoTractsSplitable" + str(i)
            bufferName = facility + "Buffer"
            unionName = bufferName + "Union"
            censusSplitable = "SLCoTractsSplitable" + str(i - 1)
            censusSplitableOutput = "SLCoTractsSplitable" + str(i)
            unionInputs = [bufferName, censusSplitable]
            expression = "FID_facility" + str(i) + "Buffer = 1"
            expressionLO = "FID_facility" + str(i) + "Buffer = -1"
            leftOverLayer = "SLCoTractsSplitable" + str(i)
            totalPopInCensusTract = ["why_csv_Total_population"]
            fieldsForDeletion = ["USER_Name_of_Store", "USER_Gross", "USER_Net", "BUFF_DIST", "ORIG_FID", "FID_facility" + str(i - 1) + "Buffer", "FID_facility" + str(i - 1) + "BufferUnion"]
            featureClassesForDeletion = [facility, bufferName, "facility" + str(i - 1) + "BufferUnion", censusSplitable]
           
            print("Iteration:", i)
            print('Store {0}, {1}, has Net Square Footage of {2}'.format(row[0],row[1], row[2]))
            radius = .1
            
            # This creates the a feature class that only has one feature in it so the caculations can be done.
            arcpy.management.MakeFeatureLayer(inTable, facility, "OBJECTID = " + str(row[0]))

            bufferPopulationDemand = 0

            netSquareFeet = getValueFromCompetitionTable(facility, fieldNetSF)
            while facilitySupplyIsGreaterThanbufferPopulationDemand(bufferPopulationDemand, netSquareFeet, radius, radiusIncrement):
                print("Radius is:", radius)

                bufferTool(facility, bufferName, radius)

                unionTool(unionInputs, unionName)

                #Print the Total population inside the buffer
                summedTotal = 0
                with arcpy.da.SearchCursor(unionName, totalPopInCensusTract, expression) as cursor2:
                    for row2 in cursor2:
                        summedTotal = summedTotal + row2[0]
                print('Total Population inside of the Buffer is:', summedTotal, 'people, multiplied by Salt Lake Metro Capita Multiplier of', MetroPerCapitaSFMultiplier, '=', summedTotal*MetroPerCapitaSFMultiplier, "Self Storage Square Feet Demanded.")
                bufferPopulationDemand = (summedTotal*MetroPerCapitaSFMultiplier)
                radius += radiusIncrement       
            
            #to delete extra fields in the leftover table that just build up over each iteration
            for field in fieldsForDeletion:
                arcpy.management.DeleteField(unionName, field)
            
            #leftOverTool(unionName, leftOverLayer, expressionLO)
            splitableToolEndOfLoop(unionName, censusSplitableOutput, expressionLO)
           
            for featureClass in featureClassesForDeletion:
                arcpy.management.Delete(featureClass, None)
            
            #next 2 lines only works in IDE or IDLE.  Have to press enter to continue
            #print("press enter to continue...")
            #input()
            i += 1
    return;


def executeProgram():
    splitableTool("SLCoTracts", "SLCoTractsSplitable0")
    performLoop()

    return;
         
#FUNCTIONS

executeProgram()

print ("Script has finished running!")



#import arcpy
#tractsTable = "SLCoTracts"
#fieldList = arcpy.ListFields(tractsTable)
#for fields in fieldList:
#    print (fields.name)