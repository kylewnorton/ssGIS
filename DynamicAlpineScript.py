import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
env.workspace = "C:/desktop/SS GIS-Zoning-Competition"

# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")

# Prep environments
featureClassesForDeletion = ["LeftOver", "facCapture", "BufferUnion", "AlpineBuffer", "sumStats", "Buffer"]
for thingVariable in featureClassesForDeletion:
    arcpy.management.Delete(thingVariable, None)

fieldDeletion = ["NetSF", "NetSF95Occ"]
for field in fieldDeletion:
    arcpy.management.DeleteField("Alpine", field)

radius = .1
while radius < .5:
    # the buffer tool
    facility = "Alpine"
    facBufferName = "AlpineBuffer"
    # Run Buffer using the variables set above and pass the remaining
    # parameters in as strings
    arcpy.Buffer_analysis(facility, facBufferName, radius, "Miles", "FULL", "ROUND", "NONE")
    # arcpy.analysis.Buffer("Alpine", r"C:\GISData\Utah\Salt Lake County\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\Buffer", ".1 Miles", "FULL", "ROUND", "NONE", None, "PLANAR")
    radius += .1
