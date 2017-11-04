
import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
env.workspace = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"

# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")

# VARIABLES
featureClassesForDeletion = ["LeftOver", "facCapture", "BufferUnion", "AlpineBuffer", "sumStats", "Buffer"]
fieldsForDeletion = ["NetSF", "NetSF95Occ"]
featureClass = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\SLCComFew"
#featureClass = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\Alpine"

featrureClassName = "SLCComFew"

radius = .1
radiusIncrement = .4
supply = None
demand = None
netSquareFeet = None
facilityBufferName = featrureClassName + "- Facility "
censusTracts = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\SLCoTracts"
bufferUnion = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\BufferUnion"
outPutInsideLayer = featrureClassName + "- Facility "
outPutOutsideLayer = "LeftOver"
nameOfSumTable = "sumStats"
fieldToSum = "why_csv_Total_population" 
fieldNameToAdd = ["SFDemanded"]
popToSFMultiplier = 7.93
fieldToCalc = "SFDemanded"
featureClassIndex = 0
featureClassColumns = ["USER_Name_of_Store", "USER_Net", "USER_Gross"]
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
        print("Supply:", supply, ", Demand:", demand, " Equilibrium Found!!!")
    else :
        print("Supply is larger than demand, increasing radius from:", radius - radiusIncrement, " to:", radius)

    return supply > demand;

def bufferTool (featureClass, facilityBufferName):
    arcpy.Buffer_analysis(featureClass, facilityBufferName, str(radius) + " Miles", "FULL", "ROUND", "NONE")

    return;

def unionTool (facilityBufferName, censusTracts, bufferUnion):
    inFeatures = [facilityBufferName, censusTracts]
    arcpy.Union_analysis (inFeatures, bufferUnion, "All", None, "Gaps")

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

def buildNamesFromCurrentIndex (i, nameOfFacility):
    facilityBufferName + "- " + nameOfFacility + " " + str(i)
    outPutInsideLayer + str(i) + "Capture"
    #TODO: add rest of strings with indexes for ouput

    return;

def dynamicBufferTool (currentIndex, nameOfFacility):
    currentIndex += 1

    buildNamesFromCurrentIndex(currentIndex, nameOfFacility)


    resetEnvironment(featureClassesForDeletion, fieldsForDeletion)

    netSquareFeet = getValueFromCompetitionTable("USER_Net")
    supply = netSquareFeet

    while supplyIsGreaterThanDemand():
        resetEnvironment(featureClassesForDeletion, fieldsForDeletion)

        bufferTool (featureClass, facilityBufferName)

        unionTool (facilityBufferName, censusTracts, bufferUnion)

        splitUnionTool (outPutInsideLayer, outPutOutsideLayer, bufferUnion)

        sumInsideBuffer (outPutInsideLayer, nameOfSumTable, fieldToSum)

        addFieldToSumTable (nameOfSumTable, fieldNameToAdd)

        popToSFCalculation(nameOfSumTable, fieldToCalc, popToSFMultiplier)

        fc = nameOfSumTable
        field = fieldToCalc
        cursor = arcpy.SearchCursor(fc)
        for rowdemand in cursor:
            demand = (rowdemand.getValue(field))

        radius += radiusIncrement
# FUNCTIONS


















#dynamicBufferTool(featureClassIndex, "dallas is the best")







#inTable = "SLCoCompetitionFew"
## inField = ["USER_Net"]
#with arcpy.da.SearchCursor(inTable, ["USER_Name_of_Store", "USER_Net"]) as cursor:
#    for row in cursor:
#        print('Store {0} has net SF of {1}'.format(row[0], row[1]))


#loop over each row in the featureclass, then perform loop below on each
#todo: change thing to one more item in arrary from featureclass









# This is what Dallas and I worked on last night....but it didn't work in the end....keep as an idea of what TODO.
#with arcpy.da.searchcursor(featureclass, "*") as cursor:
#     for row in cursor:
#        print(row)
#        print('store {0} has net sf of {1} and gross of {2}'.format(row[0], row[15], row[2]))
#        dynamicbuffertool(row[0], row['gross'])



#arcpy.management.CopyFeatures("SLCComFew", r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\SLCComFew_CopyFeatures1", None, None, None, None)

