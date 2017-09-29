import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
env.workspace = "C:/desktop/SS GIS-Zoning-Competition"

# Prep environments
featureClassesForDeletion = ["LeftOver", "F1Capture", "BufferUnion", "Alpine_Buffer", "Sum_Stats", "Sum_Stats1"]
for thingVariable in featureClassesForDeletion:
    arcpy.management.Delete(thingVariable, None)

fieldDeletion = ["NetSF", "NetSF95Occ"]
for field in fieldDeletion:
    arcpy.management.DeleteField("Alpine", field)


# Add a Numeric Field for the facility then use the calculate tool to get a numeric value in the field
# Set local variables
inFeatures = "Alpine"
fieldName1 = "NetSF"
fieldPrecision = 15
fieldName2 = "NetSF95Occ"

arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE", fieldPrecision)
arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE", fieldPrecision)

# Times the TotPop times the Utah SLC 7.93/per person
arcpy.management.CalculateField("Alpine", "NetSF", '"250,466.00"', "PYTHON_9.3", None)
arcpy.management.CalculateField("Alpine", "NetSF95Occ", "!NetSF! * .95", "PYTHON_9.3", None)


# the buffer tool
facility = "Alpine"
output = "Alpine_Buffer"
distance = .01

# Run Buffer using the variables set above and pass the remaining
# parameters in as strings
arcpy.Buffer_analysis(facility, output, distance, "FULL", "ROUND", "NONE")

# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")


# union tool
in_features = ["Alpine_Buffer", "SLCoTractsDiv"]
out_feature_class = "BufferUnion"

arcpy.Union_analysis (in_features, out_feature_class)


# Make a layer tool uses the field info tool to get ratios for splitting demographics
# MakeFeatureLayer_management (in_features, out_layer, {where_clause}, {workspace}, {field_info})
input_features = "BufferUnion"
outputin_layer = "F1Capture"
outputout_layer = "LeftOver"

arcpy.MakeFeatureLayer_management (input_features, outputin_layer, "FID_Alpine_Buffer = 1")
arcpy.MakeFeatureLayer_management (input_features, outputout_layer, "FID_Alpine_Buffer = -1")

fieldToSum = "why_csv_Total_population"
# sum up the people located in the buffer shown in feature class F1Capture
arcpy.Statistics_analysis("F1Capture", "Sum_Stats", [[fieldToSum, "SUM"]])

# times the Sum by the SF demand per person
# First, Add the field to the sum table
# Set local variables
inFeatures = "Sum_Stats"
fieldName1 = "SFDemanded"
fieldPrecision = 15
fieldName2 = "NetSF"
fieldName3 = "NetSF95Occ"
fieldName4 = "FacilityID"

arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE", fieldPrecision)
arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE", fieldPrecision)
arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE", fieldPrecision)
arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE", fieldPrecision)

# Set local variable(s)
Multiplier = 7.93
tableToCalc = "Sum_Stats"
fieldToCalc = "SFDemanded"
capPopField = "!SUM_why_csv_Total_population!"

# Times the TotPop times the Utah SLC 7.93/per person
arcpy.management.CalculateField(tableToCalc, fieldToCalc, "capPopField * Multiplier", "PYTHON_9.3", None)


#**************************************************************
# to calculate if the script grew the buffer to be big enough
import arcpy

fc = "Alpine"
field = "NetSF"
cursor = arcpy.SearchCursor(fc)

# print (cursor)

for rowsupply in cursor:
    suppliedsf = (rowsupply.getValue(field))

fc = "Sum_Stats"
field = "SFDemanded"
cursor = arcpy.SearchCursor(fc)
for rowdemand in cursor:
    demandedsf = (rowdemand.getValue(field))

if demandedsf>suppliedsf:
    print ("Yes")
else:
    print("No")
