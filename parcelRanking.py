import arcpy
from arcpy import env
env.workspace = r"C:\Users\Kyle\Documents\ArcGIS\Projects\roadTest\roadTest.gdb"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.env.overwriteOutput = True


parcels = "SandySSParcels"
roads = "AADT_Open_Data_CopyFeatures1"
spatialJoinName = "SandySSParcelsSPRoads"
fields = ["OBJECTID_1", "AADT2015"]
bufferLayer = "roadBuffer"
symbologyLayer = "zoning"

#This joins the roads to the parcels so then you have the attributes of the roads...then rank by Daily Traffic
arcpy.analysis.SpatialJoin(parcels, roads, spatialJoinName, "JOIN_ONE_TO_MANY", "KEEP_ALL", None,"INTERSECT", "30 Meters", None)
#arcpy.management.SelectLayerByAttribute(spatialJoinName, "NEW_SELECTION", "AADT2015 >= 9090", None)
