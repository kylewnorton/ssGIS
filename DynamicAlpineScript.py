import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
env.workspace = "C:/desktop/SS GIS-Zoning-Competition"

# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")


# FUNCTIONS
# Reset environment
def resetEnvironment(featureClassesForDeletion, fieldsForDeletion):
    for featureClass in featureClassesForDeletion:
        arcpy.management.Delete(featureClass, None)


    for field in fieldDeletion:
        arcpy.management.DeleteField("Alpine", field)


def isDemandGreaterThanSupply(demand, supply):
    print(demand > supply)

# FUNCTIONS

featureClassesForDeletion = ["LeftOver", "facCapture", "BufferUnion", "AlpineBuffer", "sumStats", "Buffer"]
fieldsForDeletion = ["NetSF", "NetSF95Occ"]
resetEnvironment(featureClassesForDeletion, fieldsForDeletion)


radius = .1
while radius < .9:
    resetEnvironment(featureClassesForDeletion, fieldsForDeletion)

    # Add a Numeric Field for the facility then use the calculate tool to get a numeric value in the field
    fieldName = ["NetSF", "NetSF95Occ"]
    for fieldNameIndex in fieldName:
        facility = "Alpine"
        fieldPrecision = 15
        arcpy.AddField_management(facility, fieldNameIndex, "DOUBLE", fieldPrecision)

    # I know there is a way to incorporate this into the for loop above...but I am unsure on how to do it.
    arcpy.management.CalculateField(facility, "NetSF", '"250,466.00"', "PYTHON_9.3", None) #interesting syntax for the 250,466!!!!!!!!!!!!!!!!!!!!!!!
    arcpy.management.CalculateField(facility, "NetSF95Occ", "!NetSF! * .95", "PYTHON_9.3", None)


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

    #**************************************************************
    fc = "Alpine"
    field = "NetSF"
    cursor = arcpy.SearchCursor(fc)

    # print (cursor)

    for rowsupply in cursor:
        suppliedsf = (rowsupply.getValue(field))

    fc = "sumStats"
    field = "SFDemanded"
    cursor = arcpy.SearchCursor(fc)
    for rowdemand in cursor:
        demandedsf = (rowdemand.getValue(field))

    isDemandGreaterThanSupply(demandedsf, suppliedsf)

    radius += .1
