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
featureClass = "Alpine"
radius = .1
radiusIncrement = .1
supply = None
demand = None
netSquareFeet = None
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

# FUNCTIONS


resetEnvironment(featureClassesForDeletion, fieldsForDeletion)

netSquareFeet = getValueFromCompetitionTable("USER_Net")
supply = netSquareFeet

while supplyIsGreaterThanDemand():
    resetEnvironment(featureClassesForDeletion, fieldsForDeletion)

    # the buffer tool
    facility = "Alpine"
    facBufferName = "AlpineBuffer"

    # Run Buffer using the variables set above and pass the remaining
    # parameters in as strings
    arcpy.Buffer_analysis(facility, facBufferName, str(radius) + " Miles", "FULL", "ROUND", "NONE")

    # union tool
    inFeatures = [facBufferName, "SLCoTractsDiv"]
    bufferUnion = "BufferUnion"

    arcpy.Union_analysis (inFeatures, bufferUnion)


    # Make a layer tool uses the field info tool to get ratios for splitting demographics
    # MakeFeatureLayer_management (in_features, out_layer, {where_clause}, {workspace}, {field_info})
    outPutInsideLayer = "facCapture"
    outPutOutsideLayer = "LeftOver"
    arcpy.MakeFeatureLayer_management (bufferUnion, outPutInsideLayer, "FID_AlpineBuffer = 1") #I think I could use a dictionary here
    arcpy.MakeFeatureLayer_management (bufferUnion, outPutOutsideLayer, "FID_AlpineBuffer = -1") #I think I could use a dictionary here

    nameOfSumTable = "sumStats"
    fieldToSum = "why_csv_Total_population"
    # sum up the people located in the buffer shown in feature class F1Capture
    arcpy.Statistics_analysis(outPutInsideLayer, nameOfSumTable, [[fieldToSum, "SUM"]])

    # times the Sum by the SF demand per person
    # First, Add the field to the sum table
    # Set local variables
    fieldName = ["SFDemanded", "NetSF", "NetSF95Occ"]
    for fieldNameIndex in fieldName:
        inFeatures = "sumStats"
        fieldPrecision = 15
        arcpy.AddField_management(inFeatures, fieldNameIndex, "DOUBLE", fieldPrecision)

    # Times the TotPop times the Utah SLC 7.93/per person
    # Set local variable(s)
    Multiplier = 7.93
    tableToCalc = "sumStats"
    fieldToCalc = "SFDemanded"
    capturedPopField = "!SUM_why_csv_Total_population!"
    arcpy.management.CalculateField(tableToCalc, fieldToCalc, "!SUM_why_csv_Total_population! * 7.93", "PYTHON_9.3", None)

    #**********************************************`****************

    fc = "sumStats"
    field = "SFDemanded"
    cursor = arcpy.SearchCursor(fc)
    for rowdemand in cursor:
        demand = (rowdemand.getValue(field))

    radius += radiusIncrement
