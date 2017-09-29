# use this tool when you need to determine how much of the population it serves
import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
env.workspace = "C:/desktop/SS GIS-Zoning-Competition"

# cleanup the map file before running the script
featureClassesForDeletion = ["LeftOver", "F1Capture", "BufferUnion", "Alpine_Buffer", "Sum_Stats", "Sum_Stats1"]
for thingVariable in featureClassesForDeletion:
    arcpy.management.Delete(thingVariable, None)

fieldDeletion = ["NetSF", "NetSF95Occ"]
for field in fieldDeletion:
    arcpy.management.DeleteField("Alpine", field)

# Make a layer tool uses the field info tool to get ratios for splitting demographics#

#Union Tool - Combine the Buffer Outputs with the Census Tracts
radiusList = ["1", "2", "3"]
inFeatures = ["Buffers\PossNovellSSFac_Buffer", "TractRatioLayer"]

for radiusListIndex in radiusList:
    currentBufferUnion = "BufferUnion" + radiusListIndex #this creates the output feature layer
    arcpy.Union_analysis([inFeatures[0] + radiusListIndex, inFeatures[1]], currentBufferUnion)


# MakeFeatureLayer_management (in_features, out_layer, {where_clause})
# This may prove useful in showing a visualization...but I do not think it is necessary
for radiusListIndex in radiusList:
    input_feature = "BufferUnion" + radiusListIndex #this creates the input feature layer
    facilityCapture = "FacilityCapture" + radiusListIndex + "M"
    arcpy.MakeFeatureLayer_management(input_feature, facilityCapture, "FID_PossNovellSSFac_Buffer" + radiusListIndex + " = 1")

# sum up the people located in the buffer shown in feature class F1Capture
for radiusListIndex in radiusList:
    arcpy.Statistics_analysis("FacilityCapture" + radiusListIndex + "M", "Sum_Stats" + radiusListIndex, [["TotPop", "SUM"]])

# Why can't I print this?...weird...because arcpy/arcGIS does not allow it?
# print "All Done!"
