import arcpy
from arcpy import env
env.workspace = r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb"

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.env.overwriteOutput = True

#VARIABLES
SLMetroPerCapitaSFMultiplier = 7.93
splitableInput = "SLCoTracts1"
censusSplitable = "SlCoTractsSplitable"
facilityFC = "Alpine"
fieldGrossSF = "USER_Gross"
bufferName = facilityFC + "Buffer"
unionName = bufferName + "Union"
unionInputs = [bufferName, censusSplitable]
radius = .1
radiusIncrement = .2
supply = None
demand = None
grossSquareFeet = None
expressionLO = "FID_AlpineBuffer = -1"
leftOverLayer = facilityFC + "LeftOver"
currentIndex = 0
#VARIABLES

# FUNCTIONS
#Retrieve the Square Footage supplied for the Facility
 #The following gives a list of fields to pick from:**********
    #fieldList = arcpy.ListFields(facilityFC)
    #for fields in fieldList:
    #    print (fields.name)
    #************************************************************
def getValueFromCompetitionTable(facilityFC, fieldGrossSF):
    expression = None
    facilityGrossSF = 0
    with arcpy.da.SearchCursor(facilityFC, fieldGrossSF, expression) as cursor:
        for row in cursor:
            facilityGrossSF = float(row[0].replace(",", ""))
    print ('The facility Gross Square Footage is:', facilityGrossSF)

    return facilityGrossSF;

def supplyIsGreaterThanDemand():
    if demand is None:
        return True;

    if supply < demand:
        print("Supply:", supply, ", Demand:", demand, " Equilibrium Found!!!")
    else :
        print("Supply is larger than demand, increasing radius from:", radius - radiusIncrement, " to:", radius)

    return supply > demand;

#To make a feature class "Divisible" or "Splitable"
def splitableTool (splitableInput, censusSplitable):
    arcpy.management.MakeFeatureLayer(splitableInput, censusSplitable, None, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;tl_2016_49_tract_STATEFP tl_2016_49_tract_STATEFP VISIBLE NONE;tl_2016_49_tract_COUNTYFP tl_2016_49_tract_COUNTYFP VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_NAMELSAD tl_2016_49_tract_NAMELSAD VISIBLE NONE;tl_2016_49_tract_MTFCC tl_2016_49_tract_MTFCC VISIBLE NONE;tl_2016_49_tract_FUNCSTAT tl_2016_49_tract_FUNCSTAT VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Id why_csv_Id VISIBLE NONE;why_csv_Id2 why_csv_Id2 VISIBLE NONE;why_csv_Geography why_csv_Geography VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE NONE;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE NONE;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE NONE;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE NONE;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE RATIO;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE")

    return;

#Buffer Creation
def bufferTool (facilityFC, bufferName, radius):
    arcpy.analysis.Buffer(facilityFC, bufferName, str(radius) + " Miles", "FULL", "ROUND", "NONE", None, "PLANAR")

    return;

#union between buffer and census tracts (divisible)
def unionTool (unionInputs, unionName):
    arcpy.analysis.Union(unionInputs, unionName, "ALL", None, "GAPS")

    return;

def leftOverTool (unionName, leftOverLayer, expressionLO):
    arcpy.MakeFeatureLayer_management (unionName, leftOverLayer, expressionLO)

    return;

#FUNCTIONS


#SCRIPT
splitableTool (splitableInput, censusSplitable)

grossSquareFeet = getValueFromCompetitionTable(facilityFC, fieldGrossSF)
supply = grossSquareFeet

while supplyIsGreaterThanDemand():
    bufferTool (facilityFC, bufferName, radius)

    unionTool (unionInputs, unionName)

    #Print the Total population inside the buffer
    fc = "AlpineBufferUnion"
    fields = ["why_csv_Total_population"]
    expression = "FID_AlpineBuffer = 1"
    summedTotal = 0
    with arcpy.da.SearchCursor(fc, fields, expression) as cursor:
        for row in cursor:
            summedTotal = summedTotal + row[0]
    print ('Total Population inside of the Buffer is:', summedTotal)
    print ('Population of', summedTotal, 'multiplied by Salt Lake Metro Capita Multiplier of', SLMetroPerCapitaSFMultiplier, '=', summedTotal*SLMetroPerCapitaSFMultiplier )
    demand = (summedTotal*SLMetroPerCapitaSFMultiplier)

    radius += radiusIncrement

leftOverTool (unionName, leftOverLayer, expressionLO)
#perhaps this should be renamed to SLCoTractsSplitable (for the next round)
#look how Dallas suggested iterating through

