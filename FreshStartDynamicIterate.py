#1st thing when establishing new map...go into the map and set up the projection
#import competition and Tracts (but add them to the geodatabase as well
#set up new work environment
import arcpy
from arcpy import env
import os
env.workspace = r"C:\Users\Kyle\Desktop\SS GIS-Zoning-Competition\SS GIS-Zoning-Competition\Projects\dynamicIterate\dynamicIterate.gdb"

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

def getValueFromCompetitionTable(facility, fieldGrossSF):
    expression = None
    facilityGrossSF = 0
    with arcpy.da.SearchCursor(facility, fieldGrossSF, expression) as cursor:
        for row in cursor:
            facilityGrossSF = float(row[0].replace(",", ""))
    print (facility, 'has a Gross Square Footage of:', facilityGrossSF)

    return facilityGrossSF;

def facilitySupplyIsGreaterThanbufferPopulationDemand(bufferPopulationDemand, grossSquareFeet, radius, radiusIncrement):
    if bufferPopulationDemand is None:
        return True;

    if grossSquareFeet < bufferPopulationDemand:
        print("grossSquareFeet:", grossSquareFeet, ", bufferPopulationDemand:", bufferPopulationDemand, " Equilibrium Found!!!")
    else :
        print("grossSquareFeet is larger than bufferPopulationDemand, increasing radius from:", radius, " to:", radius + radiusIncrement)

    return grossSquareFeet > bufferPopulationDemand;

#To make a feature class "Divisible" or "Splitable"
def splitableTool (censusNonSplitable, censusSplitable):
    arcpy.management.MakeFeatureLayer(censusNonSplitable, censusSplitable, None, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;tl_2016_49_tract_STATEFP tl_2016_49_tract_STATEFP VISIBLE NONE;tl_2016_49_tract_COUNTYFP tl_2016_49_tract_COUNTYFP VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_NAMELSAD tl_2016_49_tract_NAMELSAD VISIBLE NONE;tl_2016_49_tract_MTFCC tl_2016_49_tract_MTFCC VISIBLE NONE;tl_2016_49_tract_FUNCSTAT tl_2016_49_tract_FUNCSTAT VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Id why_csv_Id VISIBLE NONE;why_csv_Id2 why_csv_Id2 VISIBLE NONE;why_csv_Geography why_csv_Geography VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE NONE;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE NONE;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE NONE;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE NONE;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE RATIO;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE")

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
    radiusIncrement = .2
    fieldGrossSF = "USER_Gross"
    bufferPopulationDemand = None
    grossSquareFeet = None
    inTable = "SLCComFew"
    fields = ["OBJECTID", "USER_Name_of_Store", "USER_Gross"]
    #VARIABLES

    with arcpy.da.SearchCursor(inTable, fields) as cursor:
        for row in cursor:
            clearConsole()
            facility = "facility" + str(i)
            censusNonSplitable = "SLCoTractsSplitable" + str(i)
            bufferName = facility + "Buffer"
            unionName = bufferName + "Union"
            censusSplitable = "SLCoTractsSplitable" + str(i - 1) + "Again"
            censusSplitableOutput = "SLCoTractsSplitable" + str(i) + "Again"
            unionInputs = [bufferName, censusSplitable]
            expression = "FID_facility" + str(i) + "Buffer = 1"
            expressionLO = "FID_facility" + str(i) + "Buffer = -1"
            leftOverLayer = "SLCoTractsSplitable" + str(i)
            fields = ["why_csv_Total_population"]
           
            radius = .1
            bufferPopulationDemand = 0

            print("Iteration:", i)
            print("Radius is:", radius)
            print('Store {0}, {1}, has Gross SF of {2}'.format(row[0],row[1], row[2]))
            arcpy.management.MakeFeatureLayer(inTable, facility, "OBJECTID = " + str(row[0]))
            
            #splitableTool (censusNonSplitable, censusSplitable)

            grossSquareFeet = getValueFromCompetitionTable(facility, fieldGrossSF)
            while facilitySupplyIsGreaterThanbufferPopulationDemand(bufferPopulationDemand, grossSquareFeet, radius, radiusIncrement):
                bufferTool(facility, bufferName, radius)

                unionTool(unionInputs, unionName)

                #Print the Total population inside the buffer
                summedTotal = 0
                with arcpy.da.SearchCursor(unionName, fields, expression) as cursor2:
                    for row2 in cursor2:
                        summedTotal = summedTotal + row2[0]
                print('Total Population inside of the Buffer is:', summedTotal)
                print('Population of', summedTotal, 'multiplied by Salt Lake Metro Capita Multiplier of', MetroPerCapitaSFMultiplier, '=', summedTotal*MetroPerCapitaSFMultiplier )
                bufferPopulationDemand = (summedTotal*MetroPerCapitaSFMultiplier)

                radius += radiusIncrement
                print("Radius is:", radius)
            
            #next line only works in IDE or IDLE.  Have to press enter to continue
            leftOverTool(unionName, leftOverLayer, expressionLO)
            splitableTool(censusNonSplitable, censusSplitableOutput)
            input()
            i += 1
    return;


def executeProgram():
    splitableTool("SLCoTractsSplitable0", "SLCoTractsSplitable0Again")
    performLoop()

    return;
         
#FUNCTIONS

executeProgram()