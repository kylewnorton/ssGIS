# use this tool when you need to create multiple buffers for a possible facility...even the analysis after the filter?
# this tool will calculate the demographics in the 1, 2, 3 mile radii
import arcpy

# delete old features so you get a blank slate to work with
for featuretodelete in ["Sum_Stats1", "Sum_Stats2", "Sum_Stats3", "BufferUnion1", "BufferUnion2", "BufferUnion3", "F1Capture1", "F1Capture2", "F1Capture3", "LeftOver1", "LeftOver2", "LeftOver3", "FacilityCapture1M", "FacilityCapture2M", "FacilityCapture3M"]:
    arcpy.management.Delete(featuretodelete, None)

# set the environment so the path does not need to be typed for every feature class
from arcpy import env
env.workspace = r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Utah County\Novell Campus Storage\Novell Campus Storage.gdb"

# Make a layer tool uses the field info tool to get ratios for splitting demographics#

#Union Tool - Combine the Buffer Outputs with the Census Tracts
radiusList = ["1", "2", "3"]
inFeatures = ["Buffers\PossNovellSSFac_Buffer", "TractRatioLayer"]

for radiusListIndex in radiusList:
    currentBufferUnion = "BufferUnion" + radiusListIndex #this creates the output feature layer
    arcpy.Union_analysis([inFeatures[0] + radiusListIndex, inFeatures[1]], currentBufferUnion)

    # MakeFeatureLayer_management (in_features, out_layer, {where_clause})
    # This may prove useful in showing a visualization...but I do not think it is necessary
    input_feature = "BufferUnion" + radiusListIndex #this creates the input feature layer
    facilityCapture = "FacilityCapture" + radiusListIndex + "M"
    arcpy.MakeFeatureLayer_management(input_feature, facilityCapture, "FID_PossNovellSSFac_Buffer" + radiusListIndex + " = 1")

    # sum up the people located in the buffer shown in feature class F1Capture
    arcpy.Statistics_analysis("FacilityCapture" + radiusListIndex + "M", "Sum_Stats" + radiusListIndex, [["TotPop", "SUM"]])


# Why can't I print this?...weird...because arcpy/arcGIS does not allow it?
# print "All Done!"
