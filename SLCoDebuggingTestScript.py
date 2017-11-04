import arcpy
from arcpy import env

env.workspace = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")

# VARIABLES
featureClassesForDeletion = ["LeftOver", "facCapture", "BufferUnion", "AlpineBuffer", "sumStats", "Buffer"]
fieldsForDeletion = ["NetSF", "NetSF95Occ"]
featureClass = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\Alpine"
radius = 1.0
radiusIncrement = .4
supply = None
demand = None
netSquareFeet = None
facilityBufferName = featureClass + "Buffer"
censusTracts = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\SLCoTractsSplitable1"
bufferUnion = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\BufferUnion"
outPutInsideLayer = "facCapture"
outPutOutsideLayer = "LeftOver"
nameOfSumTable = "sumStats"
fieldToSum = "why_csv_Total_population"
fieldNameToAdd = ["SFDemanded"]
popToSFMultiplier = 7.93
fieldToCalc = "SFDemanded"
# VARIABLES

# FUNCTIONS

def resetEnvironment(featureClassesForDeletion, fieldsForDeletion):
    for featureClass in featureClassesForDeletion:
        arcpy.management.Delete(featureClass, None)

    for fieldsForDel in fieldsForDeletion:
        arcpy.management.DeleteField("Alpine", fieldsForDel)

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
    arcpy.MakeFeatureLayer_management (bufferUnion, outPutInsideLayer, "FID_AlpineBuffer = 1")
    arcpy.MakeFeatureLayer_management (bufferUnion, outPutOutsideLayer, "FID_AlpineBuffer = -1")

    return;

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



# FUNCTIONS


# SCRIPT
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

    popToSFCalculation (nameOfSumTable, fieldToCalc, popToSFMultiplier)

    fc = nameOfSumTable
    field = fieldToCalc
    cursor = arcpy.SearchCursor(fc)
    for rowdemand in cursor:
        demand = (rowdemand.getValue(field))

    radius += radiusIncrement

