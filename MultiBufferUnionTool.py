import arcpy
from arcpy import env

env.workspace = r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Utah County\Novell Campus Storage\Novell Campus Storage.gdb"

# union tool - Cant get this section to work with the actual commands below...so I changed the commands below to something that worked
# in_features1 = ["PossNovellSSFac_Buffer1", "tl_2016_49_tract_Copy"]
# in_features2 = ["PossNovellSSFac_Buffer2", "tl_2016_49_tract_Copy"]
# in_features3 = ["PossNovellSSFac_Buffer3", "tl_2016_49_tract_Copy"]
# out_feature_class1 = "BufferUnion1"
# out_feature_class2 = "BufferUnion2"
# out_feature_class3 = "BufferUnion3"

# arcpy.Union_analysis (in_features1, out_feature_class1)
# arcpy.Union_analysis (in_features2, out_feature_class2)
# arcpy.Union_analysis (in_features3, out_feature_class3)
bufferList = ["1", "2", "3"]
inFeatures = ["Buffers\PossNovellSSFac_Buffer", "Tract_PCT"]

for bufferListIndex in bufferList:
    currentBufferUnion = "BufferUnion" + bufferListIndex
    arcpy.Union_analysis([inFeatures[0] + bufferListIndex, inFeatures[1]], currentBufferUnion)

# Make a layer tool uses the field info tool to get ratios for splitting demographics
# MakeFeatureLayer_management (in_features, out_layer, {where_clause}, {workspace}, {field_info})
input_features1 = "BufferUnion1"
input_features2 = "BufferUnion2"
input_features3 = "BufferUnion3"
outputin_layer1 = "F1Capture1"
outputin_layer2 = "F1Capture2"
outputin_layer3 = "F1Capture3"
outputout_layer1 = "LeftOver1"
outputout_layer2 = "LeftOver2"
outputout_layer3 = "LeftOver3"

arcpy.MakeFeatureLayer_management (input_features1, outputin_layer1, "FID_PossNovellSSFac_Buffer1 = 1")
arcpy.MakeFeatureLayer_management (input_features1, outputout_layer1, "FID_PossNovellSSFac_Buffer1 = -1")
arcpy.MakeFeatureLayer_management (input_features2, outputin_layer2, "FID_PossNovellSSFac_Buffer2 = 1")
arcpy.MakeFeatureLayer_management (input_features2, outputout_layer2, "FID_PossNovellSSFac_Buffer2 = -1")
arcpy.MakeFeatureLayer_management (input_features3, outputin_layer3, "FID_PossNovellSSFac_Buffer3 = 1")
arcpy.MakeFeatureLayer_management (input_features3, outputout_layer3, "FID_PossNovellSSFac_Buffer3 = -1")

# sum up the people located in the buffer shown in feature class F1Capture
arcpy.Statistics_analysis("F1Capture1", "Sum_Stats1", [["TotPop", "SUM"]])
arcpy.Statistics_analysis("F1Capture2", "Sum_Stats2", [["TotPop", "SUM"]])
arcpy.Statistics_analysis("F1Capture3", "Sum_Stats3", [["TotPop", "SUM"]])
