# use this tool when you need to create multiple buffers for a possible facility...even the analysis after the filter?
# this tool will calculate the demographics in the 1, 2, 3 mile radii
import arcpy

# delete old features so you get a blank slate to work with
for featuretodelete in ["sandyPossible1", "sandyPossible2", "sandyPossible3", "SumStats1", "SumStats2", "SumStats3", "BufferUnion1", "BufferUnion2", "BufferUnion3", "F1Capture1", "F1Capture2", "F1Capture3", "LeftOver1", "LeftOver2", "LeftOver3", "FacilityCapture1M", "FacilityCapture2M", "FacilityCapture3M"]:
    arcpy.management.Delete(featuretodelete, None)

# set the environment so the path does not need to be typed for every feature class
from arcpy import env
env.workspace = r"C:\Users\Kyle\Desktop\SS GIS-Zoning-Competition\Utah\Salt Lake County\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"
arcpy.env.overwriteOutput = True

# Make a layer tool uses the field info tool to get ratios for splitting demographics#
site = "sandyPossible"
tracts = "SLCoTractsDiv"

#Union Tool - Combine the Buffer Outputs with the Census Tracts
radiusList = ["3", "2", "1"]
inFeatures = [site, tracts]

for radiusListIndex in radiusList:
    facilityBufferName = site + radiusListIndex
    arcpy.Buffer_analysis(site, facilityBufferName, str(radiusListIndex) + " Miles")
    currentBufferUnion = "BufferUnion" + radiusListIndex #this creates the output feature layer
    arcpy.Union_analysis([inFeatures[0] + radiusListIndex, inFeatures[1]], currentBufferUnion)

    # MakeFeatureLayer_management (in_features, out_layer, {where_clause})
    # This may prove useful in showing a visualization...but I do not think it is necessary
    input_feature = "BufferUnion" + radiusListIndex #this creates the input feature layer
    facilityCapture = "FacilityCapture" + radiusListIndex + "M"
    arcpy.MakeFeatureLayer_management(input_feature, facilityCapture, "FID_" + site + radiusListIndex + " = 1")

    # sum up the people located in the buffer shown in feature class FacilityCapture
    arcpy.Statistics_analysis("FacilityCapture" + radiusListIndex + "M", "SumStats" + radiusListIndex, [["Total Population", "SUM"]])

print("All Done!")
