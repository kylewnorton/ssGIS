import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
# env.workspace = "C:/desktop/SS GIS-Zoning-Competition"
# env.workspace = r"C:\Users\Kyle\Desktop\Temp\newTest\newTest.gdb"
# env.workspace = r"C:\Users\Kyle\Desktop\SS GIS-Zoning-Competition\SS GIS-Zoning-Competition\Utah\Salt Lake County\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"
env.workspace = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"

# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")

# VARIABLES
featureClassesForDeletion = ["LeftOver", "facCapture", "BufferUnion", "AlpineBuffer", "sumStats", "Buffer"]
fieldsForDeletion = ["NetSF", "NetSF95Occ"]
featureClass = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\Alpine"
radius = .1
radiusIncrement = .4
supply = None
demand = None
netSquareFeet = None
facilityBufferName = featureClass + "Buffer"
censusTracts = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\SLCoTracts"
bufferUnion = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\BufferUnion"
outPutInsideLayer = "facCapture"
outPutOutsideLayer = "LeftOver"
nameOfSumTable = "sumStats"
fieldToSum = "why_csv_Total_population" #is there a way to look this up?  Or should I have more code to get ready for this?
# could have python look up the table?
fieldNameToAdd = ["SFDemanded"]
popToSFMultiplier = 7.93
fieldToCalc = "SFDemanded"
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

# arcpy.analysis.Union("AlpineBuffer #;SLCoTractsDiv #", r"C:\Users\Kyle\Desktop\SS GIS-Zoning-Competition\SS GIS-Zoning-Competition\Utah\Salt Lake County\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\BufferUnion", "ALL", None, "GAPS")

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



# FUNCTIONS


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
