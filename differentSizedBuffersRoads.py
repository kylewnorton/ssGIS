import arcpy
from arcpy import env
env.workspace = r"C:\Users\Kyle\Documents\ArcGIS\Projects\roadTest\roadTest.gdb"

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.env.overwriteOutput = True

inTable = "AADT_Open_Data_CopyFeatures1"
fields = ["OBJECTID_1", "AADT2015"]
bufferLayer = "roadBuffer"
symbologyLayer = "zoning"
with arcpy.da.SearchCursor(inTable, fields) as cursor:
    for row in cursor:
        roadTraffic = row[1]*.01
        arcpy.management.MakeFeatureLayer(inTable, bufferLayer + str(row[0]), "OBJECTID_1 = " + str(row[0]))
        arcpy.analysis.Buffer(bufferLayer + str(row[0]), "BufferForRoad" + str(row[0]), str(roadTraffic) + " Feet", "FULL", "FLAT", "NONE", None, "PLANAR")


arcpy.management.Merge(arcpy.ListFeatureClasses("BufferForRoad*"), "bufferMerge")
#arcpy.management.ApplySymbologyFromLayer("bufferMerge", symbologyLayer, None)