import arcpy

# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")

# the buffer tool
facility = "PossNovellSSFac"
output = "Buffer1M"
distance = (1, 2, 3)

# Run Buffer using the variables set above and pass the remaining
# parameters in as strings
distancelist =
for bufferList =
arcpy.analysis.Buffer(facility, output, "1 Miles", "FULL", "ROUND", "NONE", None, "PLANAR")

arcpy.analysis.Buffer("PossNovellSSFac", r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Utah County\Novell Campus Storage\Novell Campus Storage.gdb\PossNovellSSFac_Buffer", "1 Miles", "FULL", "ROUND", "NONE", None, "PLANAR")

# Import system modules
import arcpy
from arcpy import env

# Set environment settings
# env.workspace = "C:/data/airport.gdb"

# Set local variables
facility = "PossNovellSSFac"
outFeatureClass = "Buffer1M"
distances = [1,2,3]
bufferUnit = "miles"
for outFeatureClass in outFeatureClasses:
    arcpy.analysis.Buffer(facility, outFeatureClass, distances, bufferUnit, "", "ALL")


import arcpy

infile = "PossNovellSSFac"
distances =[1, 2, 3]
bufferUnit = "miles"
for distance in distances:
    outfile = "Buffer" + str(distances)
    arcpy.Buffer_analysis(infile, outfile, distance, bufferUnit, "Full", "Round", "LIST", "Distance")


# arcpy.env.workspace = "C:/data"
env.workspace = r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Utah County\Novell Campus Storage\Novell Campus Storage.gdb"



# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
facility = "PossNovellSSFac"
arcpy.analysis.Buffer(facility, r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Utah County\Novell Campus Storage\Novell Campus Storage.gdb\PossNovellSSFac_Buffer1", "1 Miles", "FULL", "ROUND", "NONE", None, "PLANAR")
arcpy.analysis.Buffer(facility, r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Utah County\Novell Campus Storage\Novell Campus Storage.gdb\PossNovellSSFac_Buffer2", "2 Miles", "FULL", "ROUND", "NONE", None, "PLANAR")
arcpy.analysis.Buffer(facility, r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Utah County\Novell Campus Storage\Novell Campus Storage.gdb\PossNovellSSFac_Buffer3", "3 Miles", "FULL", "ROUND", "NONE", None, "PLANAR")
