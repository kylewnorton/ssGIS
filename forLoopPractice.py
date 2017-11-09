import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
env.workspace = "C:/desktop/SS GIS-Zoning-Competition"

# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")

# VARIABLES
featureClassesForDeletion = ["LeftOver", "facCapture", "BufferUnion", "AlpineBuffer", "sumStats", "Buffer"]
fieldsForDeletion = ["NetSF", "NetSF95Occ"]
featureClass = "SLCoCompetitionFew"
radius = .1
radiusIncrement = .4
supply = None
demand = None
netSquareFeet = None
facilityBufferName = featureClass + "Buffer"
censusTracts = "SLCoTractsDiv"
bufferUnion = "BufferUnion"
outPutInsideLayer = "facCapture"
outPutOutsideLayer = "LeftOver"
nameOfSumTable = "sumStats"
fieldToSum = "why_csv_Total_population" #is there a way to look this up?  Or should I have more code to get ready for this?
# could have python look up the table?
fieldNameToAdd = ["SFDemanded"]
popToSFMultiplier = 7.93
fieldToCalc = "SFDemanded"
competitionFacilities = "SLCoCompetitionFew"
# VARIABLES


# FUNCTIONS

# Reset environment
def resetEnvironment(featureClassesForDeletion, fieldsForDeletion):
    for featureClass in featureClassesForDeletion:
        arcpy.management.Delete(featureClass, None)

    for field in fieldsForDeletion:
        arcpy.management.DeleteField("Alpine", field)

    return;

def getNetSquareFootageAsFloat(netSqFt):
    return float(netSqFt);

def getValueFromCompetitionTable(field):
    # for field in arcpy.ListFields("Alpine"):
    #     print(field.name)

    with arcpy.da.SearchCursor(featureClass, field) as cursor:
        for row in cursor:
            value = float(row[0].replace(",", ""))

    return value;

def supplyIsGreaterThanDemand():
    if demand is None:
        return True;

    if supply < demand:
        print("Supply:", supply, ", Demand:", demand, " Found Site!!!")
    else :
        print("Supply is larger than demand, increasing radius from:", radius - radiusIncrement, " to:", radius)

    return supply > demand;

def bufferTool (featureClass, facilityBufferName):
    arcpy.Buffer_analysis(featureClass, facilityBufferName, str(radius) + " Miles", "FULL", "ROUND", "NONE")

    return;

def unionTool (facilityBufferName, censusTracts, bufferUnion):
    inFeatures = [facilityBufferName, censusTracts]
    arcpy.Union_analysis (inFeatures, bufferUnion)

    return;

def splitUnionTool (outPutInsideLayer, outPutOutsideLayer, bufferUnion):
    arcpy.MakeFeatureLayer_management (bufferUnion, outPutInsideLayer, "FID_AlpineBuffer = 1") #I think I could use a dictionary here
    arcpy.MakeFeatureLayer_management (bufferUnion, outPutOutsideLayer, "FID_AlpineBuffer = -1") #I think I could use a dictionary here

    return;

# I think I can substitute this with a PYTHON statement
def sumInsideBuffer (outPutInsideLayer, nameOfSumTable, fieldToSum):
    arcpy.Statistics_analysis(outPutInsideLayer, nameOfSumTable, [[fieldToSum, "SUM"]])

    return;

def addFieldToSumTable (nameOfSumTable, fieldNameToAdd):
    for fieldNameIndex in fieldNameToAdd:
        inFeatures = nameOfSumTable
        fieldPrecision = 15
        arcpy.AddField_management(inFeatures, fieldNameIndex, "DOUBLE", fieldPrecision)

    return;

def popToSFCalculation (nameOfSumTable, fieldToCalc, popToSFMultiplier):
    capturedPopField = "!SUM_why_csv_Total_population!"
    arcpy.management.CalculateField(nameOfSumTable, fieldToCalc, "!SUM_why_csv_Total_population! * popToSFMultiplier", "PYTHON_9.3", None)

    return;

def numberOfFacilities ():


    return;

# FUNCTIONS


resetEnvironment(featureClassesForDeletion, fieldsForDeletion)

# netSquareFeet = getValueFromCompetitionTable("USER_Net")
# supply = netSquareFeet

# list fields
featureclass = "SLCoCompetitionFew"






#*****************************this works**********************************************************************************8
inTable = "SLCoCompetitionFew"
# inField = ["USER_Net"]
with arcpy.da.SearchCursor(inTable, ["USER_Name_of_Store", "USER_Net"]) as cursor:
    for row in cursor:
        print('Store {0} has net SF of {1}'.format(row[0], row[1]))
#*********************why I can't get it to do anything else is beyond me.

# everything below this sucks!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1



import arcpy
for field in arcpy.ListFields("SLCoTractsSplitable43"):
    print(field.name)



fieldsForDeletion = ["Loc_name_*", "Status_*", "Score_*", "Match_type_*", "Match_addr_*", "LongLabel_*", "ShortLabel_*", "Addr_type_*", "Place_addr_*", "Rank_*", "AddNum_*", "AddNumFrom_*", "AddNumTo_*", "AddRange_*", "Side_*", "StPreDir_*", "StName_*", "StType_*", "StDir_*", "StAddr_*", "City_*", "Subregion_*", "Region_*", "RegionAbbr_*", "Postal_*", "Country_*", "LangCode_*", "Distance_*", "X_*", "Y_*", "DisplayX_*", "DisplayY_*", "Xmin_*", "Xmax_*", "Ymin_*", "Ymax_*", "ExInfo_*", "IN_Address_*", "IN_City_*", "IN_Postal_*", "USER_Object_ID_*", "USER_Name_of_Store_*", "USER_Street_*", "USER_City_*", "USER_St_*", "USER_Zip_*", "USER_Gross_*", "USER_Net_*", "USER_Notes_*", "USER_Developer_*", "USER_Status_*", "USER_Units_*", "USER_Date_Entered_*", "USER_*", "0x*", "0_climate_*", "USER_*", "0x*", "0_non_climate_*", "USER_Lattitude_*", "USER_Longitude_*", "USER_Field*", "9_*", "BUFF_DIST_*", "ORIG_FID_*"]

for field in fieldsForDeletion:
    arcpy.management.DeleteField("SLCoTractsSplitable43", field)




Loc_name_1
Status_1
Score_1
Match_type_1
Match_addr_1
LongLabel_1
ShortLabel_1
Addr_type_1
Place_addr_1
Rank_1
AddNum_1
AddNumFrom_1
AddNumTo_1
AddRange_1
Side_1
StPreDir_1
StName_1
StType_1
StDir_1
StAddr_1
City_1
Subregion_1
Region_1
RegionAbbr_1
Postal_1
Country_1
LangCode_1
Distance_1
X_1
Y_1
DisplayX_1
DisplayY_1
Xmin_1
Xmax_1
Ymin_1
Ymax_1
ExInfo_1
IN_Address_1
IN_City_1
IN_Postal_1
USER_Object_ID_1
USER_Name_of_Store_1
USER_Street_1
USER_City_1
USER_St_1
USER_Zip_1
USER_Gross_1
USER_Net_1
USER_Notes_1
USER_Developer_1
USER_Status_1
USER_Units_1
USER_Date_Entered_1
USER_10x10_climate_1
USER_10x10_non_climate_1
USER_Lattitude_1
USER_Longitude_1
USER_Field19_1
BUFF_DIST_1
ORIG_FID_1




























import arcpy

# delete old features so you get a blank slate to work with
for featuretodelete in ["ToysRus1", "ToysRus2", "ToysRus3", "SumStats1", "SumStats2", "SumStats3", "BufferUnion1", "BufferUnion2", "BufferUnion3", "F1Capture1", "F1Capture2", "F1Capture3", "LeftOver1", "LeftOver2", "LeftOver3", "FacilityCapture1M", "FacilityCapture2M", "FacilityCapture3M"]:
    arcpy.management.Delete(featuretodelete, None)

# set the environment so the path does not need to be typed for every feature class
from arcpy import env
env.workspace = r"C:\GISData\Utah\Salt Lake County\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"
#  step through a feature class and produce buffer
inTable = "SLCoCompetitionFew"
# inField = ["USER_Net"]
with arcpy.da.SearchCursor(inTable, ["StName", "USER_Net"]) as cursor:
    for row in cursor:
        facilityBufferName = row[0]
        value = float(row[1].replace(",", ""))
        arcpy.Buffer_analysis(featureClass, facilityBufferName, str(value) + " Feet", "FULL", "ROUND", "NONE")


inTable = "SLCFewComps_CopyRows"
with arcpy.da.SearchCursor(inTable, ["USER_Name_of_Store", "USER_Net"]) as cursor:
    for row in cursor:
        facilityBufferName = row[0]
        value = float(row[1].replace(",", ""))
        arcpy.Buffer_analysis(row[0], facilityBufferName, str(value) + " Feet", "FULL", "ROUND", "NONE")


# import modules
import arcpy, glob
from arcpy import env
env.workspace = r"C:\GISData\Utah\Salt Lake County\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"
# folder where shapefiles are stored
inTable = "SLCoCompetitionFew"
facilityBufferName = row[0]
# loop through all shapefiles
for shapefile in glob.glob( inTable + '*.shp' ):
     arcpy.Buffer_analysis( shapefile, r"C:\GISData\Utah\Salt Lake County\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb", "100 Feet", "FULL", "ROUND", "LIST", "Distance")


# step through a feature class and print specific field values
inTable = "SLCoCompetitionFew"
inField = ["USER_Net"]
with arcpy.da.SearchCursor(inTable, ["USER_Name_of_Store", "USER_Net"]) as cursor:
    for row in cursor:
        value = (row[1].replace(",", ""))
        arcpy.Buffer_analysis(inTable, row[0] + "Buffer", str(value) + " Feet", "FULL", "ROUND", "NONE")






# to get unique values
# values = [row[0] for row in arcpy.da.SearchCursor(inTable, inField)]
# uniqueValues = set(values)
# print(uniqueValues)
