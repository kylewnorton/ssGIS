import arcpy
from arcpy import env
env.workspace = r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb"

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.env.overwriteOutput = True

inTable = "SLCComFew"
fields = ["OBJECTID", "USER_Name_of_Store", "USER_Gross"]
bufferLayer = "bufferLayer"
symbologyLayer = "AlpineBuffer"
with arcpy.da.SearchCursor(inTable, fields) as cursor:
	for row in cursor:
		facilityGrossSF = (float(row[2].replace(",", "")))*.03
		arcpy.management.MakeFeatureLayer(inTable, bufferLayer, "OBJECTID = " + str(row[0]))
		arcpy.analysis.Buffer(bufferLayer, "BufferForFacility" + str(row[0]), str(facilityGrossSF) + " Feet", "FULL", "ROUND", "NONE", None, "PLANAR")

arcpy.management.Merge(arcpy.ListFeatureClasses("BufferForFacility*"), "bufferMerge")
arcpy.management.ApplySymbologyFromLayer("bufferMerge", symbologyLayer, None)