#This is to be used on arcGIS project: SanDiego
import arcpy
from arcpy import env
env.workspace = r"C:\Users\Kyle\Documents\ArcGIS\Projects\SanDiego\SanDiego.gdb"

#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 2011 StatePlane California VI FIPS 0406 Ft US_1")
arcpy.env.overwriteOutput = True

##to fill in some fields that have missing Square Footage Data...this is an exercise!
 
## Retrieve input parameters: the feature class, the field affected by
##  the search and replace, the search term, and the replace term.
#fc = "SanDiegoCoSSCompTest"
#affectedField = "Net"
#oldValue = "-"
#newValue = "116,292.60"
 
## Create the SQL expression for the update cursor. Here this is
##  done on a separate line for readability.
#queryString = "Net = 'Null'"
## Create the update cursor and update each row returned by the SQL expression
#with arcpy.da.UpdateCursor(fc, (affectedField), queryString) as cursor:
#    for row in cursor:
#        row[0] = newValue
#        cursor.updateRow(row)

#print ('Done')


inTable = "SanDiegoCoSSCompTest"
fields = ["OBJECTID", "Name_of_Store", "Gross"]
bufferLayer = "bufferLayer"
symbologyLayer = "Geocoding_Result_2_Buffer"
with arcpy.da.SearchCursor(inTable, fields) as cursor:
	for row in cursor:
		facilityGrossSF = (float(row[2].replace(",", "")))*.03
		arcpy.management.MakeFeatureLayer(inTable, bufferLayer, "OBJECTID = " + str(row[0]))
		arcpy.analysis.Buffer(bufferLayer, "BufferForFacility" + str(row[0]), str(facilityGrossSF) + " Feet", "FULL", "ROUND", "NONE", None, "PLANAR")

arcpy.management.Merge(arcpy.ListFeatureClasses("BufferForFacility*"), "bufferMerge")
arcpy.management.ApplySymbologyFromLayer("bufferMerge", symbologyLayer, None)

print ('Done')


arcpy.management.SelectLayerByAttribute("SanDiegoCoSSCompTest", "NEW_SELECTION", "Gross = ' ? '", None)
arcpy.management.SelectLayerByAttribute("SanDiegoCoSSCompTest", "NEW_SELECTION", "Gross = '100000'", None)
arcpy.management.SelectLayerByAttribute("SanDiegoCoSSCompTest", "NEW_SELECTION", "Gross = ' -   '", None)
arcpy.management.SelectLayerByAttribute("SanDiegoCoSSCompTest", "NEW_SELECTION", "Net = ' -   '", None)